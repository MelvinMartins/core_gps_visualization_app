import panel as pn

#from core_gps_visualization_app.test import Chart
from core_gps_visualization_app.charts import Chart
pn.extension(loading_spinner='dots', loading_color='#000000', sizing_mode="scale_width")
pn.param.ParamMethod.loading_indicator = True


def app(doc):
    chart = Chart()
    row = pn.Row(pn.Column(pn.Param(chart.param, name="Configure Visualization:")), chart.update_plot,
                 chart.update_variables)
    row.server_doc(doc)