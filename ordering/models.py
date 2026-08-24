from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    allowance_used = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    @property

    def available_balance(self):
        return self.monthly_allowance - self.allowance_used

    def __str__(self):
        return f"{self.user.username} - R{self.available_balance} available"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.employee.user.username}"