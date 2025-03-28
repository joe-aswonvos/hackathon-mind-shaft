from django.shortcuts import render, get_object_or_404, redirect
from .models import Deck
from .forms import DeckForm
# Create your views here.


def index(request):
    return render(request, "flash_cards/index.html")


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
    return render(request, "flash_cards/create_edit_card.html")


def edit_card(request, deck_id, card_id):
    return render(request, "flash_cards/create_edit_card.html")


def delete_card(request, deck_id, card_id):
    return render(request, "flash_cards/deck.html")
