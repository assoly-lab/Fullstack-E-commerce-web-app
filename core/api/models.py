from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from mptt.models import MPTTModel,TreeForeignKey
from django.utils import timezone
from django.core.validators import EmailValidator,MinValueValidator, MaxValueValidator
import uuid
import os
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('an email must be set')
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have staff privilege.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have superuser privilege ')
        self.create_user(email=email,password=password,**extra_fields)





class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name= models.CharField(max_length=35,blank=True)
    last_name= models.CharField(max_length=35,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)



    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('parent', 'name')




class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=1,blank=False,null=False)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)
    discount_start_date = models.DateTimeField(blank=True, null=True)
    discount_end_date = models.DateTimeField(blank=True, null=True)
    is_discounted = models.BooleanField(default=False) 
    main_image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.discount_start_date and self.discount_end_date:
            self.is_discounted = self.discount_start_date <= now <= self.discount_end_date
        else:
            self.is_discounted = False
        super().save(*args, **kwargs)

    def get_discounted_price(self):
        if self.is_discounted:
            if self.discount_price:
                return self.discount_price
            elif self.discount_percentage:
                return self.price * (1 - self.discount_percentage / 100.0)
        return self.price

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='carousel_images/',blank=True)
    alt_text = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Cart for {self.user.email}'



class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.first_name}'s cart"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"



class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    title = models.CharField(max_length=120)
    review = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Please provide a rating between 1 and 5."
    )
    image = models.ImageField(upload_to='review_images/',blank=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(validators=[EmailValidator],blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Field to store the date it was added


    def __str__(self):
        return f"{self.title} by {self.user or self.name}"

    def save(self, *args, **kwargs):
        if self.image:
            # Get the original image name
            original_image_name = self.image.name

            # Split the image name into name and extension
            image_name, extension = os.path.splitext(original_image_name)

            # Generate a new image name by appending a UUID to it
            new_image_name = f"{image_name}_{uuid.uuid4()}{extension}"

            # Set the new image name
            self.image.name = new_image_name

        # Call the parent's save method to continue saving the model instance
        super().save(*args, **kwargs)