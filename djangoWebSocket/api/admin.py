from django.contrib import admin
from api.models import TransactionId


# Register your models here.
class TransactionIdAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TransactionId._meta.fields]


admin.site.register(TransactionId, TransactionIdAdmin)
