import os

from django.core.management.base import BaseCommand
from django.conf import settings

from sss_server.sss.poller import Poller
class Command(BaseCommand):

    def handle(self, *args, **options):
        poller = Poller()
        poller.start()
