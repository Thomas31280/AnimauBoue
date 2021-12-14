from django.core.management.base import BaseCommand, CommandError

from administration.models import Parks

class Command(BaseCommand):
    help = 'Populate Parks model, with initial values'

    def handle(self, *args, **options):
        
        try:
            for i in range(1, 11):
                if i <= 8:
                    Parks(name='E'+str(i), availability=False).save()
                else:
                    j = i-8
                    Parks(name='I'+str(j), availability=False).save()
            
            self.stdout.write(self.style.SUCCESS('Initialisation des parcs effectuée avec succès !'))
        
        except Exception:
            raise CommandError('Il semblerait que les parcs aient déjà été initialisés')
