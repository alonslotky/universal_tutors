from django import forms
from autocomplete_light import MultipleChoiceWidget,ChoiceWidget, TextWidget
from apps.profile.models import Genre

class SearchForm(forms.Form):
    subject = forms.ModelMultipleChoiceField(Genre.objects.all(), widget=MultipleChoiceWidget('GenreAutocomplete'))