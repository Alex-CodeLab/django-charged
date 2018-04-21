# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from lightning import LightningRpc
from charged.api import Ln
from django.conf import settings

class Command(BaseCommand):
    help = 'lightning info'

    #def add_arguments(self, parser):
    #   parser.add_argument('command' , nargs='+', type=str)


    def handle(self, *args, **options):
        result = Ln().getinfo()
        print(result)

