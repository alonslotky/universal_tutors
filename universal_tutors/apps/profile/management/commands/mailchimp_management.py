from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Mass payment of tutors"""
    
    def handle_noargs(self, **options):
        from apps.profile.models import UserProfile
        from django.conf import settings
        import mailchimp
        
        types = {
             UserProfile.TYPES.TUTOR: settings.TUTORS_LIST_ID,
             UserProfile.TYPES.STUDENT: settings.STUDENTS_LIST_ID,
             UserProfile.TYPES.PARENT: settings.PARENTS_LIST_ID,
             UserProfile.TYPES.UNDER16: settings.STUDENTS_LIST_ID,
        }
        
        for profile in UserProfile.objects.all():
            if profile.newsletters and profile.type in types.keys():
                try:
                    list = mailchimp.utils.get_connection().get_list_by_id(types.get(profile.type))
                    list.subscribe(profile.user.email, {'EMAIL': profile.user.email})
                except mailchimp.chimpy.chimpy.ChimpyException:
                    continue
            elif not profile.newsletters and profile.type in types.keys():
                try:
                    list = mailchimp.utils.get_connection().get_list_by_id(types.get(profile.type))
                    list.unsubscribe(profile.user.email)
                except mailchimp.chimpy.chimpy.ChimpyException:
                    continue