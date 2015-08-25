from django.contrib import admin

from django.contrib.sessions.models import Session
from .models import User, Bill, Transaction, Contact

class TransactionInline(admin.TabularInline):
    model = Transaction
    
class BillAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]

admin.site.register(User)
admin.site.register(Bill, BillAdmin)
admin.site.register(Contact)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)