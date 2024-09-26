from django.core.management.base import BaseCommand
from DataGovCRUD.models import Location

class Command(BaseCommand):
    help = 'Remove duplicate Location entries'

    def handle(self, *args, **kwargs):
        seen = set()
        duplicates = []
        for location in Location.objects.all():
            identifier = (location.name, location.address)
            if identifier in seen:
                duplicates.append(location.id)
            else:
                seen.add(identifier)
        
        Location.objects.filter(id__in=duplicates).delete()
        self.stdout.write(self.style.SUCCESS(f'Removed {len(duplicates)} duplicate locations'))
