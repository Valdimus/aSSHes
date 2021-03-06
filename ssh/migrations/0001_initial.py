# Generated by Django 2.2.2 on 2019-06-12 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ssh.hostbase_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnixUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ssh.unixuser_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='UserBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ssh.userbase_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('hostbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.HostBase')),
                ('fqdn', models.CharField(max_length=256, unique=True)),
                ('ip', models.CharField(max_length=100)),
                ('latest_seen', models.DateTimeField(verbose_name='Latest time host comes to get his keys')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.hostbase',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.UserBase')),
                ('login', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date')),
                ('revoked', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.userbase',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, unique=True)),
                ('tag_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssh.TagType')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ssh.HostBase')),
                ('unix_target', models.ManyToManyField(related_name='unix_target', to='ssh.UnixUser')),
                ('user_target', models.ManyToManyField(related_name='user_target', to='ssh.UserBase')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('userbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.UserBase')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('external', models.BooleanField(default=False)),
                ('members', models.ManyToManyField(related_name='members', to='ssh.UserBase')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.userbase',),
        ),
        migrations.CreateModel(
            name='UnixUserGroup',
            fields=[
                ('unixuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.UnixUser')),
                ('members', models.ManyToManyField(related_name='members', to='ssh.UnixUser')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.unixuser',),
        ),
        migrations.CreateModel(
            name='SSHKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256, unique=True)),
                ('sum_md5', models.CharField(max_length=256, unique=True)),
                ('sum_sha256', models.CharField(max_length=256, unique=True)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date')),
                ('validated', models.BooleanField(default=False)),
                ('selected', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ssh.User')),
            ],
        ),
        migrations.CreateModel(
            name='HostTag',
            fields=[
                ('hostbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.HostBase')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('tags', models.ManyToManyField(related_name='host_tags', to='ssh.Tag')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.hostbase',),
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('hostbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ssh.HostBase')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('members', models.ManyToManyField(related_name='members', to='ssh.HostBase')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('ssh.hostbase',),
        ),
    ]
