from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db  import connection
from datetime import datetime
from .models import Customer,CustAddress,CustNos,Authenticate,Address,CustNos,Manager,Restaurant,restPhNos,Product,Category,Product_categ,orderProducts,Orders,deliveryPersonnel,availability,Delivery,Status
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    return render(request, "food_delivery_app/index.html", {})

def customer_list(request):
    customers = Customer.objects.all
    #customers = Customer.objects.raw("SELECT * FROM Customer")
    print(customers)
    return render(request, "food_delivery_app/custlist.html", {'data':customers})

def userreg(request):
    return render(request, "food_delivery_app/userreg.html", {})

def manreg(request):
    return render(request, "food_delivery_app/manreg.html", {})

def delreg(request):
    return render(request,"food_delivery_app/delreg.html")

def prodreg(request):
    return render(request,"food_delivery_app/prodreg.html")

def orderreg(request):
    pass

def login2(request):
    return render(request,"food_delivery_app/login2.html")

def login(request):
    cursor = connection.cursor()
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    #user = Authenticate.objects.filter(username=username1,password=password1)
    user = cursor.fetchone()
    print(user)
    #user = user[0]
    if user :
        # store the user's credentials in the session
        request.session['username'] = username
        request.session['password'] = password
        #return redirect('custHome')
        if user[3] == "Customer":
            return redirect('custHome')
        if user[3] == "Manager":
            return redirect('manHome')
        if user[3] == "DeliveryPerson":
            return redirect('delHome')
    else:
            # authentication failed, show an error message
        messages.error(request, 'Invalid username or password')
    
    # render the login page
    return render(request, 'food_delivery_app/login.html')
    # if user:
    #     for query in connection.queries:    
    #         print(query)
    #     return render(request,"food_delivery_app/userreg.html", {})
    #     #messages.success(request,"Signed in")
    # else:
    #     for query in connection.queries:    
    #         print(query)
    #     return render(request,"food_delivery_app/login.html", {})
    #     #messages.error(request,"Check Your Credentials")
    
    # return render(request,"food_delivery_app/login.html", {})
def logout(request):
    # clear the session data
    request.session.clear()
    # redirect to the login page
    return redirect('login')

def custHome(request):
    cursor = connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    p_id=user[0]
    cursor.execute( "SELECT `Customer`.`customer_id`, `Customer`.`f_name`, `Customer`.`l_name`, `Customer`.`email` FROM `Customer` WHERE (`Customer`.`p_id_id` = %s)",(p_id,))
    customer = cursor.fetchone()
    if customer:
        customer_id = customer[0]
    else:
    # handle the case where no customer is found
        customer_id = None
    if user[3]=="Customer":
        all_restaurants = Restaurant.objects.all()
        for query in connection.queries:
            print(query)

        context={
            'data':all_restaurants,
            'customer_id':customer_id,
        }
        return render(request,'food_delivery_app/custHome.html',{'data':all_restaurants})
    else:
        # authentication failed, redirect to the login page
        return redirect('login')

def manHome(request):
    cursor = connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute("SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    
    if user[3]=="Manager":
        auth_id = str(user[0])
        print(auth_id)
        cursor.execute("SELECT `Manager`.`manager_id`, `Manager`.`Name`, `Manager`.`email`, `Manager`.`p_id_id` FROM `Manager` WHERE (`Manager`.`p_id_id` = %s)",(auth_id))
        manager = cursor.fetchone()
        #manager = Manager.objects.filter(p_id = auth_id)[0]
        print(manager)
        manager_id = str(manager[0])
        cursor.execute("SELECT `Restaurant`.`restaurant_id` FROM `Restaurant` WHERE (`Restaurant`.`man_id_id` = %s)",(manager_id))
        restaurant = cursor.fetchone()
        #restaurant = Restaurant.objects.filter(man_id=manager_id)[0]
        restaurant_id = restaurant[0]
        all_items = Product.objects.filter(res_id = restaurant_id)
        #all_customers = Customer.objects.all()
        all_orders = Orders.objects.filter(restaurant_id = restaurant_id)
        for query in connection.queries:
            print(query)
        return render(request,'food_delivery_app/manHome.html',{'items':all_items,'orders':all_orders,'restaurant_id':restaurant_id})
    else:
        # authentication failed, redirect to the login page
        return redirect('login')

def delHome(request):
    cursor = connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    if user[3] == "DeliveryPerson":
        all_restaurants = Restaurant.objects.all()
        for query in connection.queries:
            print(query)
        return render(request,'food_delivery_app/custHome.html',{'data':all_restaurants})
    else:
        # authentication failed, redirect to the login page
        return redirect('login')
    pass
def insertCustomer(request):
    vuname = request.POST['tuname']
    vpass = request.POST['tpass']
    vfn = request.POST['tfn']
    vln = request.POST['tln']
    vemail = request.POST['temail']
    vaddr = request.POST['taddr']
    vtphone = request.POST['tphone']
    vzip = request.POST['tzip']

    #v_cust_id = Customer.objects.raw("""SELECT COUNT(*) AS `__count` FROM `Customer`""") + 1
    #v_cust_id = Customer.objects.all().count() + 1
    cursor = connection.cursor()
    customer = Customer.objects.all()
    if customer:
        cursor.execute("SELECT MAX(customer_id)+1 AS `__count` FROM `Customer`")
        r1 = cursor.fetchone()[0]
    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Customer`")
        r1 = cursor.fetchone()[0]
    v_cust_id = r1

    authenticate = Authenticate.objects.all()
    if authenticate:
        cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2
    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2

    address = Address.objects.all()
    if address:
        cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
        r3 = cursor.fetchone()[0]
        v_addr_id = r3
    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
        r3 = cursor.fetchone()[0]
        v_addr_id = r3
    
    # custaddress = CustAddress.objects.all()
    # if custaddress:
    #     cursor.execute("SELECT MAX(cust_add_id)+1 AS `__count` FROM `CustAddress`")
    #     r4 = cursor.fetchone()[0]
    #     v_cust_addr_id = r4
    
    # else:
    #     cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `CustAddress`")
    #     r4 = cursor.fetchone()[0]
    #     v_cust_addr_id = r4
    # v_p_id = Authenticate.objects.all().count() + 1
    # v_addr_id = Address.objects.all().count() + 1
    # v_cust_addr_id = CustAddress.objects.all().count() + 1
    #Authenticate.objects.raw("INSERT INTO `Authenticate` (`p_id`, `username`, `password`) VALUES (6, 'atharva', 'atharva')")

    # q1 = "INSERT INTO `Authenticate` (`p_id`, `username`, `password`) VALUES (%s, %s, %s)"
    # value = (v_p_id,vuname,vpass)
    user_type = "Customer"
    cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vuname,vpass,user_type))
    cursor.execute("INSERT INTO `Customer` (`customer_id`, `f_name`, `l_name`, `email`, `p_id_id`) VALUES (%s,%s,%s,%s,%s)",(v_cust_id,vfn,vln,vemail,v_p_id))
    cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vaddr,vzip))
    cursor.execute("INSERT INTO `CustNos` (`customer_id_id`, `ph_no`) VALUES (%s,%s)",(v_cust_id,vtphone))
    cursor.execute("INSERT INTO `CustAddress` (`customer_id_id`, `add_id_id`) VALUES (%s,%s)",(v_cust_id,v_addr_id))

    # q2 = "INSERT INTO `Customer` (`customer_id`, `f_name`, `l_name`, `email`, `p_id_id`) VALUES (?,?,?,?,?)"
    # value = (v_cust_id,vfn,vln,vemail,v_p_id)
    # cursor.execute(q2,value)

    # q3 = "INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (?,?,?)"
    # value = (v_addr_id,vaddr,vzip)
    # cursor.execute(q3,value)

    # q4 = "INSERT INTO `CustNos` (`customer_id_id`, `ph_no`) VALUES (?,?)"
    # value = (v_cust_id,vtphone)
    # cursor.execute(q4,value)

    # q5 = "INSERT INTO `CustAddress` (`cust_add_id`, `add_id_id`, `customer_id_id`) VALUES (?,?,?)"
    # value = (v_cust_addr_id,v_addr_id,v_cust_id)
    # cursor.execute(q5,value)

    # credentials = Authenticate.objects.create(p_id =v_p_id, username=vuname,password=vpass)
    # customer=Customer.objects.create(customer_id=v_cust_id,f_name=vfn,l_name=vln,email=vemail,p_id_id=v_p_id)
    # addr = Address.objects.create(add_id=v_addr_id,address=vaddr,zipcode=vzip)
    # phone = CustNos.objects.create(customer_id_id=v_cust_id,ph_no=vtphone)
    # cust_addr = CustAddress.objects.create(cust_add_id=v_cust_addr_id,add_id_id=v_addr_id,customer_id_id=v_cust_id)
    for query in connection.queries:    
        print(query)

    return render(request, "food_delivery_app/login.html", {}) 

def insertManager(request):

    vmname = request.POST['muname']
    vmpass = request.POST['mpass']
    vmn = request.POST['mn']
    #vmphone = request.POST['mphone']
    vmemail = request.POST['memail']


    vrname = request.POST['rname']
    #vremail = request.POST['remail']
    vraddr = request.POST['raddr']
    vrphone = request.POST['rphone']
    vrzip = request.POST['rzip']

    cursor = connection.cursor()

    #manager = Manager.objects.all()
    manager = cursor.execute("SELECT `Manager`.`manager_id`, `Manager`.`Name`, `Manager`.`email`, `Manager`.`p_id_id` FROM `Manager`")
    if manager:
        cursor.execute("SELECT MAX(manager_id)+1 AS `__count` FROM `Manager`")
        r1 = cursor.fetchone()[0]
        v_man_id = r1

    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Manager`")
        r1 = cursor.fetchone()[0]
        v_man_id = r1
    


    authenticate = Authenticate.objects.all()
    if authenticate:
        cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2
    else:        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2

    restaurant = Restaurant.objects.all()
    if restaurant:
        cursor.execute("SELECT MAX(restaurant_id)+1 AS `__count` FROM `Restaurant`")
        r3 = cursor.fetchone()[0]
        v_res_id = r3

    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Restaurant`")
        r3 = cursor.fetchone()[0]
        v_res_id = r3

    address = Address.objects.all()
    if address:
        cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
        r4 = cursor.fetchone()[0]
        v_addr_id = r4
    else:
        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
        r4 = cursor.fetchone()[0]
        v_addr_id = r4

    user_type = "Manager"

    cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vmname,vmpass,user_type))
    cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vraddr,vrzip))
    cursor.execute("INSERT INTO `Manager` (`manager_id`, `Name`, `email`,`p_id_id`) VALUES (%s,%s,%s,%s)",(v_man_id,vmn,vmemail,v_p_id))
    cursor.execute("INSERT INTO `Restaurant` (`restaurant_id`,`addr_id_id`, `man_id_id`,`restaurant_name`) VALUES (%s,%s,%s,%s)",(v_res_id,v_addr_id,v_man_id,vrname))
    cursor.execute("INSERT INTO `restPhNos` (`restaurant_id_id`, `ph_no`) VALUES (%s,%s)",(v_res_id,vrphone))

    for query in connection.queries:    
        print(query)    

    return render(request, "food_delivery_app/manreg.html", {}) 
 
def insertDeliveryPerson(request):
     
    vdname = request.POST['duname']
    vdpass = request.POST['dpass']
    vdn = request.POST['dn']
    #vmphone = request.POST['mphone']
    vdphone = request.POST['dphone']
    vdaddr = request.POST['daddr']
    vdzip = request.POST['dzip']

    cursor = connection.cursor()
    authenticate = Authenticate.objects.all()
    if authenticate:
        cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2
    else:        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
        r2 = cursor.fetchone()[0]
        v_p_id = r2


    delman = cursor.execute("SELECT `deliveryPersonnel`.`personnel_id`, `deliveryPersonnel`.`name`, `deliveryPersonnel`.`p_id_id`, `deliveryPersonnel`.`addr_id_id`, `deliveryPersonnel`.`phone` FROM `deliveryPersonnel`")
    if delman:
        cursor.execute("SELECT MAX(personnel_id)+1 AS `__count` FROM `deliveryPersonnel`")
        r1 = cursor.fetchone()[0]
        v_del_id = r1

    else:
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `deliveryPersonnel`")
        r1 = cursor.fetchone()[0]
        v_del_id = r1

    address = Address.objects.all()
    if address:
        cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
        r4 = cursor.fetchone()[0]
        v_addr_id = r4
    else:
        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
        r4 = cursor.fetchone()[0]
        v_addr_id = r4
    
    user_type = "DeliveryPerson"
    availability="Available"

    cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vdname,vdpass,user_type))
    cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vdaddr,vdzip))
    cursor.execute("INSERT INTO `deliveryPersonnel` (`personnel_id`, `name`, `p_id_id`, `addr_id_id`,`phone`) VALUES (%s, %s, %s, %s, %s)",(v_del_id,vdn,v_p_id,v_addr_id,vdphone))
    cursor.execute("INSERT INTO `Availability` (`personnel_id`, `availability`) VALUES (%s, %s)",(v_del_id,availability))
    for query in connection.queries:    
        print(query)    

    return render(request, "food_delivery_app/delreg.html", {}) 
   

def insertOrder(request):
    pass 

def insertProduct(request):
    cursor = connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute("SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    
    if user[3]=="Manager":
        auth_id = str(user[0])
        print(auth_id)
        cursor.execute("SELECT `Manager`.`manager_id`, `Manager`.`Name`, `Manager`.`email`, `Manager`.`p_id_id` FROM `Manager` WHERE (`Manager`.`p_id_id` = %s)",(auth_id))
        manager = cursor.fetchone()
        #manager = Manager.objects.filter(p_id = auth_id)[0]
        print(manager)
        manager_id = str(manager[0])
        cursor.execute("SELECT `Restaurant`.`restaurant_id` FROM `Restaurant` WHERE (`Restaurant`.`man_id_id` = %s)",(manager_id))
        restaurant = cursor.fetchone()
        #restaurant = Restaurant.objects.filter(man_id=manager_id)[0]
        restaurant_id = restaurant[0]
        vname = request.POST['pname']
        vprice = request.POST['price']
        vdesc = request.POST['pdesc']
        #vcat = request.POST['pcat']

        product = Product.objects.all()
        if product:
            cursor.execute("SELECT MAX(product_id)+1 AS `__count` FROM `Product`")
            r2 = cursor.fetchone()[0]
            v_prod_id = r2
        else:        
            cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Product`")
            r2 = cursor.fetchone()[0]
            v_prod_id = r2

        cursor.execute("INSERT INTO `Product` (`product_id`, `res_id_id`, `item_name`, `price`, `description`) VALUES (%s, %s, %s, %s, %s)",(v_prod_id,restaurant_id,vname,vprice,vdesc))


        for query in connection.queries:
            print(query)
        return redirect('manHome')
        #return render(request,'food_delivery_app/manHome.html',{})
    else:
        # authentication failed, redirect to the login page
        return redirect('login')
    
def restView(request):

    pass 

def item_list(request, restaurant_id):
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id)
    items = Product.objects.filter(res_id = restaurant_id)
    context = {'restaurant': restaurant, 'items': items}
    return render(request, 'food_delivery_app/item_list.html', context)
 
def order(request, product_id):
    product = Product.objects.get(product_id=product_id)
    print(product)
    #restaurant = Restaurant.objects.filter(restaurant_id=product.res_id)
    cursor = connection.cursor()
    #cursor.execute( "SELECT `Product`.`res_id_id`, `Product`.``, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    order = Orders.objects.all()
    cursor = connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    p_id = user[0]
    customer = Customer.objects.get(p_id=p_id)
    payment_type = request.POST.get('payment_type')
    if order:
        cursor.execute("SELECT MAX(order_id)+1 AS `__count` FROM `Orders`")
        r2 = cursor.fetchone()[0]
        v_order_id = r2
    else:        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Orders`")
        r2 = cursor.fetchone()[0]
        v_order_id = r2
    Orders.objects.create(order_id=v_order_id,restaurant_id =product.res_id,customer_id=customer,total_price=product.price,ordered_on=datetime.now())
    order = {'item_name': product.item_name, 'price': product.price, 'payment_type': payment_type}
    context = {'order': order}
    for query in connection.queries:
        print(query)
    return render(request, 'food_delivery_app/order.html', context)

def man_view(request,restaurant_id):
    #product = Product.objects.get(product_id=product_id)
    #print(product)
    #restaurant = Restaurant.objects.filter(restaurant_id=product.res_id)
    # cursor = connection.cursor()
    # #cursor.execute( "SELECT `Product`.`res_id_id`, `Product`.``, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    # #order = Orders.objects.all()
    # cursor = connection.cursor()
    # username = request.session.get('username')
    # password = request.session.get('password')
    # cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    # user = cursor.fetchone()
    # p_id = user[0]
    # manager = Manager.objects.get(p_id=p_id)
    # restaurant = Restaurant.objects.get(man_id=manager)
    # #restaurant = request.user.restaurant # assuming the authenticated user is a restaurant manager
    # orders = Orders.objects.filter(restaurant_id=restaurant)
    # personnel_id_q = availability.objects.filter(availability='Available').values_list('personnel_id', flat=True)
    # delivery_personnel = deliveryPersonnel.objects.filter(personnel_id=personnel_id_q)
    # delivery_personnel = list(delivery_personnel)
    # for order in orders:
    #     order_delivery_personnel = delivery_personnel.first()  # retrieve the first available delivery person
    #     if order_delivery_personnel is not None:
    #         # if there is an available delivery person, assign them to the order
    #         order.delivery_personnel = order_delivery_personnel
    #         order.save()
    #         # remove the delivery person from the QuerySet so they can't be assigned to another order
    #         delivery_personnel = delivery_personnel.exclude(personnel_id=order_delivery_personnel.personnel_id)
    #     else:
    #         # if there are no more available delivery personnel, break out of the loop
    #         break
    # context = {'orders': orders, 'delivery_personnel': delivery_personnel}
    # return render(request, 'man_view.html', context)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    
    #orders = Orders.objects.filter(restaurant_id=restaurant)
    personnel_ids = availability.objects.filter(availability='Available').values_list('personnel', flat=True)
    delivery_orders = Orders.objects.filter(restaurant_id=restaurant, status_val='Out For Delivery')
    undelivered_orders = Orders.objects.filter(restaurant_id=restaurant,status_val='Processing')
    delivered_orders = Orders.objects.filter(restaurant_id=restaurant,status_val='Delivered')
    delivery_personnel = deliveryPersonnel.objects.filter(personnel_id__in=personnel_ids)   
    # availability1=availability.objects.filter(availability='Available')
    # delivery_personnel = deliveryPersonnel.objects.filter(personnel_id=availability1.values('personnel'))
    if request.method == 'POST':
        order_id = request.POST['order_id']
        personnel_id = request.POST['personnel_id']
        order = Orders.objects.get(order_id=order_id)
        personnel = deliveryPersonnel.objects.get(personnel_id=personnel_id)
        order_delivery = Delivery.objects.create(
            orderId=order,
            personnelId=personnel,
            timeDispatch=datetime.now()
        )
        Orders.objects.filter(order_id=order_id).update(status_val="Out For Delivery")
        availability.objects.filter(personnel=personnel_id).update(availability="Delivering")
        order_delivery.save()
        #order_status = Status.objects.get(status_val='Processing')
        #order.status_id = order_status
        #order.save()
    context = {
        'restaurant':restaurant,
        'delivery_orders':delivery_orders,
        'undelivered_orders':undelivered_orders,
        'delivered_orders':delivered_orders,
        'delivery_personnel':delivery_personnel,
    }
    for query in connection.queries:
        print(query)
    return render(request,'food_delivery_app/man_view.html',context)


def del_view(request, personnel_id):
    personnel = deliveryPersonnel.objects.get(personnel_id=personnel_id)
    delivery = Delivery.objects.filter(personnelId=personnel_id)
    

    if request.method == 'POST':
        order_id = int(request.POST.get('order_id'))
        #order_id=request.POST['order_id']
        delivery_id=request.POST.get('delivery_id')
        #order=Orders.objects.filter(order_id=order_id)
        Orders.objects.filter(order_id=order_id).update(status_val="Delivered")
        Delivery.objects.filter(delivery_id=delivery_id).update(timeArrival=datetime.now())
        availability.objects.filter(personnel=personnel_id).update(availability="Available")
        return redirect('del_view', personnel_id=personnel_id)

    context = {
        'personnel':personnel,
        'deliveries':delivery,
    }
    for query in connection.queries:
        print(query)
    return render(request,'food_delivery_app/del_view.html',context)

def edit_cprofile(request, customer_id):
    
    customer = Customer.objects.filter(customer_id=customer_id)
    #p_id=customer.p_id
    add_id = CustAddress.objects.filter(customer_id=customer_id)
    address = Address.objects.filter(add_id=add_id)
    ph_no = CustNos.objects.filter(customer_id=customer_id)
    context = {
        'customer':customer,
        'address':address,
        'phno':ph_no,
    }


    return render(request, 'food_delivery_app/edit_cprofile.html',context)

