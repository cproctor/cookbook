# Generated by Django 2.1.3 on 2018-11-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0002_auto_20181102_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('servings', models.IntegerField()),
                ('recipes', models.ManyToManyField(related_name='menus', to='recipes.Recipe')),
            ],
            options={'ordering': ['name']},
        ),
    ]
