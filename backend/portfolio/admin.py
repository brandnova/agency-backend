from django.contrib import admin
from .models import Project, Purchase

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_paid', 'created_at', 'updated_at')
    list_filter = ('is_paid', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'tags')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'purchase_date', 'transaction_id')
    list_filter = ('purchase_date',)
    search_fields = ('user__username', 'project__title', 'transaction_id')