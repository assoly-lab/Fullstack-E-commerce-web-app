from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import (CustomUser,Product,ProductImage,Cart,ProductReview,
CartItem,Order,OrderItem,Category)
from rest_framework import serializers




class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id','email','first_name','last_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id','email','first_name','last_name')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email','first_name','last_name')


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ('id','name','description','price','stock','main_image','images','category','created_at')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [ 'product', 'quantity']

    def validate_quantity(self, value):
        # Get the product ID from the request data
        product_id = self.initial_data['product']

        # Fetch the actual Product object
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        # Check if the requested quantity exceeds the available stock
        if value > product.stock:
            raise serializers.ValidationError(f"Only {product.stock} items in stock.")

        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)

    class Meta:
        model = Cart
        fields = ('id','user','items')



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id','product','quantity','price')




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ('id','user','items','total_cost','status','created_at')


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = obj.get_children()
        if children:
            return CategorySerializer(children, many=True).data
        return None
        
    class Meta:
        model = Category
        fields = ('id','name','description','image','children')





class SingleCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id','name','description','image',)



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductReview
        fields = ['id', 'product', 'user', 'title', 'review', 'image', 'name', 'rating','created_at']
        extra_kwargs = {
            'user': {'required': False},
        }



class CategoryProductsCountSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    
    class Meta:
        model = Category
        fields =('id','name','description','image','product_count')
        
