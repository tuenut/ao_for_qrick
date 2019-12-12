from __future__ import absolute_import, unicode_literals

from celery import shared_task

from libs.killboard import KillBoardParser


@shared_task
def parse_kill_board_task():
    parser = KillBoardParser()
    parser.exec()
