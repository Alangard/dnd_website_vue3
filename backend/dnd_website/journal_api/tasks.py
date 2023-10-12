# tasks.py

import time
from celery import Celery
from django.conf import settings
from .serializers import *
from django.utils.text import slugify
from dnd_website.celery import app


# # Создание экземпляра Celery
# app = Celery('postponed_publish', broker=settings.BROKER_URL)
# app = Celery('tasks', broker=broker_url, backend=redis_url)

@app.task
def postponed_publish(post_data):
    # Ваш код для выполнения функции test2 с аргументом post_data
    print(f"Executing test2 with post_data: {post_data}")

    time.sleep(3)
    print("test2 completed.")


    # change is_publish to True