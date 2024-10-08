from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem,ProductImage
from mptt.admin import MPTTModelAdmin



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class ProductImageInline(admin.TabularInline): 
    model = ProductImage
    extra = 1


admin.site.register(Category,MPTTModelAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'main_image')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category',)
    inlines = [ProductImageInline]

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'alt_text',)
#     search_fields = ('product',)
#     list_filter = ('product',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)
    inlines = [CartItemInline]





@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__email', 'product__name')
    list_filter = ('cart', 'product')




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cost', 'status', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]





@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__user__email', 'product__name')
    list_filter = ('order', 'product')