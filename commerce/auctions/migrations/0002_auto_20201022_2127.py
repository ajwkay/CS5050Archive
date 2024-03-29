# Generated by Django 3.1.1 on 2020-10-22 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='listing',
        ),
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='listings',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='auctions.Comments'),
        ),
        migrations.AddField(
            model_name='listings',
            name='open',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listings',
            name='highest_bid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='listing', to='auctions.bids'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(null=True, related_name='watchlist', to='auctions.Listings'),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
