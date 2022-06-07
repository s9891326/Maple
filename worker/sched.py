import logging

from apscheduler.schedulers.blocking import BlockingScheduler

import django

django.setup()

from exchange.models import Product
from utils.util import get_two_days_ago

sched = BlockingScheduler()


# @sched.scheduled_job('interval', seconds=10)
# @sched.scheduled_job('interval', minutes=10, hours=14)
@sched.scheduled_job('cron', second='*/10')
# @sched.scheduled_job('cron', hour='14', minute='53', second='0')
def delete_time_out_product():
    logging.warning('Delete_time_out_product: %s', get_two_days_ago())
    # Product.objects.filter(update_date__lte=get_two_days_ago()).delete()


sched.start()
