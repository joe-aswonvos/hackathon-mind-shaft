from django import forms
from .models import Deck


class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name', 'keywords', 'public', 'leitner', 'random']
