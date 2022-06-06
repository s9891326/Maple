import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from exchange.models import Product
from utils.util import get_two_days_ago

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=0, hours=22)
@sched.scheduled_job('interval', seconds=10)
def delete_time_out_product():
    logging.warning('Delete_time_out_product')
    # Product.objects.filter(update_date__lte=get_two_days_ago()).delete()

sched.start()
