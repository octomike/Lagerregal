# Generated by Django 1.9.4 on 2016-04-29 16:38
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_lageruser_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lageruser',
            name='theme',
            field=models.CharField(choices=[('default', 'default'), ('darkly', 'darkly'), ('simplex', 'simplex'), ('superhero', 'superhero'), ('united', 'united')], default='default', max_length=50),
        ),
    ]
