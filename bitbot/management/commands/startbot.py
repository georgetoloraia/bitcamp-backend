from django.core.management.base import BaseCommand

from ... import bot

class Command(BaseCommand):
    help = 'Starts the Discord bot'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the Discord bot...')
        bot.start()  # Call the main function of your bot




