from django.contrib import admin
from .models import ZqUser
# from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule
from django.utils import timezone

import json
# # # Register your models here.



def create_periodic_task():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='0',
        day_of_week='1-5',  # Monday to Friday
    )
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Schedule Bonus',
        task='zqUsers.tasks.schedule_payments',
        start_time=timezone.now(),
    )

 
class ZQUserAdmin(admin.ModelAdmin):
    # Customize admin display, list filters, etc. as needed
     actions = [create_periodic_task]


admin.site.register(ZqUser, ZQUserAdmin)

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)
# admin.site.register(CrontabSchedule)
# admin.site.register(SolarSchedule)
# admin.site.register(ClockedSchedule)
