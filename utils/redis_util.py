from redis import StrictRedis

import config

rds = StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db, password=config.redis_password)
