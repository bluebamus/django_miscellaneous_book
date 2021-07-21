from django.contrib import admin
from ..models_ex.models_signal_login_ip_logging import UserLoginLog


# Register your models here.
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ip_address",
        "user_agent",
    )
    list_filter = ("ip_address",)
    date_hierarchy = "created"


admin.site.register(UserLoginLog, UserLoginLogAdmin)
