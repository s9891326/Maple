import logging

from apscheduler.schedulers.blocking import BlockingScheduler

import django

from Maple.settings import base

django.setup()

from exchange.models import Product
from utils.util import get_one_week_ago

sched = BlockingScheduler(timezone=base.TIME_ZONE)


@sched.scheduled_job('cron', hour='0', minute='0', second='0')
def delete_time_out_product():
    logging.warning('Delete_time_out_product: %s', get_one_week_ago())
    Product.objects.filter(update_date__lte=get_one_week_ago()).delete()


sched.start()
