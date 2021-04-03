# Generated by Django 3.1.6 on 2021-03-11 09:07

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('instagram_profile', '0003_auto_20210310_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='first_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='first_image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_url',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='post'),
        ),
    ]