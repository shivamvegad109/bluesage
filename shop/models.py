from django.db import models
from author.models import AuthorProfile


class Category(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products')
    price = models.IntegerField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    streetaddress = models.CharField(max_length=100)
    streetaddress1 = models.CharField(max_length=100)
    towncity = models.CharField(max_length=100)
    postcodezip = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    emailaddress = models.CharField(max_length=100)
    total_price = models.IntegerField()
    items = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    payment_signature = models.CharField(max_length=100)
    payment_order_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # updated_at = models.DateTimeField(auto_now=True)