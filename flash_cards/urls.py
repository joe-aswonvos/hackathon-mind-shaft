from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_deck", views.create_deck, name="create_deck"),
    path("deck/<int:deck_id>/", views.deck, name="deck"),
    path("deck/<int:deck_id>/edit/", views.edit_deck, name="edit_deck"),
    path("deck/<int:deck_id>/delete/", views.delete_deck, name="delete_deck"),
    path("deck/<int:deck_id>/update_deck/", views.update_deck, name="update_deck"),
    path("deck/insert_deck/", views.insert_deck, name="insert_deck"),
    path("deck/<int:deck_id>/add_card/", views.add_card, name="add_card"),
    path("deck/<int:deck_id>/card/<int:card_id>/edit/", views.edit_card, name="edit_card"),
    path("deck/<int:deck_id>/card/<int:card_id>/delete/", views.delete_card, name="delete_card"),
]