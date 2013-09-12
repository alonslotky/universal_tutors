import autocomplete_light

from apps.profile.models import Genre

autocomplete_light.register(Genre, search_fields=('name',),
    )