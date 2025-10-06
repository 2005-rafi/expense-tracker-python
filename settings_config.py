# settings_config.py

import os
from django.conf import settings
from django.utils.crypto import get_random_string

def configure_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY=get_random_string(50),
            ROOT_URLCONF="backend",
            ALLOWED_HOSTS=['*'],
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'rest_framework',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'expense_tracker.sqlite3',
                }
            },
            REST_FRAMEWORK={
                'DEFAULT_PERMISSION_CLASSES': [],
                'UNAUTHENTICATED_USER': None,
            },
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            }],
        )

    import django
    django.setup()
