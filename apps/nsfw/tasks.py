import logging
import random
import uuid

from celery import shared_task
from celery.utils.log import get_task_logger

_LOGGER = get_task_logger(__name__)


def _new_post():
    post_id = str(uuid.uuid4())
    return {
        'id': post_id,
        'title': f'post title #{post_id[:8]}'
    }


@shared_task(
    acks_late=True
)
def task_generate_new_post():
    num_of_posts = random.randint(0, 5)

    for _ in range(num_of_posts):
        post = _new_post()
        _LOGGER.info('post id: %s', post['id'])
