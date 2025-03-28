# Generated by Django 5.1.7 on 2025-03-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0002_alter_card_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhistory',
            name='last_score',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='comments_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
