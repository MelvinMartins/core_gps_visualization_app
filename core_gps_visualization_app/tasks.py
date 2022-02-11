""" Visualization tasks """
import logging
import time
from celery import shared_task

logger = logging.getLogger(__name__)


#TODO: Build visualization data every day at midnight
#@periodic_task(run_every=crontab(minute=0, hour=0))

@shared_task
def build_visualization_data():
    """

    Returns: list of charts with same x and y but different ids and data

    """
    try:
        start_time = time.time()
        logger.info("Periodic task: START creating plots objects")

        x_parameter = api.get_x_parameter()
        y_parameter = api.get_y_parameter()
        data_sources = api.get_data_sources()

        # TODO: FIX Chart optimization
        # if api.plots_exist(x_parameter, y_parameter, data_sources):
        #    list_of_charts = api.get_plots_data(x_parameter, y_parameter, data_sources)
        #    return list_of_charts

        all_data = utils.get_all_data()
        list_of_charts = parse_data(all_data, x_parameter, y_parameter, data_sources)

        # TODO: FIX Chart optimization
        # api.create_plots(list_of_charts, x_parameter, y_parameter, data_sources)

        logger.info("Periodic task: FINISH creating plots objects " +
                    "(" + str((time.time() - start_time) / 60) + "minutes)")

        return list_of_charts

    except Exception as e:
        logger.error("An error occurred while creating plots objects: " + str(e))

