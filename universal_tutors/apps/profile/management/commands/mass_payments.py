from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Mass payment of tutors"""
    
    def handle_noargs(self, **options):
        from apps.profile.utils import mass_payments        
        mass_payments()
        
        