# Generated by Django 2.2.2 on 2019-06-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('query_handler', models.CharField(max_length=250)),
                ('order', models.IntegerField(default=100)),
            ],
        ),
    ]