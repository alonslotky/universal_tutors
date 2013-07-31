from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Alert tutors and students that their class is about to start"""
    
    def handle_noargs(self, **options):
        from apps.classes.utils import alert_classes        
        alert_classes()
        
        