from django.urls import path     
from . import views

urlpatterns = [
    path('', views.drift),
    path('rate_me/home', views.home, name='home'),
    path('rate_me/registration',views.registration),
    path('rate_me/register',views.register),
    path('rate_me/log_in',views.log_in),
    path('rate_me/login',views.login),
    path('rate_me/logout', views.logout),
    path('rate_me/company/<int:id>',views.category),
    path('rate_me/type/<int:id>',views.item),
    path('rate_me/profile/<int:id>', views.check),
    path('check/<int:id>', views.check),
    path('user/<int:id>', views.user),
    path('admin/<int:id>', views.admin),
    path('rate/<int:item_id>', views.rate),
    path('deleteit/<int:id_item>/<int:id_review>', views.deleteit),
    path('makeadmin/<int:id1>', views.makeadmin),
    path('deleteuser/<int:id1>', views.makeadmin),
    path('upload', views.upload),
    path('update/<int:id>',views.update),
    path('deletetype/<int:id>',views.deletetype),
    path('uploadtype/<int:id>',views.uploadtype),
    path('search', views.search),
    
    
]