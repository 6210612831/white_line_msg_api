from django.contrib import admin

from message_api.models import Account, Audience
from .views import *

# Register your models here.
admin.site.register(Audience)
admin.site.register(Account)