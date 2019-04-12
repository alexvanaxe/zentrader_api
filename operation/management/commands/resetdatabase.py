from django.core.management.base import BaseCommand
from operation.models import Operation, BuyData, SellData
from experience.models import ExperienceData
from notes.models import Note
from account.models import default_account
from learning.models import PaperBuy, PaperSell, PaperOperation


class Command(BaseCommand):
    """
    A command used to reset the development database to a consistent state.
    """
    help = 'Reset the database to a consistent state'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting the cleaning"))
        result = Note.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s notes" % (result)))
        result = PaperBuy.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s papers bougths" % (result)))
        result = PaperSell.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s papers solds" % (result)))
        result = PaperOperation.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s papers operations" % (result)))
        result = SellData.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s solds" % (result)))
        result = BuyData.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s boughts" % (result)))
        result = ExperienceData.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s experiences" % (result)))
        result = Operation.objects.all().delete()
        result = str(result)
        self.stdout.write(self.style.NOTICE("Deleted %s operations" % (result)))

        account = default_account()
        account.equity = 10000
        account.save()
        self.stdout.write(self.style.NOTICE("Equity updated to 10000"))
