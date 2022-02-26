"""
Data models
"""

from django_mongoengine import fields, Document
from core_gps_visualization_app import data_config
from core_gps_visualization_app.utils import data_utils as utils


class DataSources(Document):
    """ Data Structure to fill Django Form. Object is used to optimize loading time

    """
    data_sources = fields.ListField(blank=False)

    @staticmethod
    def create_data_sources():
        """
        Returns: data source is a list of tuples

        """
        data_sources = []
        data_source_path = data_config.info_data_source['dataSourcePath']

        all_data = utils.get_all_data()
        for xml_file in all_data:
            dict_content = xml_file['dict_content']
            data_source = utils.get_value_by_path(dict_content, data_source_path)
            if data_source not in data_sources:
                data_sources.append(data_source)

        return DataSources.objects.create(data_sources=data_sources)

    @staticmethod
    def update_data_sources():
        """

        Returns:

        """
        DataSources.objects.all().delete()
        return DataSources.create_data_sources()

    @staticmethod
    def get_data_sources():
        """
        Returns:

        """
        if len(DataSources.objects.all()) == 0:
            DataSources.create_data_sources()
        data_sources_object = DataSources.objects.all()[0]
        return data_sources_object.data_sources

