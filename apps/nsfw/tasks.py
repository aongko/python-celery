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

        task_classify_nsfw.delay(post)


class RetryableError(Exception):
    pass


def classify_nsfw(title):
    # load_model()
    # model.predict()
    if random.randint(1, 100) < 20:
        # simulate 20% error rate
        raise RetryableError('oops, something bad happened, please retry.')
    if set('cdf').intersection(set(title)):
        # pretend that it's NSFW if the title contains one of the letters 'xyz'.
        return True
    return False


@shared_task(
    acks_late=True,
    autoretry_for=(RetryableError,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=600,
    time_limit=30,
)
def task_classify_nsfw(post):
    post_id = post.get('id', '')
    if not post_id:
        return

    title = post.get('title', '')
    if not title:
        return

    try:
        is_nsfw = classify_nsfw(title)
    except RetryableError:
        _LOGGER.exception('Failed to classify NSFW for post %s', post_id)
        raise

    # do something with the result, i.e. save to database
    _LOGGER.info('post "%s" NSFW result: %s', post_id, is_nsfw)
    return is_nsfw
