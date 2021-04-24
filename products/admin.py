from django.contrib import admin
from .models import Product,OrderedProduct,Order,CompanyOrder,ProductReview,ProductImage


class OrderAdmin(admin.ModelAdmin):
    list_display =['user','get_items','delivered','ordered','delivery_location','amount_paid','created_time']
    def get_items(self, obj):
        return "\n".join([str(p.item.name) + str( p.quantity) for p in obj.order_items.all()])

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(ProductReview)
admin.site.register(OrderedProduct)
admin.site.register(Order,OrderAdmin)
admin.site.register(CompanyOrder)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
# chai

