# Generated by Django 2.2.4 on 2019-09-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MendelienDatabase', '0003_auto_20190915_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='mendeliengene',
            name='IsInheritanceKnown',
            field=models.BooleanField(default=True),
        ),
    ]
