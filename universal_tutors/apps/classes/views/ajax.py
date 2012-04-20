from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User

from apps.profile.models import NewsletterSubscription
from apps.profile.forms import *
from apps.common.utils.view_utils import main_render, handle_uploaded_file

try:
    import simplejson
except ImportError:
    from django.utils import simplejson

@login_required
@main_render('profile/iframes/change_photo.html')
def change_photo(request):

    form = ProfilePhotoForm(request.POST or None, request.FILES or None)

    success = False
    error_message = ''

    photo = ''

    if request.method == 'POST' and form.is_valid():
        user = request.user
        profile = user.profile

        f, filename = handle_uploaded_file(request.FILES['photo'], 'uploads/profiles/profile_images')

        profile.profile_image = 'uploads/profiles/profile_images/' + filename
        profile.save()

        success = True

        photo = profile.get_profile_image_path()

    return {
        'success': success,
        'form': form,
        'photo': photo,
    }
