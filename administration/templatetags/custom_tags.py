# Création de filters personnalisés pour les templates
from django import template

register = template.Library()

def equal_to_date(date_1, date_2):
    return date_1.date() == date_2.date()

register.filter('equal_to_date', equal_to_date)


def before_or_equal_date(date_1, date_2):
    return date_1.date() <= date_2.date()

register.filter('before_or_equal_date', before_or_equal_date)

def add_one_to_int(value):
    data = value+1
    return data

register.filter('add_one_to_int', add_one_to_int)