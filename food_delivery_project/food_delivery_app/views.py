from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db  import connection
from datetime import datetime
from .models import Customer,CustAddress,CustNos,Authenticate,Address,CustNos,Manager,Restaurant,restPhNos,Product,orderProducts,Orders,deliveryPersonnel,Delivery,restaurantPersonnel
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
def home(request):
    return render(request, "food_delivery_app/home.html", {})
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
        return render(request,'food_delivery_app/custHome.html',context)
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
    p_id=user[0]
    cursor.execute("SELECT `deliveryPersonnel`.`personnel_id` FROM `deliveryPersonnel` WHERE (`deliveryPersonnel`.`p_id_id` = %s)",(p_id,))
    personnel = cursor.fetchone()
    personnel_id=personnel[0]
    if user[3] == "DeliveryPerson":
        
        
        cursor.execute("SELECT `RestaurantPersonnel`.`restaurant_id` FROM `RestaurantPersonnel` WHERE (`RestaurantPersonnel`.`personnel_id` = %s)",(personnel_id,))
        selected_restaurants=cursor.fetchall()

        all_restaurants = Restaurant.objects.all()
        for query in connection.queries:
            print(query)
        return render(request,'food_delivery_app/delHome.html',{'data':selected_restaurants,
                                                                'personnel_id':personnel_id})
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
def add_customer(request):
    if request.method == 'POST':
        vuname = request.POST['tuname']
        vpass = request.POST['tpass']
        vfn = request.POST['tfn']
        vln = request.POST['tln']
        vemail = request.POST['temail']
        vaddr = request.POST['taddr']
        vtphone = request.POST['tphone']
        vzip = request.POST['tzip']

        with connection.cursor() as cursor:
            cursor.execute("CALL AddCustomer(%s, %s, %s, %s, %s, %s, %s)", [vuname, vpass, vfn, vln, vemail, vaddr, vzip])
            
    return render(request, "food_delivery_app/login.html")

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
 
# def insertDeliveryPerson(request):
#     if request.method=='POST':
#         vdname = request.POST['duname']
#         vdpass = request.POST['dpass']
#         vdn = request.POST['dn']
#         #vmphone = request.POST['mphone']
#         vdphone = request.POST['dphone']
#         vdaddr = request.POST['daddr']
#         vdzip = request.POST['dzip']
#         selected_restaurants = request.POST.getlist('restaurants')

#         cursor = connection.cursor()
#         authenticate = Authenticate.objects.all()
#         if authenticate:
#             cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
#             r2 = cursor.fetchone()[0]
#             v_p_id = r2
#         else:        
#             cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
#             r2 = cursor.fetchone()[0]
#             v_p_id = r2


#         delman = cursor.execute("SELECT `deliveryPersonnel`.`personnel_id`, `deliveryPersonnel`.`name`, `deliveryPersonnel`.`p_id_id`, `deliveryPersonnel`.`addr_id_id`, `deliveryPersonnel`.`phone` FROM `deliveryPersonnel`")
#         if delman:
#             cursor.execute("SELECT MAX(personnel_id)+1 AS `__count` FROM `deliveryPersonnel`")
#             r1 = cursor.fetchone()[0]
#             v_del_id = r1

#         else:
#             cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `deliveryPersonnel`")
#             r1 = cursor.fetchone()[0]
#             v_del_id = r1

#         address = Address.objects.all()
#         if address:
#             cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
#             r4 = cursor.fetchone()[0]
#             v_addr_id = r4
#         else:
            
#             cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
#             r4 = cursor.fetchone()[0]
#             v_addr_id = r4
        
#         user_type = "DeliveryPerson"
#         availability="Available"

#         cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vdname,vdpass,user_type))
#         cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vdaddr,vdzip))
#         cursor.execute("INSERT INTO `deliveryPersonnel` (`personnel_id`, `name`, `p_id_id`, `addr_id_id`,`phone`) VALUES (%s, %s, %s, %s, %s)",(v_del_id,vdn,v_p_id,v_addr_id,vdphone))
#         cursor.execute("INSERT INTO `Availability` (`personnel_id`, `availability`) VALUES (%s, %s)",(v_del_id,availability))

#         for r_id in selected_restaurants:
#                 restaurant = Restaurant.objects.get(pk=r_id)
#                 rp = restaurantPersonnel(personnel=v_del_id, restaurant=restaurant)
#                 rp.save()
#     # for query in connection.queries:    
#     #     print(query)    

#     #return render(request, "food_delivery_app/delreg.html", {}) 
#         print(restaurants)
#         return render(request, "food_delivery_app/delreg_success.html")
#     else:
#         # Get all restaurants to display on the registration form
#         restaurants = Restaurant.objects.all()
#         print(restaurants)
#         return render(request, "food_delivery_app/delreg.html", {'restaurants': restaurants})

def insertDeliveryPerson(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        # Get form data
        vdname = request.POST['duname']
        vdpass = request.POST['dpass']
        vdn = request.POST['dn']
        vdphone = request.POST['dphone']
        vdaddr = request.POST['daddr']
        vdzip = request.POST['dzip']
        selected_restaurants = request.POST.getlist('restaurant')
        
        authenticate = Authenticate.objects.all()
        person = deliveryPersonnel.objects.all()
        address = Address.objects.all()
        if authenticate:
            cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
            v_p_id = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
            v_p_id = cursor.fetchone()[0]

        if person:
            cursor.execute("SELECT MAX(personnel_id)+1 AS `__count` FROM `deliveryPersonnel`")
            v_del_id = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `deliveryPersonnel`")
            v_del_id = cursor.fetchone()[0]
        if address:
            cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
            v_addr_id = cursor.fetchone()[0]
        else:
            cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
            v_addr_id = cursor.fetchone()[0]

        # Create new entries in the Authenticate, Address, and deliveryPersonnel tables
        user_type = "Delivery Person"
        availability = "Available"
        cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vdname,vdpass,user_type))
        cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vdaddr,vdzip))
        cursor.execute("INSERT INTO `deliveryPersonnel` (`personnel_id`, `name`, `p_id_id`, `addr_id_id`,`phone`,`availability`) VALUES (%s, %s, %s, %s, %s, %s)",(v_del_id,vdn,v_p_id,v_addr_id,vdphone,availability))
        #cursor.execute("INSERT INTO `Availability` (`personnel_id`, `availability`) VALUES (%s, %s)",(v_del_id,availability))

        # auth = Authenticate(p_id=v_p_id, username=vdname, password=vdpass, user_type='DeliveryPerson')
        # auth.save()

        # addr = Address(add_id=v_addr_id, address=vdaddr, zipcode=vdzip)
        # addr.save()

        # del_person = deliveryPersonnel(personnel_id=v_del_id, name=vdn, p_id=auth, addr_id=addr, phone=vdphone)
        # del_person.save()

        # Add the delivery person to the selected restaurants in the restaurantPersonnel table
        del_person = deliveryPersonnel.objects.filter(personnel_id=v_del_id)
        for r_id in selected_restaurants:
            restaurant = Restaurant.objects.get(pk=r_id)
            personnel = deliveryPersonnel.objects.get(personnel_id=v_del_id)
            # Link the delivery person to the selected restaurant
            rp = restaurantPersonnel(personnel=personnel, restaurant=restaurant)
            rp.save()
            

        # Render success page
        return render(request, "food_delivery_app/delreg_success.html")
    else:
        # Get all restaurants to display on the registration form
        restaurants = Restaurant.objects.all()
        print(restaurants)
        return render(request, "food_delivery_app/delreg.html", {'restaurants': restaurants})

# def insertDeliveryPerson(request):
    
#     if request.method == 'POST':
#         cursor = connection.cursor()
#         # Get form data
#         vdname = request.POST['duname']
#         vdpass = request.POST['dpass']
#         vdn = request.POST['dn']
#         vdphone = request.POST['dphone']
#         vdaddr = request.POST['daddr']
#         vdzip = request.POST['dzip']
#         selected_restaurants = request.POST.getlist('restaurant')
        
#         # Get the user_type for the delivery person
#         user_type = 'DeliveryPerson'

#         # Check if there are any entries in the Authenticate, Address, and deliveryPersonnel tables
#         cursor.execute("SELECT COUNT(*) FROM `Authenticate`")
#         auth_count = cursor.fetchone()[0]
#         cursor.execute("SELECT COUNT(*) FROM `Address`")
#         addr_count = cursor.fetchone()[0]
#         cursor.execute("SELECT COUNT(*) FROM `deliveryPersonnel`")
#         person_count = cursor.fetchone()[0]

#         if auth_count > 0:
#             cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
#             v_p_id = cursor.fetchone()[0]
#         else:
#             v_p_id = 1

#         if person_count > 0:
#             cursor.execute("SELECT MAX(personnel_id)+1 AS `__count` FROM `deliveryPersonnel`")
#             v_del_id = cursor.fetchone()[0]
#         else:
#             v_del_id = 1
#         if addr_count > 0:
#             cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
#             v_addr_id = cursor.fetchone()[0]
#         else:
#             v_addr_id = 1

#         # Create new entries in the Authenticate, Address, and deliveryPersonnel tables
#         availability = "Available"
#         cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s,%s,%s,%s)", (v_p_id,vdname,vdpass,user_type))
#         cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id, vdaddr, vdzip))
#         cursor.execute("INSERT INTO `deliveryPersonnel` (`personnel_id`, `name`, `p_id_id`, `addr_id_id`,`phone`) VALUES (%s,%s,%s,%s,%s)",(v_del_id,vdn, v_p_id,v_addr_id, vdphone))
#         cursor.execute("INSERT INTO `Availability` (`personnel_id`, `availability`) VALUES (%s,%s)",(v_del_id, availability))

#         # Add the delivery person to the selected restaurants in the restaurantPersonnel table
#         for r_id in selected_restaurants:
#             cursor.execute("INSERT INTO `restaurantPersonnel` (`personnel_id`, `restaurant_id`) VALUES (%s,%s)",(v_del_id, r_id))

#         # Render success page
#         return render(request, "food_delivery_app/delreg_success.html")
#     else:
#         cursor=connection.cursor()
#         # Get all restaurants to display on the registration form
#         cursor.execute("SELECT * FROM `Restaurant`")
#         restaurants = cursor.fetchall()
#         #print(len(restaurants))
#         length = len(restaurants)
#         return render(request, "food_delivery_app/delreg.html", {'restaurants': restaurants,'length':length})

def add_delivery_person(request):

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


    if request.method == 'POST':
        vdname = request.POST['duname']
        vdpass = request.POST['dpass']
        vdn = request.POST['dn']
        vdphone = request.POST['dphone']
        vdaddr = request.POST['daddr']
        vdzip = request.POST['dzip']
        selected_restaurant_id = restaurant_id
        ##manager_id = request.session.get('manager_id')
        restaurant=Restaurant.objects.get(restaurant_id=restaurant_id)
        # Get the manager object
        # manager = Manager.objects.get(pk=manager_id)

        # Check if the selected restaurant is linked to the manager
        #restaurant = Restaurant.objects.get(pk=selected_restaurant_id)
        # if restaurant.man_id != manager:
        #     return render(request, 'food_delivery_app/add_del_personnel.html', {'error': 'The selected restaurant is not linked to your account.'})

        # Generate new IDs for the delivery person and address
        with connection.cursor() as cursor:
            authenticate = Authenticate.objects.all()
            person = deliveryPersonnel.objects.all()
            address = Address.objects.all
            if authenticate:
                cursor.execute("SELECT MAX(p_id)+1 AS `__count` FROM `Authenticate`")
                v_p_id = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Authenticate`")
                v_p_id = cursor.fetchone()[0]

            if person:
                cursor.execute("SELECT MAX(personnel_id)+1 AS `__count` FROM `deliveryPersonnel`")
                v_del_id = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `deliveryPersonnel`")
                v_del_id = cursor.fetchone()[0]
            if address:
                cursor.execute("SELECT MAX(add_id)+1 AS `__count` FROM `Address`")
                v_addr_id = cursor.fetchone()[0]
            else:
                cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Address`")
                v_addr_id = cursor.fetchone()[0]

            # Insert the new delivery person into the database
            user_type = "DeliveryPerson"
            availability = "Available"
            cursor.execute("INSERT INTO `Authenticate` (`p_id`, `username`, `password`, `user_type`) VALUES (%s, %s, %s, %s)",(v_p_id,vdname,vdpass,user_type))
            cursor.execute("INSERT INTO `Address` (`add_id`, `address`, `zipcode`) VALUES (%s,%s,%s)",(v_addr_id,vdaddr,vdzip))
            cursor.execute("INSERT INTO `deliveryPersonnel` (`personnel_id`, `name`, `p_id_id`, `addr_id_id`,`phone`,`availability`) VALUES (%s, %s, %s, %s, %s, %s)",(v_del_id,vdn,v_p_id,v_addr_id,vdphone,availability))
            #cursor.execute("INSERT INTO `Availability` (`personnel_id`, `availability`) VALUES (%s, %s)",(v_del_id,availability))
            personnel = deliveryPersonnel.objects.get(personnel_id=v_del_id)
            # Link the delivery person to the selected restaurant
            rp = restaurantPersonnel(personnel=personnel, restaurant=restaurant)
            rp.save()

        return render(request, 'food_delivery_app/login.html', {'success': 'Delivery person added successfully.'})
    else:
        #manager_id = request.session.get('manager_id')
        # Get all restaurants linked to the manager
        restaurants = Restaurant.objects.filter(man_id=manager_id)

        return render(request, 'food_delivery_app/add_del_personnel.html', {'restaurants': restaurants})
   

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
    #cursor.execute()
    customer = Customer.objects.get(p_id=p_id)
    payment_type = request.POST.get('payment_type')
    payment_quantity = request.POST.get('payment_quantity')
    if order:
        cursor.execute("SELECT MAX(order_id)+1 AS `__count` FROM `Orders`")
        r2 = cursor.fetchone()[0]
        v_order_id = r2
    else:        
        cursor.execute("SELECT COUNT(*)+1 AS `__count` FROM `Orders`")
        r2 = cursor.fetchone()[0]
        v_order_id = r2
    
    cursor.execute( "SELECT `Customer`.`customer_id` FROM `Customer` WHERE (`Customer`.`p_id_id` = %s)",(p_id,))
    customer_id = cursor.fetchone()[0]
    print(customer_id)
    cursor.execute( "SELECT `CustAddress`.`add_id_id` FROM `CustAddress` WHERE (`CustAddress`.`customer_id_id` = %s)",(customer_id,))
    addr_id = cursor.fetchone()[0]
    price=int(product.price)
    quantity=int(payment_quantity)
    price = price*quantity
    
    cursor.execute("INSERT INTO `Orders` (`order_id`, `addr_id_id`, `restaurant_id_id`, `customer_id_id`, `total_price`, `ordered_on`, `status_val`) VALUES (%s, %s, %s, %s, %s, %s, %s)",(v_order_id,addr_id,product.res_id.restaurant_id,customer_id,price,datetime.now(),"Processing"))
    cursor.execute("INSERT INTO `orderProducts` (`order_id_id`, `product_id_id`, `quantity`) VALUES (%s, %s, %s)",(v_order_id,product.product_id,payment_quantity))
    cursor.execute("INSERT INTO `Payment` (`payMode`, `cust_id_id`, `order_id_id`, `payDate`) VALUES (%s, %s, %s, curdate())",(payment_type,customer_id,v_order_id))
    
    #Orders.objects.create(order_id=v_order_id,addr_id=addr_id,restaurant_id =product.res_id,customer_id=customer,total_price=product.price,ordered_on=datetime.now())
    #orderProducts.objects.create()
    order = {'item_name': product.item_name, 'price': product.price, 'payment_type': payment_type, 'payment_quantity':payment_quantity}
    context = {'order': order}
    for query in connection.queries:
        print(query)
    return render(request, 'food_delivery_app/order.html', context)

def man_view(request,restaurant_id):
    
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    
    #orders = Orders.objects.filter(restaurant_id=restaurant)
    #personnels = availability.objects.filter(availability='Available').values_list('personnel', flat=True)
    personnel_ids = restaurantPersonnel.objects.filter(restaurant=restaurant_id).values_list('personnel', flat=True)
    delivery_orders = Orders.objects.filter(restaurant_id=restaurant, status_val='Out For Delivery')
    undelivered_orders = Orders.objects.filter(restaurant_id=restaurant,status_val='Processing')
    delivered_orders = Orders.objects.filter(restaurant_id=restaurant,status_val='Delivered')
    delivery_personnel = deliveryPersonnel.objects.filter(personnel_id__in=personnel_ids,availability="Available")
       
    cursor= connection.cursor()
    #cursor.execute("")
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
        deliveryPersonnel.objects.filter(personnel_id=personnel_id).update(availability="Delivering")
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
    cursor=connection.cursor()

    personnel = deliveryPersonnel.objects.get(personnel_id=personnel_id)
    delivery = Delivery.objects.filter(personnelId=personnel_id)
    

    if request.method == 'POST':
        order_id = int(request.POST.get('order_id'))
        #order_id=request.POST['order_id']
        delivery_id=request.POST.get('delivery_id')
        #order=Orders.objects.filter(order_id=order_id)

        cursor.execute("UPDATE `Orders` SET `status_val` = 'Delivered' WHERE `Orders`.`order_id` = %s",(order_id,))
        cursor.execute("UPDATE `Delivery` SET `timeArrival` = %s WHERE `Delivery`.`delivery_id` = %s",(datetime.now(),delivery_id))
        cursor.execute("UPDATE `deliveryPersonnel` SET `availability` = 'Available' WHERE `deliveryPersonnel`.`personnel_id` = %s",(personnel_id,))
        # Orders.objects.filter(order_id=order_id).update(status_val="Delivered")
        # Delivery.objects.filter(delivery_id=delivery_id).update(timeArrival=datetime.now())
        # availability.objects.filter(personnel=personnel_id).update(availability="Available")
        for query in connection.queries:
            print(query)
        return redirect('del_view', personnel_id=personnel_id)

    context = {
        'personnel':personnel,
        'deliveries':delivery,
    }
    for query in connection.queries:
        print(query)
    return render(request,'food_delivery_app/del_view.html',context)

# def edit_cprofile(request, customer_id):
    
#     customer = Customer.objects.filter(customer_id=customer_id)
#     #p_id=customer.p_id
#     add_id = CustAddress.objects.filter(customer_id=customer_id)
#     address = Address.objects.filter(add_id=add_id)
#     ph_no = CustNos.objects.filter(customer_id=customer_id)
#     context = {
#         'customer':customer,
#         'address':address,
#         'phno':ph_no,
#     }


#     return render(request, 'food_delivery_app/edit_cprofile.html',context)

# def edit_cprofile(request, customer_id):
#     customer = Customer.objects.filter(customer_id=customer_id)
#     add_ids = CustAddress.objects.filter(customer_id=customer_id).values_list('add_id', flat=True)
#     addresses = Address.objects.filter(add_id__in=add_ids)
#     ph_no = CustNos.objects.filter(customer_id=customer_id)
#     context = {
#         'customer': customer,
#         'addresses': addresses,
#         'phno': ph_no,
#     }
#     return render(request, 'food_delivery_app/edit_cprofile.html', context)
def edit_cprofile(request, customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    if request.method == 'POST':
        # Update customer information
        address1 = CustAddress.objects.get(customer_id=customer_id)
        add_id = address1.add_id.add_id
        customer.f_name = request.POST.get('f_name')
        customer.l_name = request.POST.get('l_name')
        customer.email = request.POST.get('email')
        customer.save()
        messages.success(request, 'Profile updated successfully.')
        # Update customer addresses
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        
        #add_id = request.POST.get('add_id')
        # address = request.POST.getlist('address')[i]
        # zip_code = request.POST.getlist('zip_code')[i]
                
                # Update the corresponding Address object
        address1 = Address.objects.get(add_id=add_id)
        address1.address = address
        address1.zipcode = zipcode
        address1.save()
        messages.success(request, 'Addresses updated successfully.')
        return redirect('custHome')
    else:
        addresses = Address.objects.filter(custaddress__customer_id=customer)
        context = {
            'customer': customer,
            'addresses': addresses
        }
        for query in connection.queries:
            print(query)
        return render(request, 'food_delivery_app/edit_cprofile.html', context)
    
# def forgot_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         new_password = request.POST.get('new_password')
#         # security_question = request.POST.get('security_question')
#         # security_answer = request.POST.get('security_answer')
#         cursor=connection.cursor()  
#         #user = Authenticate.objects.filter(username=username)
#         user = cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`username` = %s)",(username,))
#         #user = Authenticate.objects.filter(username=username1,password=password1)
#         user = cursor.fetchone()
#         p_id = user[0]
#         print(user)
#         #user = user[0]
#         if user :
#             # store the user's credentials in the session
#             request.session['username'] = username
#             if user[3] == "Customer":
#                 user1 = Customer.objects.get(p_id=p_id)
#                 user_email=user1.email
#                 if(user_email==email):
#                     user2 = Authenticate.objects.filter(username=username)
#                     user2.update(password=new_password)
            
#             if user[3] == "Manager":
#                 user1 = Manager.objects.get(p_id=p_id)
#                 user_email=user1.email
#                 if(user_email==email):
#                     user2 = Authenticate.objects.filter(username=username)
#                     user2.update(password=new_password)

#             if user[3] == "Delivery Person":
#                 user1 = deliveryPersonnel.objects.get(p_id=p_id)
#                 user_email=user1.email
#                 if(user_email==email):
#                     user2 = Authenticate.objects.filter(username=username)
#                     user2.update(password=new_password)
                
#         else:
#                 # authentication failed, show an error message
#             messages.error(request, 'Invalid username or password')
#             user1
#             print(user)
#             #user2 = 
#         if user is None:
#             messages.error(request, 'Email address not found')
#             return redirect('forgot_password')

#         messages.success(request, 'Your password has been reset')
#         for query in connection.queries:
#             print(query)
#         return redirect('login')
    

#     return render(request, 'food_delivery_app/forgot_password.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        # Fetch the user details from the database
        cursor = connection.cursor()
        cursor.execute("""
            SELECT a.p_id, a.username, a.password, a.user_type, c.email
            FROM Authenticate a
            LEFT JOIN Customer c ON c.p_id_id = a.p_id
            WHERE a.username = %s
        """, [username])
        user = cursor.fetchone()

        # Check if the user exists and the provided email is correct
        if user and user[4] == email:
            p_id = user[0]
            user_type = user[3]

            # Update the password for the user
            cursor.execute("UPDATE Authenticate SET password = %s WHERE p_id = %s", [new_password, p_id])

            # Commit the changes to the database
            connection.commit()

            # Redirect the user to the appropriate dashboard based on their user type
            if user_type == "Customer":
                return redirect('login')
            elif user_type == "Manager":
                return redirect('manHome')
            elif user_type == "Delivery Person":
                return redirect('delHome')

        # If the user does not exist or the provided email is incorrect, show an error message
        messages.error(request, 'Invalid username or email')

    return render(request, 'food_delivery_app/forgot_password.html')

# def search_restaurant(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('search_query')
#         if search_query:
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     """
#                     SELECT * 
#                     FROM Restaurant 
#                     WHERE restaurant_name LIKE %s
#                     """, ['%' + search_query + '%'])
#                 restaurants = cursor.fetchall()
#                 for query in connection.queries:
#                     print(query)
#                 print(restaurants)
#             return render(request, 'food_delivery_app/custHome.html', {'restaurants': restaurants})
#     return redirect('custHome')

def search_restaurant(request):
    if request.method == 'GET':
        name_query = request.GET.get('name_query')
        zip_query = request.GET.get('zip_query')
        if name_query or zip_query:
            with connection.cursor() as cursor:
                query = """
                    SELECT * 
                    FROM Restaurant r
                    JOIN Address a ON r.addr_id_id = a.add_id
                    WHERE """
                params = []
                if name_query:
                    query += "r.restaurant_name LIKE %s"
                    params.append('%' + name_query + '%')
                if name_query and zip_query:
                    query += " AND "
                if zip_query:
                    query += "a.zipcode LIKE %s"
                    params.append('%' + zip_query + '%')
                cursor.execute(query, params)
                restaurants = cursor.fetchall()
                for query in connection.queries:
                    print(query)
                print(restaurants)
            return render(request, 'food_delivery_app/custHome.html', {'restaurants': restaurants})
    return redirect('custHome')

def view_orders(request):
    cursor=connection.cursor()
    username = request.session.get('username')
    password = request.session.get('password')
    cursor.execute( "SELECT `Authenticate`.`p_id`, `Authenticate`.`username`, `Authenticate`.`password`, `Authenticate`.`user_type` FROM `Authenticate` WHERE (`Authenticate`.`password` = %s AND `Authenticate`.`username` = %s)",(password,username))
    user = cursor.fetchone()
    p_id=user[0]
    cursor.execute( "SELECT `Customer`.`customer_id`, `Customer`.`f_name`, `Customer`.`l_name`, `Customer`.`email` FROM `Customer` WHERE (`Customer`.`p_id_id` = %s)",(p_id,))
    customer = cursor.fetchone()
    customer_id=customer[0]
    if request.method == 'GET':
        #customer_id = request.GET.get('customer_id')
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT o.order_id, r.restaurant_name, o.total_price, o.status_val
                FROM Orders o 
                INNER JOIN Restaurant r ON o.restaurant_id_id = r.restaurant_id 
                WHERE o.customer_id_id = %s
                """, [customer_id])
            orders = cursor.fetchall()
            for query in connection.queries:
                print(query)
            print(orders)
        return render(request, 'food_delivery_app/viewOrders.html', {'orders': orders})
    return redirect('custHome')

# def restaurant_analytics(request):
#     # Get the restaurant ID from the user session or URL parameter
#     restaurant_id = request.session.get('restaurant_id')

#     # Calculate average delivery time
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT AVG(timeArrival - timeDispatch) AS avg_delivery_time
#             FROM Delivery d
#             INNER JOIN Orders o ON d.orderId_id = o.order_id
#             WHERE o.restaurant_id_id = %s AND timeArrival IS NOT NULL;
#         ''', [restaurant_id])
#         row = cursor.fetchone()
#         avg_delivery_time = row[0] if row and row[0] else None

#     # Get the most sold product
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT p.item_name, SUM(op.quantity) AS total_quantity
#             FROM orderProducts op
#             INNER JOIN Product p ON op.product_id_id = p.product_id
#             INNER JOIN Orders o ON op.order_id_id = o.order_id
#             WHERE o.restaurant_id_id = %s
#             GROUP BY p.product_id
#             ORDER BY total_quantity DESC
#             LIMIT 1
#         ''', [restaurant_id])
#         row = cursor.fetchone()
#         most_sold_product = row[0] if row and row[0] else None
#         most_sold_quantity = row[1] if row and row[1] else None

#     # Get the number of orders and total revenue
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT COUNT(*) AS num_orders, SUM(total_price) AS total_revenue
#             FROM Orders
#             WHERE restaurant_id_id = %s AND status_val = 'Delivered'
#         ''', [restaurant_id])
#         row = cursor.fetchone()
#         num_orders = row[0] if row and row[0] else None
#         total_revenue = row[1] if row and row[1] else None

#     # Calculate productivity (orders per hour)
#     if num_orders and total_revenue:
#         with connection.cursor() as cursor:
#             cursor.execute('''
#                 SELECT EXTRACT(EPOCH FROM (MAX(ordered_on) - MIN(ordered_on))) AS time_diff
#                 FROM Orders
#                 WHERE restaurant_id_id = %s AND status_val = 'Delivered'
#             ''', [restaurant_id])
#             row = cursor.fetchone()
#             time_diff = row[0] if row and row[0] else None

#         if time_diff:
#             hours_diff = time_diff / 3600
#             productivity = num_orders / hours_diff
#         else:
#             productivity = None
#     else:
#         productivity = None

#     return render(request, 'restaurant_analytics.html', {
#         'avg_delivery_time': avg_delivery_time,
#         'most_sold_product': most_sold_product,
#         'most_sold_quantity': most_sold_quantity,
#         'num_orders': num_orders,
#         'total_revenue': total_revenue,
#         'productivity': productivity,
#     })

def restaurant_analytics(request, restaurant_id):
    # Average delivery time
    with connection.cursor() as cursor:
        cursor.execute('''SELECT AVG(timeArrival - timeDispatch) AS avg_delivery_time
        FROM Delivery d
        INNER JOIN Orders o ON d.orderId_id = o.order_id
        WHERE o.restaurant_id_id = %s AND timeArrival IS NOT NULL;''', [restaurant_id])
        avg_delivery_time = cursor.fetchone()[0] or 0

    # Productivity
    with connection.cursor() as cursor:
        cursor.execute('''SELECT COUNT(*)/(DATEDIFF(NOW(), MIN(ordered_on))+1) AS productivity
                          FROM Orders
                          WHERE restaurant_id_id = %s AND status_val = 'Delivered' ''', [restaurant_id])
        productivity = cursor.fetchone()[0] or 0

    # Most sold product
    with connection.cursor() as cursor:
        cursor.execute('''SELECT p.item_name, SUM(op.quantity) AS quantity
                          FROM orderProducts op
                          INNER JOIN Product p ON op.product_id_id = p.product_id
                          INNER JOIN Orders o ON op.order_id_id = o.order_id
                          WHERE o.restaurant_id_id = %s AND o.status_val = 'Delivered'
                          GROUP BY p.product_id
                          ORDER BY quantity DESC
                          LIMIT 1''', [restaurant_id])
        most_sold_product = cursor.fetchone()
        if most_sold_product:
            most_sold_product_name, most_sold_product_quantity = most_sold_product
        else:
            most_sold_product_name, most_sold_product_quantity = '-', 0

    # Average time taken to prepare an order
    # with connection.cursor() as cursor:
    #     cursor.execute('''SELECT AVG(EXTRACT(EPOCH FROM (o.time_of_preparation - o.ordered_on))) AS avg_preparation_time
    #                       FROM Orders o
    #                       WHERE o.restaurant_id_id = %s AND o.status_val = 'Delivered' AND o.time_of_preparation IS NOT NULL''', [restaurant_id])
    #     avg_preparation_time = cursor.fetchone()[0] or 0

    context = {
        'avg_delivery_time': avg_delivery_time,
        'productivity': productivity,
        'most_sold_product_name': most_sold_product_name,
        'most_sold_product_quantity': most_sold_product_quantity,
        
    }
    return render(request, 'food_delivery_app/restaurant_analytics.html', context=context)