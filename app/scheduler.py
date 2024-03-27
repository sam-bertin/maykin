from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command

_scheduler = None  # Ajoutez cet attribut global


def start_scheduler():
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        print("APScheduler is already running")
        return

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        import_city_and_hotel_data_command,
        trigger=CronTrigger(minute='*/5'),
        id='import_data_job',
        replace_existing=True,
        misfire_grace_time=3600,
    )
    _scheduler.start()


def stop_scheduler():
    global _scheduler  # Utilisez l'attribut global
    if _scheduler is None or not _scheduler.running:
        print("APScheduler is not running")
    else:
        for job in _scheduler.get_jobs():
            _scheduler.remove_job(job.id)
        _scheduler.shutdown()
        print("APScheduler stopped")


def import_city_and_hotel_data_command():
    call_command('import_city_and_hotel_data')


if __name__ == '__main__':
    start_scheduler()
