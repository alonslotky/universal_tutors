from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Helps to close the classes"""
    
    def handle_noargs(self, **options):
        from apps.core.utils import update_currencies         
        update_currencies()
        
        