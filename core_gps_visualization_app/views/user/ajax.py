from django.http import HttpResponseBadRequest, HttpResponse
import json
import copy
import holoviews as hv

from core_gps_visualization_app.components.plots import api as plots_api
from core_gps_visualization_app.components.data import operations
from core_gps_visualization_app.components.plots import operations as plots_operations
from core_gps_visualization_app.views.user.forms import SelectPlotDropDown, SelectTimeRangeDropDown

def build_visualization_data():
    all_parsed_data = operations.get_all_data()
    all_parsed_data = operations.parse_all_data(all_parsed_data)
    plots_object = plots_api.create_and_get_plots(all_parsed_data)
    plots_api.update_completed(plots_object)


def load_initial_plots(request):
    """ load layout plots into the visualization page

    Args:
        request:

    Returns:
    """
    try:
        # Load all visualizations in Python objects before continuing the thread
        plots_object = plots_api.get_plots()
        charts_html = "<p>Charts are still loading, please come back later..</p>"

        if plots_object is None:
            # Launch task to build plots
            build_visualization_data()
            return HttpResponse(json.dumps({'charts_html': charts_html}), content_type='application/json')

        if not plots_api.is_completed(plots_object):
            # If task to build plots is not completed
            return HttpResponse(json.dumps({'charts_html': charts_html}), content_type='application/json')

        else:
            plots_types = SelectPlotDropDown().fields['plots'].choices
            time_ranges = SelectTimeRangeDropDown().fields['time_ranges'].choices
            initial_plot_selected = plots_types[0][0]
            initial_time_range_selected = time_ranges[0][0]
            plots_api.update_plot_selected(plots_object, initial_plot_selected)
            plots_api.update_time_range_selected(plots_object, initial_time_range_selected)

            plots_data = copy.deepcopy(plots_api.get_plots_data(plots_object))
            layout = plots_operations.plot_layout_by_time_range(plots_data, initial_plot_selected, initial_time_range_selected)
            if layout != 0:
                renderer = hv.renderer('bokeh')
                hvplot = renderer.get_plot(layout)
                hvplot.state
                charts_html = renderer._figure_data(hvplot, 'html')
            else:
                charts_html = "<p>No charts for this configuration...</p>"

        return HttpResponse(json.dumps({'charts_html': charts_html}), content_type='application/json')

    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')


def update_selected_chart(request):
    """ Update the selected chart

    Args:
        request:

    Returns:
    """
    try:
        plot_selected = request.POST.get('plot_selected', None)

        plots_object = plots_api.get_plots()
        plots_api.update_plot_selected(plots_object, plot_selected)
        time_range_selected = plots_api.get_time_range_selected(plots_object)

        plots_data = copy.deepcopy(plots_api.get_plots_data(plots_object))
        layout = plots_operations.plot_layout_by_time_range(plots_data, plot_selected, time_range_selected)
        if layout != 0:
            renderer = hv.renderer('bokeh')
            hvplot = renderer.get_plot(layout)
            hvplot.state
            charts_html = renderer._figure_data(hvplot, 'html')
        else:
            charts_html = "<p>No charts for this configuration...</p>"

        return HttpResponse(json.dumps({'charts_html': charts_html}), content_type='application/json')
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')


def update_time_range_chart(request):
    """ Update the time range for charts

    Args:
        request:

    Returns:

    """
    try:
        time_range_selected = request.POST.get('time_range_selected', None)

        plots_object = plots_api.get_plots()
        plots_api.update_time_range_selected(plots_object, time_range_selected)
        plot_selected = plots_api.get_plot_selected(plots_object)

        plots_data = copy.deepcopy(plots_api.get_plots_data(plots_object))
        layout = plots_operations.plot_layout_by_time_range(plots_data, plot_selected, time_range_selected)
        if layout != 0:
            renderer = hv.renderer('bokeh')
            hvplot = renderer.get_plot(layout)
            hvplot.state
            charts_html = renderer._figure_data(hvplot, 'html')
        else:
            charts_html = "<p>No charts for this configuration...</p>"

        return HttpResponse(json.dumps({'charts_html': charts_html}), content_type='application/json')
    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')
