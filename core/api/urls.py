from django.urls import path,include
from .views import *

urlpatterns = [
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/logout/', LogoutView.as_view(), name='jwt-logout'),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),


    path('categories/', CategoryView.as_view() ),
    path('products/', ParentCategoriesListView.as_view() ),


    path('orders/<int:user_id>/', OrderView.as_view() ),
    path('order-items/<int:order_id>/', OrderItemView.as_view() ),



    path('cart/', CartProductsListView.as_view() ),
    path('create/cart/', CartCreateView.as_view() ),
    path('create/cartitems/', CartItemsCreateView.as_view() ),
    path('create/cartitem/', SingleCartItemCreateView.as_view() ),
    path('update/cartitem/', UpdateUserCartItemView.as_view() ),
    path('list/cartitems/', UserCartItemsListView.as_view() ),


    # path('cart-items/<int:cart_id>/', CartItemView.as_view() ),
    path('best-selling/', BestSellingView.as_view() ),
    path('new-arrival/', NewArrivalView.as_view() ),
    path('product/<int:product_id>/', ProductQuickView.as_view() ),

    path('category/<int:category_id>/', SingleCategoryView.as_view() ),
    path('category/<int:category_id>/products/', CategoryProductsListView.as_view() ),
    path('category/count/', CategoryProductsCountView.as_view() ),

    path('productreviewsummary/<int:product_id>/', ProductReviewSummaryView.as_view() ),


    path('productreviews/<int:product_id>/', ProductReviewsView.as_view() ),
    path('submitreview/', ProductReviewCreateView.as_view() ),
]


