from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "flash_cards/index.html")

def create_deck(request):
    return render(request, "flash_cards/create_edit_deck.html")

def deck(request, deck_id):
    return render(request, "flash_cards/deck.html")

def edit_deck(request, deck_id):
    return render(request, "flash_cards/create_edit_deck.html")

def delete_deck(request, deck_id):
    return render(request, "flash_cards/index.html")

def add_card(request, deck_id):
    return render(request, "flash_cards/create_edit_card.html")

def edit_card(request, deck_id, card_id):
    return render(request, "flash_cards/create_edit_card.html")

def delete_card(request, deck_id, card_id):
    return render(request, "flash_cards/deck.html")
