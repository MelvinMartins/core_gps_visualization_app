""" Visualization tasks """
import logging
import copy
import time
import holoviews as hv
from celery import shared_task

from core_gps_visualization_app.components.plots import api as plots_api
from core_gps_visualization_app.components.data import operations

logger = logging.getLogger(__name__)


#@periodic_task(run_every=crontab(minute=0, hour=0))
@shared_task
def build_visualization_data():
    """Build visualization data every day at midnight"""
    try:

        start_time = time.time()
        logger.info("Periodic task: START creating plots objects")

        all_parsed_data = operations.get_all_data()
        all_parsed_data = operations.parse_all_data(all_parsed_data)
        plots_object = plots_api.create_and_get_plots(all_parsed_data)
        plots_api.update_completed(plots_object)

        logger.info("Periodic task: FINISH creating plots objects " +
                    "(" + str((time.time() - start_time)/60) + "minutes)")
    except Exception as e:
        logger.error("An error occurred while creating plots objects")
