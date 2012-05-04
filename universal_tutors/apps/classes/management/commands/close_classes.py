from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Helps to close the classes"""
    
    def handle_noargs(self, **options):
        from apps.classes.utils import close_classes        
        close_classes()
        
        