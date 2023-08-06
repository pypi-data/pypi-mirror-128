import boto3
import re
import logging, logging.config

from typing import List
from psycopg2 import connect


class ConnectionDescriptor:
    """
    ConnectionDescriptor is a wrapper to extract the needed information from
    the connections stored in glue to connect to a DB
    """

    def __init__(self,
                 name: str,
                 url: str,
                 username: str,
                 password: str):
        """

        :param name: the name of the connection in Glue Data Catalog
        :param url: the url of the connection
        :param username: the username used in the connection to connect to the DB
        :param password: the password to connect
        """
        self.name = name
        self.url = url
        self.username = username
        self.password = password

    @staticmethod
    def get_connection_descriptor(glue_conn_desc):
        """
        Creates a Glue connection based on the response returned by the
        boto3
        :param glue_conn_desc:
        :return: a ConnectionDescriptor
        """
        return ConnectionDescriptor(
            name=glue_conn_desc['Connection']['Name'],
            url=glue_conn_desc['Connection']['ConnectionProperties']['JDBC_CONNECTION_URL'],
            username=glue_conn_desc['Connection']['ConnectionProperties']['USERNAME'],
            password=glue_conn_desc['Connection']['ConnectionProperties']['PASSWORD']
        )


class ColumnDescriptor:
    """
    ColumnDescriptor describes a Column in Glue Data Catalog, in this version a
    column is described with a name, a type and a comment
    """

    def __init__(self,
                 name: str,
                 type: str,
                 comment: str = None):
        self.name = name
        self.type = type
        self.comment = comment

    def __str__(self):
        return str(self.to_glue_column_descriptor())

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, ColumnDescriptor):
            return self.name == other.name \
                   and self.type == other.type \
                   and self.comment == other.comment
        return False

    def to_glue_column_descriptor(self):
        """
        returns ColumnDescriptor in the dictionary form used in the boto3 api
        :return: a dictionary with keys Name, Type and Comment
        """

        column_dict = {
            'Name': self.name,
            'Type': self.type
        }

        if self.comment:
            column_dict['Comment'] = self.comment

        return column_dict

    @staticmethod
    def get_column_descriptor(glue_column_descriptor):
        """
        creates a ColumnDescriptor from the portion of response returned
        by boto3 api regarding the key 'Column'
        :param glue_column_descriptor:
        :return: a ColumnDescriptor
        """
        return ColumnDescriptor(
            name=glue_column_descriptor['Name'],
            type=glue_column_descriptor['Type'],
            comment=glue_column_descriptor['Comment'] if 'Comment' in glue_column_descriptor else None
        )


class SerdeInfoParametersDescriptor:

    def __init__(self,
                 path: str = None,
                 serialization_format: str = None):

        self.path = path
        self.serialization_format = serialization_format

    def __eq__(self, other):
        if isinstance(other, SerdeInfoParametersDescriptor):
            return self.path == other.path \
                   and self.serialization_format == other.serialization_format

    @staticmethod
    def get_serde_info_params_descriptor(serde_info_param):
        return SerdeInfoParametersDescriptor(
            path=serde_info_param['path'],
            serialization_format=serde_info_param['serialization.format']
        )

    def to_serde_info_parameters_descriptor(self):
        return {
            'path': self.path,
            'serialization.format': self.serialization_format
        }


class SerdeInfoDescriptor:

    def __init__(self,
                 serialization_library: str = None,
                 parameters: dict = None):
        self.serialization_library = serialization_library
        self.parameters = parameters

    def __eq__(self, other):
        if isinstance(other, SerdeInfoDescriptor):
            return self.serialization_library == other.serialization_library \
                   and self.parameters == other.parameters

        return False


    @staticmethod
    def get_serde_info_descriptor(serde_info):
        return SerdeInfoDescriptor(
            serialization_library=serde_info['SerializationLibrary'] if 'SerializationLibrary' in serde_info else None,
            parameters=serde_info['Parameters'] if 'Parameters' in serde_info else None
        )

    def to_serde_info_descriptor(self):
        return {
            'SerializationLibrary': self.serialization_library,
            'Parameters': self.parameters
        }


class StorageDescriptor:
    """
    StorageDescriptor represents the 'StorageDescriptor' tag in the
    response given by boto3
    """
    def __init__(self,
                 location: str,
                 columns: List[ColumnDescriptor],
                 input_format: str = None,
                 output_format: str = None,
                 compressed: bool = None,
                 serde_info: SerdeInfoDescriptor = None,
                 stored_as_subdirectories: bool = None):
        self.location = location
        self.columns = columns
        self.input_format = input_format
        self.output_format = output_format
        self.compressed = compressed
        self.serde_info = serde_info
        self.stored_as_subdirectories = stored_as_subdirectories

    def __eq__(self, other):
        if isinstance(other, StorageDescriptor):
            return self.location == other.location \
                   and self.columns == other.columns \
                   and self.input_format == other.input_format \
                   and self.output_format == other.output_format \
                   and self.compressed == other.compressed \
                   and self.serde_info == other.serde_info \
                   and self.stored_as_subdirectories == other.stored_as_subdirectories \

        return False

    def __str__(self):
        result = {
            'Columns': [ColumnDescriptor.to_glue_column_descriptor(col) for col in self.columns],
            'Location': self.location,
            'InputFormat': self.input_format if self.input_format else None,
            'OutputFormat': self.output_format if self.output_format else None,
            'Compressed': self.compressed if self.compressed else None,
            'SerdeInfo': self.serde_info.to_serde_info_descriptor() if self.serde_info else None,
            'StoredAsSubDirectories': self.stored_as_subdirectories if self.stored_as_subdirectories else None
        }

        return result

    @staticmethod
    def get_storage_descriptor(glue_storage_descriptor):
        """
        creates a StorageDescriptor from the 'StorageDescriptor' tag response
        :param glue_storage_descriptor:
        :return: a StorageDescriptor
        """
        return StorageDescriptor(
            location=glue_storage_descriptor['Location'],
            columns=[ColumnDescriptor.get_column_descriptor(col) for col in glue_storage_descriptor['Columns']],
            input_format=glue_storage_descriptor['InputFormat'] if 'InputFormat' in glue_storage_descriptor else None,
            output_format=glue_storage_descriptor['OutputFormat'] if 'OutputFormat' in glue_storage_descriptor else None,
            compressed=glue_storage_descriptor['Compressed'] if 'Compressed' in glue_storage_descriptor else None,
            serde_info=SerdeInfoDescriptor.get_serde_info_descriptor(
                glue_storage_descriptor['SerdeInfo']
            ) if 'SerdeInfo' in glue_storage_descriptor else None,
            stored_as_subdirectories=glue_storage_descriptor['StoredAsSubDirectories'] if 'StoredAsSubDirectories' in glue_storage_descriptor else None
        )

    def to_glue_storage_descriptor(self):

        result = {
            'Columns': [ColumnDescriptor.to_glue_column_descriptor(col) for col in self.columns],
            'Location': self.location
        }

        if self.input_format:
            result['InputFormat'] = self.input_format

        if self.output_format:
            result['OutputFormat'] = self.output_format

        if self.compressed is not None:
            result['Compressed'] = self.compressed

        if self.serde_info:
            result['SerdeInfo'] = self.serde_info.to_serde_info_descriptor()

        if self.stored_as_subdirectories is not None:
            result['StoredAsSubDirectories'] = self.stored_as_subdirectories

        return result


class PartitionKeyDescriptor:

    def __init__(self,
                 name: str,
                 type: str):
        self.name = name
        self.type = type

    def __eq__(self, other):
        if isinstance(other, PartitionKeyDescriptor):
            return self.name == other.name \
                   and self.type == other.type

        return False

    @staticmethod
    def get_partition_key_descriptor(partition_key: dict):
        return PartitionKeyDescriptor(
            name=partition_key['Name'],
            type=partition_key['Type']
        )

    def to_partition_key_descriptor(self):
        return {
            'Name': self.name,
            'Type': self.type
        }


class GlueTableDescriptor:
    """
    GlueTableDescriptor maps the response given by boto3 when querying the
    Glue Data Catalog
    """

    default_owner = 'de_owner'

    def __init__(self,
                 database_name: str,
                 name: str,
                 storage_descriptor: StorageDescriptor,
                 owner: str = default_owner,
                 partition_keys: List[PartitionKeyDescriptor] = None,
                 table_type: str = None):
        self.database_name = database_name
        self.name = name
        self.owner = owner
        self.storage_descriptor = storage_descriptor
        self.partition_keys = partition_keys
        self.table_type = table_type

    def __str__(self):

        result = {
            'Name': self.name,
            'Owner': self.owner,
            'StorageDescriptor': self.storage_descriptor.to_glue_storage_descriptor(),
            'PartitionKeys': [col.to_partition_key_descriptor() for col in self.partition_keys] if self.partition_keys else None,
            'TableType': self.table_type if self.table_type else None
        }

        return str(result)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, GlueTableDescriptor):
            return self.database_name == other.database_name \
                   and self.name == other.name \
                   and self.partition_keys == other.partition_keys \
                   and self.table_type == other.table_type \
                   and self.database_name == other.database_name \
                   and self.owner == other.owner \
                   and self.storage_descriptor == other.storage_descriptor
        return False

    @staticmethod
    def get_table_descriptor(glue_descriptor):
        """
        maps the boto3 api response to a GlueTableDescriptor
        :param glue_descriptor: the
        :return: a GlueTableDescriptor
        """
        return GlueTableDescriptor(
            database_name=glue_descriptor['DatabaseName'],
            name=glue_descriptor['Name'],
            owner=glue_descriptor['Owner'] if 'Owner' in glue_descriptor else GlueTableDescriptor.default_owner,
            storage_descriptor=StorageDescriptor.get_storage_descriptor(glue_descriptor['StorageDescriptor']),
            partition_keys=[
                PartitionKeyDescriptor.get_partition_key_descriptor(col) for col in glue_descriptor['PartitionKeys']
            ] if 'PartitionKeys' in glue_descriptor else None,
            table_type=glue_descriptor['TableType'] if 'TableType' in glue_descriptor else None
        )

    @staticmethod
    def get_table_descriptor_with_db(database_name: str, glue_descriptor):
        """
        maps the boto3 api response to a GlueTableDescriptor
        :param database_name:
        :param glue_descriptor:
        :return:
        """
        return GlueTableDescriptor(
            database_name=database_name,
            name=glue_descriptor['Name'],
            owner=glue_descriptor['Owner'] if 'Owner' in glue_descriptor else GlueTableDescriptor.default_owner,
            storage_descriptor=StorageDescriptor.get_storage_descriptor(glue_descriptor['StorageDescriptor']),
            partition_keys=[
                PartitionKeyDescriptor.get_partition_key_descriptor(col) for col in glue_descriptor['PartitionKeys']
            ] if 'PartitionKeys' in glue_descriptor else None,
            table_type=glue_descriptor['TableType'] if 'TableType' in glue_descriptor else None
        )

    def add_column(self, column: ColumnDescriptor):
        self.storage_descriptor.columns.append(column)

    def to_glue_full_descriptor(self):
        """
        returns the GlueTableDescriptor in the form it is used in most of
        the boto3 api
        :return:
        """

        result = {
            'Name': self.name,
            'Owner': self.owner,
            'StorageDescriptor': self.storage_descriptor.to_glue_storage_descriptor(),
        }

        if self.partition_keys:
            result['PartitionKeys'] = [col.to_partition_key_descriptor() for col in self.partition_keys]

        if self.table_type:
            result['TableType'] = self.table_type

        return result
