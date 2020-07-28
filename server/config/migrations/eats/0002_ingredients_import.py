from django.db import migrations
import csv


def load_ingredients(apps, schema_editor):
    try:
        Ingredient = apps.get_model('eats', 'Ingredient')
        with open('ingredients.csv') as csv_file:
            reader = csv.reader(csv_file)
            for column in reader:
                created = Ingredient.objects.update_or_create(
                    name=column[0],
                    calories=column[1],
                )
    except FileNotFoundError:
        print('CSV-файл ингредиентов не найден (server/ingredients.csv)')


class Migration(migrations.Migration):
    dependencies = [
        ('eats', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_ingredients),
    ]
