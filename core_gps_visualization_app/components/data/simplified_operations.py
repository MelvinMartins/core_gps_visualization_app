"""Visualization Data Operations"""

from core_gps_visualization_app import data_config as data_config
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.data_config import info_id_legend

import logging

logger = logging.getLogger(__name__)


def parse_data(all_data, x_parameter, y_parameter, data_sources, legend_ids, time_range):
    """ Parse data from the DB that match the configuration
    into a list of charts that are ready to be plotted (and overlaid)

    Args:
        data_sources: data sources selected on UI configurations
        legend_ids: legend elements selected on UI configurations
        y_parameter: parameter name y selected on UI configurations
        x_parameter: parameter name x selected on UI configurations
        all_data: List of all XML documents (under JSON format)
        time_range: time range selected on UI configurations

    Returns: List of dicts that each represent one plot (check tests for more details)

    """
    # Instantiate list to return
    logger.info("Periodic task: START parsing data")

    list_of_charts = []
    all_ids = []
    offset = []
    min_val = float('-inf')
    max_val = float('inf')

    # data config instantiate
    list_parameters = data_config.list_parameters

    # If x is time (so x is already in every document along with y)
    # x of the document = x selected in configurations = variable from config file
    if x_parameter == data_config.variable:

        charts_to_overlay = []
        x_display_name = x_parameter
        for xml_file in all_data:
            parameter_ids = xml_file['dict_content']['data']['parameterIds']
            parameter_info = xml_file['dict_content']['data']["parameterInfo"]
            parameter_values = xml_file['dict_content']['data']["parameterValues"]

            data_source = parameter_ids['dataOriginID']

            if 'satelliteID' in parameter_ids:
                legend_id = parameter_ids['satelliteID']
            else:
                legend_id = None

            legend_id_name = info_id_legend['legendName'] + ': ' + str(legend_id)
            parameter_name = parameter_info['parameterName']

            if legend_id_name in legend_ids:
                # Only check documents that come from a selected data source
                if data_source in data_sources:
                    # 1 file = 1 group = 1 chart
                    if parameter_name == y_parameter:
                        y_display_name = utils.get_display_name(y_parameter, list_parameters)
                        y_unit = parameter_info['unit']
                        data = utils.parse_time_data(parameter_values, time_range)
                        chart_id = legend_id_name

                        chart_dict = {
                            'x': (x_display_name, None),
                            'y': (y_display_name, y_unit),
                            'ids': chart_id,
                            'data': data
                        }

                        min_val = min(min_val, data[0][0])
                        max_val = max(max_val, data[-1][0])

                        charts_to_overlay.append(chart_dict)
                        all_ids.append(chart_id)

            elif parameter_name == 'timeoffset':
                offset = utils.parse_time_data(parameter_values, time_range)

        list_of_charts = utils.merge_ids(all_ids, charts_to_overlay)

        data = []
        for offset_tuple in sorted(offset):
            if min_val < offset_tuple[0] < max_val:
                data.append(offset_tuple)

        offset = data

    # Every chart that hasn't time as x:
    else:
        all_x_dicts = []
        all_y_dicts = []
        all_x_ids = []
        all_y_ids = []

        # Check all files
        # For every file, if x/y then all its data are added to all_x_dicts/all_y_dicts
        for xml_file in all_data:
            parameter_ids = xml_file['dict_content']['data']['parameterIds']
            parameter_info = xml_file['dict_content']['data']["parameterInfo"]
            parameter_values = xml_file['dict_content']['data']["parameterValues"]

            data_source = parameter_ids['dataOriginID']

            if 'satelliteID' in parameter_ids:
                legend_id = parameter_ids['satelliteID']
            else:
                legend_id = None

            legend_id_name = info_id_legend['legendName'] + ': ' + str(legend_id)
            parameter_name = parameter_info['parameterName']

            if legend_id_name in legend_ids:
                # Only check documents that come from a selected data source
                if data_source in data_sources:
                    # 1 file for 1 group for 1 chart
                    if parameter_name == x_parameter:
                        x_display_name = utils.get_display_name(x_parameter, list_parameters)
                        x_unit = parameter_info['unit']
                        x_data = utils.parse_time_data(parameter_values, time_range)
                        # ids is a list of dict = utils.get_parameter_ids(dict_content, ids_parameters),
                        x_id = legend_id_name

                        x_dict = {
                            'x': (x_display_name, x_unit),
                            'ids': x_id,
                            'data': x_data,  # [{var1: x1}, {var2: x2}, etc]
                        }

                        all_x_dicts.append(x_dict)
                        all_x_ids.append(x_id)

                    # 1 file for 1 group for 1 chart
                    if parameter_name == y_parameter:
                        y_display_name = utils.get_display_name(y_parameter, list_parameters)
                        y_unit = parameter_info['unit']
                        y_data = utils.parse_time_data(parameter_values, time_range)
                        # ids is a list of dict = utils.get_parameter_ids(dict_content, ids_parameters),
                        y_id = legend_id_name

                        y_dict = {
                            'y': (y_display_name, y_unit),
                            'ids': y_id,
                            'data': y_data,
                        }

                        all_y_dicts.append(y_dict)
                        all_y_ids.append(y_id)

        parsed_x_charts = utils.merge_ids(all_x_ids, all_x_dicts)
        parsed_y_charts = utils.merge_ids(all_y_ids, all_y_dicts)

        # Merge x and y
        for x_chart in parsed_x_charts:
            y_chart = next((filter(lambda l: l['ids'] == x_chart['ids'], parsed_y_charts)))
            data = [(i[1], j[1]) for i, j in zip(x_chart['data'], y_chart['data'])]

            chart_dict = {
                'x': x_chart['x'],
                'y': y_chart['y'],
                'ids': x_chart['ids'],
                'data': data
            }

            list_of_charts.append(chart_dict)

    logger.info("Periodic task: FINISH parsing data")
    return list_of_charts, offset

