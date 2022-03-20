from decouple import config 
from pathlib import Path
import dj_database_url
import os






#############################################################
#######                                             #########
#######                  ROOT CONFIGS               #########
#######                                             #########
#############################################################
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = SECRET_KEY = config('SECRET_KEY')
DEBUG = True
SITE_ID = 1
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ivoire-soap.herokuapp.com']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WSGI_APPLICATION = 'soap.wsgi.application'
ROOT_URLCONF = 'soap.urls'
LOGIN_URL = 'login'
ADMINS = [
    ('Claver DIBY', 'claverdiby9@gmail.com'),
    ('Kiuv ABRAJ', 'kiuv.abraj@gmail.com'),
    ('Kiel HANS', 'kielhans07@gmail.com'),
]
STAFF = ['claverdiby9@gmail.com', 'kiuv.abraj@gmail.com', 'kielhans07@gmail.com']

SITE_NAME = 'Savon'


#############################################################
#######                                             #########
#######       INSTALLED APPLICATIONS DEFINITION     #########
#######                                             #########
#############################################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    
    
    
    # 3rd PARTY APPS
    'taggit',
    'ckeditor',
    'hitcount',
    'django_htmx',
    'star_ratings',
    'widget_tweaks',
    'import_export',
    'debug_toolbar',
    'django_countries',
    
    
    
    # LOCALE APPS
    'address.apps.AddressConfig',
    'administration.apps.AdministrationConfig',
    'blog.apps.BlogConfig',
    'contacts.apps.ContactsConfig',
    'coupons.apps.CouponsConfig',
    'faqs.apps.FaqsConfig',
    'newsletter.apps.NewsletterConfig',
    'orders.apps.OrdersConfig',
    'products.apps.ProductsConfig',
    'profils.apps.ProfilsConfig',
    'promotions.apps.PromotionsConfig',
    'refunds.apps.RefundsConfig',
    'reports.apps.ReportsConfig',
    'website.apps.WebsiteConfig',
    
]






#############################################################
#######                                             #########
#######             MIDDLEWARES                     #########
#######                                             #########
#############################################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Added
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',  # Added
    'django_htmx.middleware.HtmxMiddleware',  # Added
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Added
]







#############################################################
#######                                             #########
#######                 TEMPLATES                   #########
#######                                             #########
#############################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'soap.context_processors.site_name',  # Added
            ],
        },
    },
]





#############################################################
#######                                             #########
#######               DATABASES                     #########
#######                                             #########
#############################################################
# Databases on production
# DATABASES = {
#     'default': {
#         'ENGINE': config('DB_ENGINE'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'NAME': config('DB_NAME'),
#         'HOST': config('DB_HOST'),
#         'USER': config('DB_USER'),
#         'PORT': config('DB_PORT', cast=int),
#     }
# }

# Development databases
DATABASES = {
    'default': {
        'ENGINE': config('DEFAULT_DB_ENGINE'),
        'NAME': config('DEFAULT_DB_NAME'),
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)









#############################################################
#######                                             #########
#######             PASSWORD VALIDATORS             #########
#######                                             #########
#############################################################
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#############################################################
#######                                             #########
#######             INTERNATIONALIZATION            #########
#######                                             #########
#############################################################
LANGUAGE_CODE = 'fr-ci'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True







#############################################################
#######                                             #########
#######          STATIC & MEDIA FILES CONFIGS       #########
#######                                             #########
#############################################################
STATIC_URL = '/files/'
STATIC_ROOT = 'collectstatic/files/'

MEDIA_URL = 'soap/files/uploads/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'files/')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'files/soap/uploads')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'







#############################################################
#######                                             #########
#######                  EMAIL CONFIGS              #########
#######                                             #########
#############################################################
EMAIL_BACKEND = config('CONSOLE_EMAIL_BACKEND')  # default for now
# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_LOCALTIME = config('EMAIL_USE_LOCALTIME', cast=bool)








#############################################################
#######                                             #########
####### SESSION, PASSWORD, CACHES, COOKIES CONFIGS  #########
#######                                             #########
#############################################################
PASSWORD_RESET_TIMEOUT_DAYS = 1
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'CacheTable',
    }
}
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 365 * 24 * 60 * 60 # one year
SESSION_COOKIE_PATH = "/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False




#############################################################
#######                                             #########
#######           3rd PARTY APPS CONFIGS            #########
#######                                             #########
#############################################################




###############################################################
########             COUNTRIES CONFIGS            #############
###############################################################
COUNTRIES_FIRST = [
    'CI',
]



###############################################################
########         STAR RATINGS CONFIGS             #############
###############################################################
STAR_RATINGS_ANONYMOUS = False
STAR_RATINGS_STAR_WIDTH = 12
STAR_RATINGS_STAR_HEIGHT = 12



###############################################################
########          PHONE NUMBER CONFIGS            #############
###############################################################
PHONENUMBER_DEFAULT_REGION = 'CI'
PHONENUMBER_DB_FORMAT = 'NATIONAL'








###############################################################
########            XHTML2PDF CONFIGS             #############
###############################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'xhtml2pdf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}






CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
CKEDITOR_UPLOAD_PATH = os.path.join(
    BASE_DIR, 'files/soap/uploads/editors/')
CKEDITOR_BROWSE_SHOW_DIRS = True





