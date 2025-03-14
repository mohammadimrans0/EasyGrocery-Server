from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    class Role(models.TextChoices):
        BUYER = 'buyer', 'Buyer'
        SELLER = 'seller', 'Seller'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True, default="")
    image = CloudinaryField("image", folder="easygrocery/user", default="https://res.cloudinary.com/dzuro3ezl/image/upload/v1739781463/easygrocery/user/avatar_qpkqzn.png")
    contact_info = models.CharField(max_length=255, blank=True, default="")
    shopping_preferences = models.TextField(blank=True, default="")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    

