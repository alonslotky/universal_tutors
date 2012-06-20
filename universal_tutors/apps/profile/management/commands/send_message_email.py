from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Send emails notification of a new message"""
    
    def handle_noargs(self, **options):
        from apps.profile.utils import send_message_email        
        send_message_email()
        
        