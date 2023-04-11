# Create your models here.
import pymysql
pymysql.install_as_MySQLdb()
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Authenticate(models.Model):
    p_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=15)
    user_type = models.CharField(max_length=30,choices=(("Customer","Customer"),("Manager","Manager"),("DeliveryPerson","DeliveryPerson")))

    class Meta:
        db_table="Authenticate"

class Address(models.Model):
    add_id = models.AutoField(primary_key=True,default=0)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    class Meta:
        db_table="Address"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    p_id = models.ForeignKey(Authenticate, on_delete=models.CASCADE)
    class Meta:
        db_table="Customer"

class CustAddress(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    add_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    class Meta:
        db_table="CustAddress"

class CustNos(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ph_no = models.CharField(max_length=255)

    class Meta:
        db_table="CustNos"

class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    p_id = models.ForeignKey(Authenticate, on_delete=models.CASCADE)
    #res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    
    class Meta:
        db_table="Manager"

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    addr_id = models.ForeignKey(Address,on_delete=models.CASCADE)
    man_id = models.ForeignKey(Manager,on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    
    class Meta:
        db_table="Restaurant"

class restPhNos(models.Model):
    restaurant_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    ph_no = models.CharField(max_length=255)

    class Meta:
        db_table="restPhNos"

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    addr_id=models.ForeignKey(Address,on_delete=models.CASCADE,default=0) 
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    ordered_on = models.DateTimeField(auto_now=True)
    status_val = models.CharField(max_length=255,choices=(("Processing","Processing"),("Out For Delivery","Out For Delivery"),("Delivered","Delivered")),default="Processing")


    class Meta:
        db_table="Orders"

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=255)

    class Meta:
        db_table="Product"

class orderProducts(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table="orderProducts"



class deliveryPersonnel(models.Model):
    personnel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    p_id = models.ForeignKey(Authenticate, on_delete=models.CASCADE)
    addr_id = models.ForeignKey(Address,on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    availability = models.CharField(max_length=255,choices=(("Delivering","Delivering"),("Available","Available")),default=("Available","Available"))

    class Meta:
        db_table="deliveryPersonnel"

class restaurantPersonnel(models.Model):
    personnel = models.ForeignKey(deliveryPersonnel,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    class Meta:
        db_table="RestaurantPersonnel"


class ManNos(models.Model):
    man_id = models.ForeignKey(Manager,on_delete=models.CASCADE)
    ph_no = models.CharField(max_length=255)

    class Meta:
        db_table="ManNos"        


class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    #statusId = models.ForeignKey(Status, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Orders, on_delete=models.CASCADE)
    personnelId = models.ForeignKey(deliveryPersonnel, on_delete=models.CASCADE)
    timeDispatch = models.DateTimeField(null=True)
    timeArrival = models.DateTimeField(null=True)

    class Meta:
        db_table="Delivery"

class Payment(models.Model):
    payId = models.AutoField(primary_key=True)
    payMode = models.CharField(max_length=100, choices=(("Cash","Cash"),("Card","Card")),default="Cash")
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE,default=0)
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE,default=0)
    payDate = models.DateTimeField()
    

    class Meta:
        db_table="Payment"


