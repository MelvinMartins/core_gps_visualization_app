import random
import time

from core_gps_visualization_app.tasks import build_visualization_data
from core_gps_visualization_app.components.plots.operations import plot_layout
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.data_config import info_id_legend
from core_gps_visualization_app.data_config import list_parameters
from core_gps_visualization_app.data_config import info_data_source

import logging
import param
import panel as pn
import holoviews as hv

logger = logging.getLogger(__name__)
hv.extension('bokeh')

# Init legend
legend_name = info_id_legend['legendName']
legend_path = info_id_legend['legendPath']
legends = utils.query_data(legend_path)
for i in range(len(legends)):
    legends[i] = legend_name + ': ' + str(legends[i])

# Init x and y
variable = utils.get_variable()
parameters = utils.get_parameters()
x_parameter = [elt[1] for elt in variable + parameters]
y_parameter = [elt[1] for elt in parameters]

# Init data sources
data_sources_path = info_data_source['dataSourcePath']
data_sources = utils.query_data(data_sources_path)


class Chart(param.Parameterized):
    x_parameter = param.ObjectSelector(default=x_parameter[0], objects=x_parameter)
    y_parameter = param.ObjectSelector(default=y_parameter[0], objects=y_parameter)
    data_sources = param.ListSelector(default=[], objects=data_sources)

    plot_selected = param.Selector(default="Scatter", objects=["Scatter", "Line"])
    time_selected = param.Selector(default="Minutes", objects=["Seconds", "Minutes", "Hours", "Days"])
    legend = param.ListSelector(default=[], objects=legends)

    submit_button = param.Action(lambda x: x.param.trigger('submit_button'), label='Submit')

    def __init__(self, **params):
        self.x_parameter = self.x_parameter
        self.y_parameter = self.y_parameter
        self.data_sources = self.data_sources
        self.plot_selected = self.plot_selected
        self.time_selected = self.time_selected
        self.legend = self.legend
        self.update_plot()
        super().__init__(**params)

    @param.depends('submit_button')
    def update_plot(self):
        if len(self.data_sources) == 0:
            return '# Use the widgets to configure your visualization...'
        visualization_data = build_visualization_data(self.legend, self.x_parameter, self.y_parameter, self.data_sources, self.time_selected)
        if visualization_data is None:
            visualization_data = []
        if len(visualization_data) == 0:
            return '# No charts for this configuration...'
        chart = plot_layout(visualization_data, self.plot_selected)

        return chart

    @param.depends('plot_selected', 'time_selected', 'legend', 'x_parameter', 'y_parameter', 'data_sources')
    def update_variables(self):
        self.x_parameter = self.x_parameter
        self.y_parameter = self.y_parameter
        self.data_sources = self.data_sources
        self.plot_selected = self.plot_selected
        self.time_selected = self.time_selected
        self.legend = self.legend
