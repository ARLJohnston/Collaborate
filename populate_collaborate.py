import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'collab_app.settings')

import django
django.setup()

def populate():
    pass

if __name__ == '__main__':
    print('Starting population script...')
    populate()