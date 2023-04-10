from django.urls import path,include
from . import views
from food_delivery_app import views


urlpatterns = [
    # path("", views.home,name='site-home'),
    # path("about", views.about,name='site-about'),
    # path("CustHome",views.customer,name="customer"),
    # path("register/", views.register, name="register"),
    path("custlist/", views.customer_list,name='customer_list'),
    path("index/", views.index,name='index'),
    path("userreg/", views.userreg,name='userreg'),
    path("manreg/", views.manreg,name='manreg'),
    path("prodreg/", views.prodreg,name='prodreg'),
    path("delreg/", views.delreg,name='manreg'),
    path("orderreg/", views.orderreg,name='orderreg'),
    path("orderreg/", views.orderreg,name='orderreg'),
    path("edit_cprofile/<int:customer_id>/", views.edit_cprofile,name='edit_cprofile'),
    path("del_view/<int:personnel_id>/", views.del_view,name='del_view'),
    path("item_list/<int:restaurant_id>/", views.item_list,name='item_list'),
    path("order/<int:product_id>/", views.order,name='order'),
    path("login/", views.login,name='login'),
    path("logout/", views.logout,name='logout'),
    path("login2/", views.login2,name='login2'),
    path("custHome/", views.custHome,name='custHome'),
    path("manHome/", views.manHome,name='manHome'),
    path("delHome/", views.delHome,name='delHome'),
    path("insertCustomer/", views.insertCustomer,name='insertCustomer'),
    path("insertManager/", views.insertManager,name='insertManager'),
    path("insertDeliveryPerson/", views.insertDeliveryPerson,name='insertDeliveryPerson'),
    path("insertProduct/", views.insertProduct,name='insertProduct'),


    
]
