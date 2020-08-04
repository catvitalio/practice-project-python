from django.db import migrations
import csv


def import_csv():
    from apps.eats.models import Ingredient
    try:
        objs = []
        with open('ingredients.csv') as csv_file:
            reader = csv.reader(csv_file)
            for column in reader:
                objs.append(Ingredient(
                    name=column[0],
                    calories=column[1],
                ))
        return objs
    except FileNotFoundError:
        print('CSV-файл ингредиентов не найден (server/ingredients.csv)')


def load_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('eats', 'Ingredient')
    objs = import_csv()
    Ingredient.objects.bulk_create(objs)


def delete_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('eats', 'Ingredient')
    objs = import_csv()
    Ingredient.objects.filter(name__in=objs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('eats', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_ingredients, delete_ingredients),
    ]
