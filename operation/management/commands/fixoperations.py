from django.core.management.base import BaseCommand
from operation.models import Operation


class Command(BaseCommand):
    """
    A command class to adjust the operations to make more of the performance
    optimizations
    """
    help = 'Fix the issues with the operations'

    def handle(self, *args, **options):
        operations_to_fix = Operation.objects.filter(category='NA')

        for operation in operations_to_fix:
            category_to_update = operation.operation_category()

            if category_to_update != 'DT':
                self.stdout.write(self.style.NOTICE("Changing category of operation %s, from %s to %s" % (operation.stock.code, operation.category, category_to_update)))
                operation.category = category_to_update
                operation.save()
                self.stdout.write(self.style.SUCCESS("Operation Updated"))
            elif operation.executed:
                self.stdout.write(self.style.NOTICE("Changing category of operation %s, from %s to %s" % (operation.stock.code, operation.category, category_to_update)))
                operation.category = category_to_update
                operation.save()
                self.stdout.write(self.style.SUCCESS("Operation Updated"))

            else:
                self.stdout.write(self.style.WARNING("Not updating %s from %s to %s because is not executed and can be daytrade or not." %(operation.stock.code, operation.creation_date, category_to_update)))

        if len(operations_to_fix) > 0:
            self.stdout.write(self.style.SUCCESS("All operations sucessful updated"))
        else:
            self.stdout.write(self.style.WARNING("There was none operations to update"))


