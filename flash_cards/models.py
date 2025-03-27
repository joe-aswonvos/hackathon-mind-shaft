from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
"""
The models required for the flash cards app are:
1. User - A user model to store the user details
2. Deck - A deck of flash cards
3. Card - A flash card
4. UserHistory - A model of the users history for a given deck
5. Comment - A model to store the comments for a given card"""
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model to store the user details - basic identifiers, plus datetimes of login and registration
    """
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    date_registered = models.DateTimeField(auto_now_add=True)
    date_last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Deck(models.Model):
    """
    Deck model to store the deck details - deck name, date created and date edited, a list of the order of cards, a list of keywords
    and boolean values for public, whether a deck is Leitner and whether the deck should be randomisable
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    order = models.TextField(blank=True)
    keywords = models.TextField()
    public = models.BooleanField(default=False)
    leitner = models.BooleanField(default=False)
    random = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Card(models.Model):
    """
    Card model to store the card details, a foreign key of the deck the card belongs to, a cardname, an optional card_image url, text for the card, an optional hidden
    text field, a boolean of whether the card will have a question, a question text field, a dictionary of answers and a boolean on whether comments are enabled for that card
    """
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    card_image = models.URLField(blank=True)
    text = models.TextField()
    hidden_text = models.TextField(blank=True)
    question = models.BooleanField(default=False)
    question_text = models.TextField(blank=True)
    answers = models.JSONField(blank=True)
    comments_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserHistory(models.Model):
    """
    UserHistory model to store the users history for a given deck, a foreign key of the user, a foreign key of the deck, date created, date last accessed, the first score achieved (optional)
    , the max score achieved (optional), a dictionary of leitner values(optional) and a boolean of whether the deck has been flagged as a favourite
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_accessed = models.DateTimeField(auto_now=True)
    first_score = models.IntegerField(blank=True)
    last_score = models.IntegerField(blank=True, default=0)
    max_score = models.IntegerField(blank=True)
    leitner_values = models.JSONField(blank=True)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.deck.name + " - " + self.user.username


class Comment(models.Model):
    """
    Comment model to store the comments for a given card, a foreign key of the card, a foreign key of the user, the date created, the date edited, a title and a comment
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    comment = models.TextField()

    def __str__(self):
        return self.title
