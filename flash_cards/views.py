from django.shortcuts import render
from django.utils import timezone

from flash_cards.models import Deck, Card, User, UserHistory, Comment


# Create your views here.

def index(request):
    """view for the main landing page - if a user is unregistered or not logged in, they will be prompted to do so
    for a registered user it will show a create deck button, a list of their decks, a list of favourited decks and a list of public decks"""

    if request.user.is_authenticated:
        # Fetch decks created by the authenticated user
        user_decks = list(Deck.objects.filter(creator=request.user).values_list('id', flat=True))

        # Fetch public decks
        public_decks = list(Deck.objects.filter(public=True).values_list('id', flat=True))

        # Fetch favourite decks for the user
        favourite_decks = list(
            UserHistory.objects.filter(user=request.user, favourite=True)
            .values_list('deck__id', flat=True)
        )
    else:
        user_decks = []
        public_decks = []
        favourite_decks = []

    return render(
        request,
        "flash_cards/index.html",
        {"user_decks": user_decks, "public_decks": public_decks, "favourite_decks": favourite_decks},
    )


def create_deck(request):
    """view for creating a new deck, utilising the same template as editing a deck, but with no existing deck_id passed to populate it"""
    return render(request, "flash_cards/create_edit_deck.html")

def deck(request, deck_id):
    """view for a single deck, returning every card in the deck allowing the user to cycle between them"""
    return render(request, "flash_cards/deck.html")

def edit_deck(request, deck_id):
    """view for editing a deck, utilising the same template as creating a deck, but with the existing deck_id passed to populate it"""
    return render(request, "flash_cards/create_edit_deck.html")

def delete_deck(request, deck_id):
    """view for deleting a deck, with a confirmation message and a button to confirm the deletion"""
    return render(request, "flash_cards/index.html")

def add_card(request, deck_id):
    """view for adding a card to a deck, utilising the same template as editing a card, but with no existing card_id passed to populate it"""
    return render(request, "flash_cards/create_edit_card.html")

def edit_card(request, deck_id, card_id):
    """view for editing a card, utilising the same template as adding a card, but with the existing card_id passed to populate it"""
    return render(request, "flash_cards/create_edit_card.html")

def delete_card(request, deck_id, card_id):
    """view for deleting a card, with a confirmation message and a button to confirm the deletion"""
    return render(request, "flash_cards/deck.html")


def update_user_last_login(sender, user, **kwargs):
    """A reusable component to update the last login date of a user in the User model"""
    user.date_last_login = timezone.now()
    user.save()