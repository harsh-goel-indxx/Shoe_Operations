from django.db import models


class PackingChoice(models.TextChoices):
            LOOSE = "loose", "Loose"
            BOX   = "box",   "Box"
            CHINA = "china", "China Packing"

            
# Create your models here.
class Party_Master(models.Model):
    name = models.CharField(max_length=50)
    whatsapp_number = models.CharField(max_length=15)
    transport = models.CharField(max_length=50, null=True, blank=True)
    marka = models.CharField(max_length=50, null=True, blank=True)
    station = models.CharField(max_length=50, null=True, blank=True)


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Sub_Party_Master(models.Model):
    name = models.CharField(max_length=50)
    parent_party = models.ForeignKey(to=Party_Master, on_delete=models.CASCADE, related_name="sub_parties")
    transport = models.CharField(max_length=50)
    marka = models.CharField(max_length=50)
    station = models.CharField(max_length=50)


class Product_Master(models.Model):
    name = models.CharField(max_length=50)
    size_max = models.IntegerField()
    size_min = models.IntegerField()
    color = models.ManyToManyField(Color, blank=True)
    # category = models.CharField()
    packing = models.CharField(max_length = 50, choices=PackingChoice.choices)
    opening_balance = models.IntegerField(blank=True, null=True)


class Orders(models.Model):
    date = models.DateField(auto_now_add=True)
    party = models.ForeignKey(Party_Master, on_delete=models.CASCADE)
    sub_party = models.ForeignKey(Sub_Party_Master, on_delete=models.CASCADE, blank=True, null=True)
    transport = models.CharField(max_length=50)
    marka = models.CharField(max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product_Master, on_delete=models.CASCADE)
    size_max = models.IntegerField()
    size_min = models.IntegerField()
    color = models.ManyToManyField(Color, blank=True)
    # category = models.CharField()
    quantity = models.IntegerField()
    packing = models.CharField(max_length = 50, choices=PackingChoice.choices)
