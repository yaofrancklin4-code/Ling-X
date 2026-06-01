#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category

print('Total categories:', Category.objects.count())
print('Categories:')
for cat in Category.objects.all().order_by('id'):
    print(f'ID {cat.id}: {cat.name}')
