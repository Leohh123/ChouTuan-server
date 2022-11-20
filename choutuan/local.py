SECRET_KEY = 'django-insecure-6vc@m$en!#elzarjc7!=(sd-((lp5aw_i=)ujxupewpi7^cqkm'
DEBUG = True


def DATABASES(base_dir):
    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_dir / 'db.sqlite3',
        }
    }
