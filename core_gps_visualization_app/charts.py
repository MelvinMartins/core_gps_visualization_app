from core_gps_visualization_app.tasks import build_visualization_data
from core_gps_visualization_app.components.plots.operations import plot_layout_by_time_range

import param
import holoviews as hv
hv.extension('bokeh')


class Chart(param.Parameterized):
    plot_selected = param.Selector(default="Scatter", objects=["Scatter", "Line"])
    time_selected = param.Selector(default="Minutes", objects=["Seconds", "Minutes", "Hours", "Days"])

    def __init__(self, **params):
        super().__init__(**params)

    @param.depends('plot_selected', 'time_selected')
    def update_plot(self):
        self.plot_selected = self.plot_selected
        self.time_selected = self.time_selected
        visualization_data = build_visualization_data()
        if len(visualization_data) == 0:
            return '# No charts for this configuration...'
        chart = plot_layout_by_time_range(visualization_data, self.plot_selected, self.time_selected)

        return chart
