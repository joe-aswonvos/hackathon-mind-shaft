from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Deck, Card, UserHistory, Comment

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)

class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'deck', 'favourite')
    list_filter = ('favourite',)

class DeckAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'public')
    list_filter = ('public',)

admin.site.register(User, UserAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Card)
admin.site.register(UserHistory, UserHistoryAdmin)
admin.site.register(Comment)