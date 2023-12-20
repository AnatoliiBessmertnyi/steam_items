from django.contrib import admin
from .models import Item, ItemAddition

admin.site.register(Item)


class ItemAdditionAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(ItemAddition, ItemAdditionAdmin)
