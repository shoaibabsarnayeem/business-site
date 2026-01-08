from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True)

    def __str__(self):
        return self.name



from .models import Product

def products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})


from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class Order(models.Model):
    total = models.FloatField(default=0)  # IMPORTANT (see issue 2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()

    def subtotal(self):
        return self.qty * self.price