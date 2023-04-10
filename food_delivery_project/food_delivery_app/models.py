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

   
# class Products(models.Model):
#     itemId = models.AutoField(primary_key=True)
#     restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     price = models.IntegerField()
#     description = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     class Meta:
#         db_table="Products"


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    ordered_on = models.DateTimeField(auto_now=True)
    status_val = models.CharField(max_length=255,choices=(("Processing","Processing"),("Out For Delivery","Out For Delivery"),("Delivered","Delivered")),default="Processing")


    class Meta:
        db_table="Orders"

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_val = models.CharField(max_length=255,choices=(("Processing","Processing"),("Out For Delivery","Out For Delivery"),("Delivered","Delivered")),default="Processing")

    class Meta:
        db_table="Status"

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
    item_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table="orderProducts"


class Category(models.Model):
    Category_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    class Meta:
        db_table="Category"

class Product_categ(models.Model):
    prod_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE)

class deliveryPersonnel(models.Model):
    personnel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    p_id = models.ForeignKey(Authenticate, on_delete=models.CASCADE)
    addr_id = models.ForeignKey(Address,on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    #availability = models.CharField(max_length=255,choices=(("Delivering","Delivering"),("Available","Available")))

    class Meta:
        db_table="deliveryPersonnel"

class availability(models.Model):
    personnel = models.ForeignKey(deliveryPersonnel,on_delete=models.CASCADE)
    availability = models.CharField(max_length=255,choices=(("Delivering","Delivering"),("Available","Available")))
    class Meta:
        db_table="Availability"




# class RestAddress(models.Model):
#     rest_add_id = models.AutoField(primary_key=True)
#     restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     add_id = models.ForeignKey(Address,on_delete=models.CASCADE)

#     class Meta:
#         db_table="RestAddress"



class ManNos(models.Model):
    man_id = models.ForeignKey(Manager,on_delete=models.CASCADE)
    ph_no = models.CharField(max_length=255)

    class Meta:
        db_table="ManNos"        

# class personnelAddr(models.Model):
#     personnel_id = models.ForeignKey(deliveryPersonnel, on_delete=models.CASCADE)
#     add_id = models.ForeignKey(Address,on_delete=models.CASCADE)

#     class Meta:
#         db_table="personnelAddr"


class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    #statusId = models.ForeignKey(Status, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Orders, on_delete=models.CASCADE)
    personnelId = models.ForeignKey(deliveryPersonnel, on_delete=models.CASCADE)
    timeDispatch = models.DateTimeField(null=True)
    timeArrival = models.DateTimeField(null=True)

    class Meta:
        db_table="Delivery"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    delivery_id = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    stars = models.IntegerField()
    del_rev = models.CharField(max_length=255)
    food_rev = models.CharField(max_length=255)
    
    class Meta:
        db_table="Review"



class payInfo(models.Model):
    infoId = models.AutoField(primary_key=True)
    custId = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payMode = models.CharField(max_length=100, choices=(("Cash","Cash"),("Card","Card")))
    payDescr = models.CharField(max_length = 100)

    class Meta:
        db_table="payInfo"


class Payment(models.Model):
    payId = models.AutoField(primary_key=True)
    payDate = models.DateTimeField()
    infoId = models.ForeignKey(payInfo, on_delete=models.CASCADE)

    class Meta:
        db_table="Payment"

# class cancelledOrder(model.Model):
#     orderId = models.ForeignKey(orders, on_delete=models.CASCADE)
#     reason = models.CharField(max_length=100)
#     refundId = models.


