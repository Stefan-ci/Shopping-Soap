# Generated by Django 4.0.3 on 2022-03-16 20:38

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre de la publication')),
                ('slug', models.SlugField(max_length=400, unique=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Réponse')),
                ('is_public', models.BooleanField(default=True, verbose_name='Public')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('website', models.CharField(blank=True, max_length=100, null=True, verbose_name='Site internet')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('content', models.TextField(verbose_name='Commentaire')),
                ('is_public', models.BooleanField(default=True, verbose_name='Public')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Poste')),
            ],
            options={
                'verbose_name': 'Commentaire',
                'verbose_name_plural': 'Commentaires',
                'ordering': ['-date'],
            },
        ),
    ]
