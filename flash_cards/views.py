from django.shortcuts import render,reverse
from django.utils import timezone
from django.db.models import Count

from flash_cards.models import Deck, Card, User, UserHistory, Comment


# Create your views here.

def index(request):
    """view for the main landing page - if a user is unregistered or not logged in, they will be prompted to do so
    for a registered user it will show a create deck button, a list of their decks, a list of favourited decks and a list of public decks"""

    if request.user.is_authenticated:
        # Fetch decks created by the authenticated user
        user_decks = Deck.objects.filter(creator=request.user).annotate(card_count=Count("card"))

        # Fetch public decks
        public_decks = Deck.objects.filter(public=True).annotate(card_count=Count("card"))

        # Fetch favourite decks for the user
        favourite_deck_ids = list(UserHistory.objects.filter(user=request.user, favourite=True).values_list('deck__id', flat=True))
        favourite_decks = Deck.objects.filter(id__in=favourite_deck_ids).annotate(card_count=Count("card"))

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
    card_deck = Deck.objects.get(id=deck_id)
    cards = Card.objects.filter(deck=card_deck)

    # Get the index of the card to display, default to 0 (first card) if not provided
    index = int(request.GET.get('index', 0))

    # Ensure the index is within the bounds of the cards list
    if index < 0 or index >= len(cards):
        index = 0

    # Get the specific card by index
    current_card = cards[index]

    # Calculate the next index
    next_index = index + 1 if index + 1 < len(cards) else 0

    context = {
        "deck": card_deck,
        "cards": cards,
        "current_card": current_card,
        "next_index": next_index,
    }

    return render(request, "flash_cards/deck.html", context)


def edit_deck(request, deck_id):
    """view for editing a deck, utilising the same template as creating a deck, but with the existing deck_id passed to populate it"""
    return render(request, "flash_cards/create_edit_deck.html", {"deck_id": deck_id})

def delete_deck(request, deck_id):
    """view for deleting a deck, with a confirmation message and a button to confirm the deletion"""
    return render(request, "flash_cards/index.html", {"deck_id": deck_id})

def add_card(request, deck_id):
    """view for adding a card to a deck, utilising the same template as editing a card, but with no existing card_id passed to populate it"""
    return render(request, "flash_cards/create_edit_card.html", {"deck_id": deck_id})

def edit_card(request, deck_id, card_id):
    """view for editing a card, utilising the same template as adding a card, but with the existing card_id passed to populate it"""
    return render(request, "flash_cards/create_edit_card.html", {"deck_id": deck_id, "card_id": card_id})

def delete_card(request, deck_id, card_id):
    """view for deleting a card, with a confirmation message and a button to confirm the deletion"""
    return render(request, "flash_cards/deck.html", {"deck_id": deck_id, "card_id": card_id})


def update_user_last_login(sender, user, **kwargs):
    """A reusable component to update the last login date of a user in the User model"""
    user.date_last_login = timezone.now()
    user.save()