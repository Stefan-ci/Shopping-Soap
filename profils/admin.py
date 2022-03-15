from django.contrib import admin
from profils.models import Profile
from import_export.admin import ImportExportModelAdmin




class ProfileAdmin(ImportExportModelAdmin):
    list_display = ['user', 'phone_number', 'is_dev', 'is_dispatcher', 'signup_ip',
        'last_login_ip']
    list_filter = ['is_dispatcher', 'date_joined', 'is_dev']
    search_fields = ['user__username', 'phone_number', 'signup_ip', 'last_login_ip']
    
    date_hierarchy = 'date_joined'


admin.site.register(Profile, ProfileAdmin)
