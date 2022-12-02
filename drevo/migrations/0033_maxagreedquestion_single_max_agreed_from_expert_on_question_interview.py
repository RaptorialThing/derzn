# Generated by Django 3.2.4 on 2022-11-30 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drevo', '0032_auto_20221130_0005'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='maxagreedquestion',
            constraint=models.UniqueConstraint(fields=('interview', 'question', 'author'), name='single_max_agreed_from_expert_on_question_interview'),
        ),
    ]
