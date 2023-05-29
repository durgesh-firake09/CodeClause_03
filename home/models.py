from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"


class Payment(models.Model):
    tid = models.IntegerField(primary_key=True)
    cust_email = models.EmailField(max_length=50)
    amount = models.FloatField()
