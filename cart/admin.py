from django.contrib import admin
from .models import Discount, Order, OrderItem



# Filter for discount code status
class FilterByStatus(admin.SimpleListFilter):
    parameter_name = 'expired'
    title = 'expired'

    def lookups(self, request, model_admin):
        return (
            ('True','Expired'),
            ('False','Not expired'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(expired=self.value())




class OrderItemAdmin(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'order_total_price', 'paid')
    inlines = (OrderItemAdmin,)
    list_filter = ('client',)



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent', 'create_time', 'expired')
    list_filter = (FilterByStatus,)


