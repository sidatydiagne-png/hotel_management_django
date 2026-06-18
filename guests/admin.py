from django.contrib import admin
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'nationality', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'id_number']
    list_filter = ['nationality', 'country']
