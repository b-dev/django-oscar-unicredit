from django.contrib import admin
from unicredit.models import UnicreditTransactionLog

class UnicreditTransactionLogAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'order_number', 'statoprecedente', 'statoattuale', 'descrizione']

admin.site.register(UnicreditTransactionLog, UnicreditTransactionLogAdmin)