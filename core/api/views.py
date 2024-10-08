from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import random
from rest_framework import status
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.shortcuts import get_object_or_404






class CategoryView(generics.ListAPIView):
    queryset = Category.objects.filter(level=0)
    serializer_class = CategorySerializer


# class ProductView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class CartView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


# class CartItemView(generics.ListAPIView):
#     serializer_class = CartItemSerializer

#     def get_queryset(self):
#         cart_id = self.kwargs.get('cart_id')
#         queryset = CartItem.objects.filter(cart_id=cart_id)
#         return queryset


class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = Order.objects.filter(user_id=user_id)
        return queryset


class OrderItemView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        queryset = OrderItem.objects.filter(order_id=order_id)
        return queryset



# class BestSellingView(APIView):
#     def get(self, request):
#         # Get all product IDs
#         product_ids = Product.objects.values_list('id', flat=True)
        
#         # Check if there are enough products to sample from
#         num_products = min(len(product_ids), 8)
        
#         # Generate 8 random IDs (or fewer if not enough products)
#         random_ids = random.sample(list(product_ids), num_products)

#         # Query the products with the selected random IDs
#         random_products = Product.objects.filter(id__in=random_ids)

#         # Serialize the products
#         serializer = ProductSerializer(random_products, many=True)

#         # Return the serialized data
#         return Response(serializer.data)




class BestSellingView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_ids = Product.objects.values_list('id', flat=True)
        num_products = min(len(product_ids), 8)
        random_ids = random.sample(list(product_ids), num_products)
        queryset = Product.objects.filter(id__in=random_ids)
        return queryset



class NewArrivalView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_ids = Product.objects.values_list('id', flat=True)
        num_products = min(len(product_ids), 8)
        random_ids = random.sample(list(product_ids), num_products)
        queryset = Product.objects.filter(id__in=random_ids)
        return queryset



class ProductQuickView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        queryset = Product.objects.filter(id=product_id)
        return queryset



class CartProductsListView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny,]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        product_ids = self.request.data.get('product_ids',[])
        print(product_ids)
        
        if not product_ids:
            return Response({"detail": "No product IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        
        products = Product.objects.filter(id__in=product_ids)
        products_dict = {product.id: product for product in products}
        ordered_products = [products_dict[product_id] for product_id in product_ids if product_id in products_dict]
        
        serializer = self.get_serializer(ordered_products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class SingleCategoryView(generics.ListAPIView):
    serializer_class = SingleCategorySerializer


    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = Category.objects.filter(id=category_id)
        return queryset




class ProductReviewSummaryView(generics.ListAPIView):
    queryset = ProductReview.objects.all()
    
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')

        # Fetch the product, or return 404 if it doesn't exist
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Initialize the response with 0 values for all ratings
        review_summary = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}


        # Group reviews by rating and count them
        number_of_reviews = ProductReview.objects.filter(product=product).count()
        print(number_of_reviews)
        reviews = ProductReview.objects.filter(product=product).values('rating').annotate(review_count=Count('rating')).order_by('-rating')

        if not reviews:
            return Response({'number_of_reviews': number_of_reviews,
            'reviews_by_rating': review_summary
        },status=status.HTTP_200_OK)
        
        # Create response format where rating is the key and count is the value
        for review in reviews:
            rating = review['rating']
            count = review['review_count']
            review_summary[rating] = count  # Use the rating as the key, and count as the value

        # Return the response in the desired format
        return Response({
            'number_of_reviews': number_of_reviews,
            'reviews_by_rating': review_summary
        },status=status.HTTP_200_OK)




class ProductReviewsView(generics.ListAPIView):

    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = ProductReview.objects.filter(product=product_id)
        return queryset



class ProductReviewCreateView(APIView):
    permission_classes = [AllowAny]  # Allow both authenticated and guest users to post reviews
    parser_classes = (MultiPartParser, FormParser)  # Enable parsing of multipart form data (file uploads)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')  # Get the product ID from the form data

        # Get the product object to create the review for
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()  # Copy the form data

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # For authenticated users, use the user's ID and ignore the name/email fields from the form
            data['user'] = request.user.id  # Set the user field to the authenticated user
            data['name'] = request.user.username  # Use the authenticated user's name
            data['email'] = request.user.email  # Use the authenticated user's email
        else:
            # For guest users, require name and email to be provided
            name = data.get('name')
            email = data.get('email')
            if not name or not email:
                return Response({"detail": "Name and email are required for guest users."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the review
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')

        if refresh_token:
            # Set the refresh token as a secure, HTTP-only cookie only for the '/api/auth/refresh' path
            response.set_cookie(
                'refresh_token', 
                refresh_token, 
                httponly=True,   # Set True in production for HTTPS
                samesite=None,
                path='/api/auth/jwt/refresh/',  # Only available for '/api/auth/jwt/refresh/' path
            )
            # Remove refresh token from the response body
            del response.data['refresh']

        return response



class LogoutView(APIView):

    def post(self, request):
        # If you want to blacklist the refresh token
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Clear the refresh token cookie
            response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token', path='/api/auth/refresh')
            return response
        
        except Exception as e:
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)





class CustomTokenRefreshView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from cookies
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token is None:
                print('it is null')
                return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                print('cookie is provided')
                # Create a new RefreshToken instance
                old_token = RefreshToken(refresh_token)

                user_id = old_token['user_id']
                user = CustomUser.objects.get(id=user_id)

                # Generate a new access and refresh token
                new_token = RefreshToken.for_user(user)
                access_token = str(new_token.access_token)
                new_refresh_token = str(new_token)
                print('new access token: ',access_token)
                print('new refresh token: ',new_refresh_token)
                # Optionally blacklist the old token if blacklisting is enabled
                old_token.blacklist()
                # Create a response with the new access token
                response = Response({
                    "access": access_token
                }, status=status.HTTP_200_OK)

                # Set the new refresh token in the cookie
                response.set_cookie(
                    key='refresh_token',
                    value=new_refresh_token,
                    httponly=True,
                    secure=False,  # Set to False if testing on local without HTTPS
                    samesite='Lax',
                    path='/api/auth/refresh/'
                )

                return response

            except InvalidToken:
                return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class CartCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if Cart.objects.filter(user=request.user).exists():
            return Response({"detail": "User already has a cart."}, status=status.HTTP_400_BAD_REQUEST)

        # If not, create a new cart for the user
        serializer = CartSerializer(data={}, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CartItemsCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # Check if the user already has a cart
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Get the cart items from the request (coming from localStorage)
        cart_items = request.data.get('cart_items', [])
        if not cart_items:
            return Response({'error': 'No cart items provided.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            
            # Validate quantity
            if quantity <= 0:
                return Response({'error': 'Quantity must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the product exists
            product = get_object_or_404(Product, id=product_id)

            # Check if a cart item with the same product and quantity already exists
            existing_cart_item = CartItem.objects.filter(cart=cart, product=product, quantity=quantity).first()
            if existing_cart_item:
                # If it exists, skip to the next item
                continue

            # Check if quantity is less than or equal to product stock
            if quantity <= product.stock:
                # Create or update CartItem for this product and cart
                try:
                    cart_item, created = CartItem.objects.update_or_create(
                        cart=cart,
                        product=product,
                        defaults={'quantity': quantity}
                    )
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Return an error if quantity exceeds available stock
                return Response({
                    'error': f"Not enough stock for {product.name}. Available stock: {product.stock}"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Cart items added successfully!'}, status=status.HTTP_200_OK)






class UserCartItemsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Get the user's cart
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        
        # Return the cart items for the user's cart
        if cart:
            return CartItem.objects.filter(cart=cart)
        return CartItem.objects.none()

    def list(self, request, *args, **kwargs):
        # If the cart doesn't exist or has no items, return an empty list
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            data = []
            for item in serializer.data:
                id = item.get('product')
                quantity = item.get('quantity')
                data.append({'id':id,'quantity':quantity})
            return Response(data,status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items in your cart.'}, status=status.HTTP_200_OK)



class UpdateUserCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def put(self, request, *args, **kwargs):
        user = request.user
        
        # Get or create a cart for the user
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Get the cart item data from the request
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        # Check if the product exists
        product = get_object_or_404(Product, id=product_id)

        # Check if the cart item already exists with the same product and quantity
        existing_cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if existing_cart_item:
            # If the quantity is the same, return a message
            if existing_cart_item.quantity == quantity:
                return Response({
                    'message': 'A cart item with the same product and quantity already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Update the quantity of the existing cart item
                existing_cart_item.quantity = quantity
                existing_cart_item.save()
                return Response({
                    'message': f'Item quantity updated successfully to {quantity}.'
                }, status=status.HTTP_200_OK)
        else:
            # Create a new cart item
            return Response({
                'message': 'Cart item does not exist!'}, status=status.HTTP_404_NOT_FOUND)






class SingleCartItemCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = [CartItemSerializer]  

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # Check if the user already has a cart
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Get the cart items from the request (coming from localStorage)
        cart_item = request.data.get('cart_item')
        if not cart_item:
            return Response({'error': 'No cart item provided.'}, status=status.HTTP_400_BAD_REQUEST)

        product_id = cart_item.get('id')
        quantity = cart_item.get('quantity')
            
            # Validate quantity
        if int(quantity) <= 0:
            return Response({'error': 'Quantity must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if the product exists
        product = get_object_or_404(Product, id=product_id)

        # Check if a cart item with the same product and quantity already exists
        existing_cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_cart_item:
            # If it exists, skip to the next item
            return Response({'error': 'A cart item already exist!'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if quantity is less than or equal to product stock
        if int(quantity) <= product.stock:
            # Create CartItem for this product and cart
            try:
                cart_item= CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return an error if quantity exceeds available stock
            return Response({
                'error': f"Not enough stock for {product.name}. Available stock: {product.stock}"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Cart items added successfully!'}, status=status.HTTP_200_OK)





class CategoryProductsListView(APIView):
    def get(self,request,category_id,*args,**kwargs):
        try:
            category = get_object_or_404(Category,id=category_id)
            child_categories = category.get_descendants(include_self=True)
            products = Product.objects.filter(category__in=child_categories)
            if not products.exists():
                return Response('No products found in the category or its subcategories!',status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(products,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response('something went wrong!',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class CategoryProductsCountView(generics.ListAPIView):
    serializer_class = CategoryProductsCountSerializer
    def get_queryset(self):
        categories = Category.objects.all()
        for category in categories:
            descendant_categories = category.get_descendants(include_self=True)
            product_count = Product.objects.filter(category__in=descendant_categories).count()
            category.product_count = product_count
        return categories
            



class ParentCategoriesListView(generics.ListAPIView):
    serializer_class = CategoryProductsCountSerializer
    def get_queryset(self):
        categories = Category.objects.filter(level=0)
        for category in categories:
            descendant_categories = category.get_descendants(include_self=True)
            product_count = Product.objects.filter(category__in=descendant_categories).count()
            category.product_count = product_count

        return categories