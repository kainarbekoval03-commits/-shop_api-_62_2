from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='customuser',
            name='registration_source',
            field=models.CharField(default='web', max_length=20),
        ),
    ]
