from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Check if is valid the tutors crb"""
    
    def handle_noargs(self, **options):
        from apps.profile.utils import check_crb        
        check_crb()
        
        