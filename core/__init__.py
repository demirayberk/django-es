from .celery import app as celery_app # pyright: ignore

__all__ = ['celery_app']
