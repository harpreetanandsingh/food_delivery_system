from django.contrib import admin

# Register your models here.
from .models import Customer,Restaurant,Orders,orderProducts,Product,deliveryPersonnel,Address,CustAddress,CustNos,restPhNos,Authenticate,Delivery,Payment,Manager,ManNos,restaurantPersonnel
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Orders)
admin.site.register(orderProducts)
#admin.site.register(Status)
admin.site.register(Product)
admin.site.register(deliveryPersonnel)
admin.site.register(Address)
admin.site.register(CustAddress)
admin.site.register(CustNos)
#admin.site.register(RestAddress)
admin.site.register(restPhNos)
#admin.site.register(personnelAddr)
#admin.site.register(Review)
admin.site.register(Authenticate)
admin.site.register(Delivery)
admin.site.register(Manager)
# admin.site.register(payInfo)
admin.site.register(Payment)
admin.site.register(ManNos)
# admin.site.register(Category)
# admin.site.register(Product_categ)
#admin.site.register(availability)
admin.site.register(restaurantPersonnel)