from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name

    @property
    def orders(self):
        order_count = self.order_set.all().count()
        return str(order_count)

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'pending'),
        ('Ongoing', 'ongoing'),
        ('Completed', 'completed'),
    )
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Pending')
    item = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='items')
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.customer.name} ordered {self.item.name}'
