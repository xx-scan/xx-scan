from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def get_redis_jobstores():
    jobstores = {
        'default': RedisJobStore(jobs_key='xpm_cron.jobs',
                                  run_times_key='xpm_cron.run_times',
                     host='192.168.2.227', port=6379, password='xxscan', db=11)
    }
    executors = {
        'default': ThreadPoolExecutor(100),
        'processpool': ProcessPoolExecutor(5)
    }
    scheduler = TornadoScheduler(jobstores=jobstores, executors=executors)
    return scheduler


from .db_context import get_db_url


def get_mysql_jobstores():
    scheduler = TornadoScheduler()
    scheduler.add_jobstore('sqlalchemy', url=get_db_url('default'))
    return scheduler


def get_django_scheduler():
    from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
    scheduler = TornadoScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    register_events(scheduler)
    return scheduler


# https://apscheduler.readthedocs.io/en/latest/userguide.html
def get_mongo_job_stores():
    from pytz import utc
    from apscheduler.jobstores.mongodb import MongoDBJobStore, MongoClient
    from apscheduler.executors.pool import ProcessPoolExecutor
    from ops.apscheduler.db_context import get_mongo_client

    client = get_mongo_client()

    jobstores = {
        'mongo': MongoDBJobStore(collection='job', database='apscheduler', client=client),
        'default': MongoDBJobStore(collection='job', database='apscheduler2', client=client),
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = TornadoScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    return scheduler
