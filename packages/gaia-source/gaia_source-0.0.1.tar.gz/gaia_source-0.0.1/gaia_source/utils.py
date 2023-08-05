import asyncio
import aiocsv
import aiofiles
import asyncpg
import bs4
import csv
import httpx
import logging
import inspect
import multiprocessing
import gzip
import os
import types
import typing

from gaia_source.datatypes import DownloadOptions, DataPath, InstallOptions

from pathlib import Path

logger = logging.getLogger(__name__)

def obtain_paths(data_path: str) -> typing.List[DataPath]:
    datas = []
    for root, dirnames, filenames in os.walk(data_path):
        for filename in filenames:
            if not filename.endswith('csv.gz'):
                continue

            archive_path = os.path.relpath(os.path.join(root, filename))
            csv_path = os.path.relpath(os.path.join(root, Path(filename).stem))
            datas.append(DataPath(archive_path, csv_path))

    # Futher in the program, .csv.gz files are removed to conserve space on disk. This second set of logic in this
    #  function returns the same value, but focuses on calculating the paths for a .csv file rather than a .csv.gz file.
    for root, dirnames, filenames in os.walk(data_path):
        for filename in filenames:
            if not filename.endswith('.csv'):
                continue

            archive_path = os.path.relpath(os.path.join(root, filename))
            archive_path = f'{archive_path}.gz'
            csv_path = os.path.relpath(os.path.join(root, filename))
            if not csv_path in [data.csv_path for data in datas]:
                datas.append(DataPath(archive_path, csv_path))

    return datas


async def download_data(data_path: str, download_option: DownloadOptions) -> typing.List[DataPath]:
    # http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/
    if download_option is DownloadOptions.Zero:
        return None

    elif download_option is DownloadOptions.Five:
        max_listing = 5

    else:
        raise NotImplementedError

    if not os.path.exists(data_path):
        os.makedirs(data_path)


    gaia_source_csv_path = 'http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/'
    links = []
    filepaths = []
    async with httpx.AsyncClient() as client:
        logger.info('Downloading gaia_source listing')
        response = await client.get(gaia_source_csv_path)
        logger.info(f'Parsing gaia_source listing')
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        logger.info(f'Extracting gaia_source links')
        for anchor in soup.findAll('a', ):
            anchor_path = anchor['href']
            if anchor_path.lower().startswith('gaiasource_'):
                link = f'{gaia_source_csv_path}{anchor_path}'
                links.append(link)

            if len(links) >= max_listing:
                break


        chunk_length = 1024 * 8
        for link in links:
            filename = Path(link).name
            filepath = os.path.join(data_path, filename)
            if not os.path.exists(filepath):
                async with client.stream('GET', link) as stream:
                    content_length = stream.headers['Content-Length']
                    logger.info(f'Downloading file: {filename} - Size: content_length')
                    async with aiofiles.open(filepath, 'wb') as local_stream:
                        async for chunk in stream.aiter_bytes(chunk_length):
                            await local_stream.write(chunk)

    return obtain_paths(data_path)


class MultiprocessAsyncioBase(type):
    def __new__(cls, name, bases, attrs, **kwargs) -> typing.Any:
        super_new = super().__new__
        if attrs.get('run_invocation', None) is None:
            raise NotImplementedError(f'Missing invocation function signature: run_invocation(self, input) -> None')

        if not '__init__' in attrs.keys():
            def __init__(self, count: int = 10) -> None:
                self._count = count

            attrs.update({'__init__': __init__})
        else:
            attrs.update({'_count': 10, '_inputs': []})

        async def invoke(self) -> None:
            if len(self._inputs) > 1:
                with multiprocessing.Pool(self._count) as pool:
                    pool.map(self.run_invocation, self._inputs)
            else:
                function_async = inspect.iscoroutinefunction(self.run_invocation)
                if function_async:
                    await self.run_invocation()

                else:
                    self.run_invocation()


        attrs.update({'invoke': invoke})

        if not '__aenter__' in attrs.keys():
            async def __aenter__(self):
                return self

            attrs.update({'__aenter__': __aenter__})

        if not '__aexit__' in attrs.keys():
            async def __aexit__(self, exc_type, exc, tb) -> None:
                pass

            attrs.update({'__aexit__': __aexit__})

        return super_new(cls, name, bases, attrs)


class UnarchiveData(metaclass=MultiprocessAsyncioBase):
    def __init__(self, datas: typing.List[DataPath]) -> None:
        self._inputs = datas

    def run_invocation(self, data: DataPath) -> None:
        '''
        Used to decompress a single archive file.
        '''
        if not os.path.exists(data.path):
            return None

        logger.info(f'Decompressing {data.csv_path}')
        with open(data.path, 'rb') as compressed_stream:
            with open(data.csv_path, 'wb') as csv_stream:
                csv_stream.write(gzip.decompress(compressed_stream.read()))

        # Remove the archive path because its no longer nessicary
        os.remove(data.path)


class CreateDatabaseTable(metaclass=MultiprocessAsyncioBase):
    def __init__(self, table_headers: typing.List[str]) -> None:
        self._table_headers = table_headers
        self._table_name = 'gaia_source'
        self._database_name = 'gaia_source'
        self._database_connection = None


    async def run_invocation(self) -> None:
        logger.info(f'Create Database Table: {self._table_name}')
        columns = [f'{header} TEXT NULL' for header in self._table_headers]
        formatted_columns = ','.join(columns)
        sql_string = f"""CREATE TABLE IF NOT EXISTS {self._table_name} (
{formatted_columns});"""
        await self._database_connection.execute(sql_string)


    async def __aenter__(self) -> None:
        self._database_connection = await asyncpg.connect(database=self._database_name)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self._database_connection.close()
        self._database_connection = None


class InsertData(metaclass=MultiprocessAsyncioBase):
    def __init__(self, datas: typing.List[DataPath], column_names: typing.List[str]) -> None:
        self._inputs = datas
        self._database_name = 'gaia_source'
        self._table_name = 'gaia_source'
        self._column_names = column_names

    async def insert_data(self, data: DataPath) -> None:
        database_connection = await asyncpg.connect(database=self._database_name)
        formatted_columns = ','.join(self._column_names)
        filepath = os.path.abspath(data.csv_path)
        sql_string = f'''COPY {self._table_name} ({formatted_columns}) FROM '{filepath}' DELIMITER ',' CSV HEADER;'''

        # Insert data and close database connection
        logger.info(f'Inserting data from file: {data.csv_path}')
        await database_connection.execute(sql_string)
        await database_connection.close()

    def run_invocation(self, data: DataPath) -> None:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.insert_data(data))


class LoadData:
    def __init__(self, datas: typing.List[DataPath]) -> None:
        self._datas = datas

    async def extract_table_headers_from_data_path(self, data: DataPath) -> None:
        async with aiofiles.open(data.csv_path, 'r') as local_stream:
            async for row in aiocsv.AsyncReader(local_stream):
                return row


    async def process(self) -> None:
        self._table_name = 'gaia_source'
        self._database_name = 'gaia_source'
        self._database_connection = None

        '''
        Begin ETL process from achive format on disk to PostgreSQL
        '''
        async with UnarchiveData(self._datas) as load_data:
            await load_data.invoke()

        table_headers = await self.extract_table_headers_from_data_path(self._datas[0])
        async with CreateDatabaseTable(table_headers) as service:
            await service.invoke()

        async with InsertData(self._datas, table_headers) as service:
            await service.invoke()


async def load_data(data_path: str, install_options: InstallOptions) -> None:
    logger.info('Installing Data')
    data_paths = obtain_paths(data_path)
    etl_controller = LoadData(data_paths)
    await etl_controller.process()

