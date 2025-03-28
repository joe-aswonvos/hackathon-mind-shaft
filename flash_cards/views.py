from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count

from flash_cards.models import Deck, Card, User, UserHistory, Comment
from .forms import DeckForm

# Create your views here.


def index(request):
    """View for the main landing page - if a user is unregistered or not logged in, they will be prompted to do so.
    For a registered user, it will show a create deck button, a list of their decks, a list of favourited decks, and a list of public decks.
    """

    # Default values for unauthenticated users
    user_decks = []
    public_decks = []
    favourite_decks = []

    if request.user.is_authenticated:
        # Fetch decks created by the authenticated user
        user_decks = Deck.objects.filter(creator=request.user).annotate(card_count=Count("card"))

        # Fetch public decks
        public_decks = Deck.objects.filter(public=True).annotate(card_count=Count("card"))

        # Fetch favourite decks for the user
        favourite_deck_ids = list(UserHistory.objects.filter(user=request.user, favourite=True).values_list('deck__id', flat=True))
        favourite_decks = Deck.objects.filter(id__in=favourite_deck_ids).annotate(card_count=Count("card"))

    return render(
        request,
        "flash_cards/index.html",
        {"user_decks": user_decks, "public_decks": public_decks, "favourite_decks": favourite_decks},
    )


def create_deck(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.creator = request.user
            deck.save()
            return redirect('deck', deck_id=deck.id)
    else:
        form = DeckForm()

    return render(request, "flash_cards/create_edit_deck.html", {"form": form, "deck": None})


def deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    return render(request, "flash_cards/deck.html")


def edit_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == "POST":
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('deck', deck_id=deck.id)
    else:
        form = DeckForm(instance=deck)

    return render(request, "flash_cards/create_edit_deck.html", {"form": form, "deck": deck})


def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == "POST":
        deck.delete()
        return redirect('index')

    return render(request, "flash_cards/delete_deck.html", {"deck": deck})


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
