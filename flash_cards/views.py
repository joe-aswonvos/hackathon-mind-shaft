from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages

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
        favourite_deck_ids = list(
            UserHistory.objects.filter(user=request.user, favourite=True).values_list('deck__id', flat=True))
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
    return render(request, "flash_cards/create_deck.html")


def deck(request, deck_id):
    """view for a single deck, returning every card in the deck allowing the user to cycle between them"""
    card_deck = Deck.objects.get(id=deck_id)
    cards = Card.objects.filter(deck=card_deck)

    # Get the index of the card to display, default to 0 (first card) if not provided
    card_index = int(request.GET.get('index', 0))

    # Ensure the index is within the bounds of the cards list
    if card_index < 0 or card_index >= len(cards):
        card_index = 0

    # Get the specific card by index
    current_card = cards[card_index]

    # Calculate the next index
    next_index = card_index + 1 if card_index + 1 < len(cards) else 0

    context = {
        "deck": card_deck,
        "cards": cards,
        "current_card": current_card,
        "next_index": next_index,
    }

    return render(request, "flash_cards/deck.html", context)


def edit_deck(request, deck_id):
    """view for editing a deck, utilising the same template as creating a deck, but with the existing deck_id passed to populate it"""
    card_deck = Deck.objects.get(id=deck_id)
    return render(request, "flash_cards/edit_deck.html", {"deck": card_deck})


def update_deck(request, deck_id):
    """Push update to existing deck"""
    name = request.POST['name']
    keywords = request.POST['keywords']
    new_deck = Deck(name=name, keywords=keywords, creator=request.user)
    new_deck = get_object_or_404(Deck, id=deck_id)
    new_deck.name = name
    new_deck.keywords = keywords
    new_deck.creator = request.user
    new_deck.save()
    return render(request, "flash_cards/edit_deck.html", {"deck": new_deck})


def insert_deck(request):
    """Push update to existing deck"""
    name = request.POST['name']
    keywords = request.POST['keywords']
    new_deck = Deck(name=name, keywords=keywords, creator=request.user)
    new_deck.save()
    return render(request, "flash_cards/edit_deck.html", {"deck": new_deck})


def delete_deck(request, deck_id):
    """view for deleting a deck, with a confirmation message and a button to confirm the deletion"""
    # Get the deck instance or return a 404 if it doesn't exist
    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == "POST":
        # Delete the card
        deck.delete()

        # Return JSON response for fetch
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def add_card(request, deck_id):
    """view for adding a card to a deck, utilising the same template as editing a card, but with no existing card_id passed to populate it"""
    deck = get_object_or_404(Deck, id=deck_id)
    return render(request, "flash_cards/create_card.html", {"deck": deck})


def edit_card(request, deck_id, card_id):
    """view for editing a card, utilising the same template as adding a card, but with the existing card_id passed to populate it"""
    deck = get_object_or_404(Deck, id=deck_id)
    card = get_object_or_404(Card, id=card_id, deck_id=deck_id)
    return render(request, "flash_cards/edit_card.html", {"deck":deck, "card": card})


def update_card(request, deck_id, card_id):
    """Push update to existing deck"""
    name = request.POST['name']
    text = request.POST['text']
    question = request.POST['question']
    answers = request.POST['answers']
    new_card = get_object_or_404(Card, id=card_id, deck_id=deck_id)
    new_card.name = name
    new_card.text = text
    new_card.question = question
    new_card.answers = answers
    new_card.save()
    return render(request, "flash_cards/edit_card.html", {"deck": deck_id, "card": new_card})


def insert_card(request, deck_id):
    """Push update to existing deck"""
    deck = get_object_or_404(Deck, id=deck_id)
    name = request.POST['name']
    text = request.POST['text']
    question = request.POST['question']
    answers = request.POST['answers']
    new_card = Card(name=name, text=text, question_text=question, answers=answers, deck_id=deck_id)
    new_card.save()
    return render(request, "flash_cards/edit_card.html", {"deck": deck, "card": new_card})


def delete_card(request, deck_id, card_id):
    """view for deleting a card, with a confirmation message and a button to confirm the deletion"""
    # Get the deck instance or return a 404 if it doesn't exist
    card_deck = get_object_or_404(Deck, id=deck_id)

    # Make sure the card exists and belongs to the specified deck
    card = get_object_or_404(Card, id=card_id, deck=card_deck)

    if request.method == "POST":
        # Delete the card
        card.delete()

        # Return JSON response for fetch
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=400)


def update_user_last_login(sender, user, **kwargs):
    """A reusable component to update the last login date of a user in the User model"""
    user.date_last_login = timezone.now()
    user.save()
