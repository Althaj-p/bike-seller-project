from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.user_login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.user_logout,name='logout'),
    path('companies',views.companies,name='companies'),
    path('companies/<str:slug>',views.companiesview,name='companiesview'),
    path('companies/<str:cat_slug>/<str:prod_slug>',views.bike_view,name='bike_view'),
    path('bikes',views.all_bikes,name='bikes'),
    path('view_order',views.view_order,name='view_order'),
    path('place_order/<int:pid>',views.place_order,name='place_order'),
    path('apishow',views.apishow,name='apishow'),
    path('delete_order/<int:bid>',views.delete_order,name="delete_order"),
    path('add_bikes',views.add_bikes,name="add_bikes"),
    path('add_company',views.add_comapny,name="add_company"),
    path('add_type',views.add_type,name="add_type"),
    path('view_datail/<str:name>',views.view_detail,name="view_detail"),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_user',views.edit_user,name='edit_user'),
    path('change_password',views.change_password,name='change_password'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_navigation',views.admin_navigation,name='admin_navigation'),
    path('admin_order',views.admin_order,name='admin_order'),
    path('change_status/<int:pid>',views.change_status,name='change_status'),
    path('admin_deleteorder/<int:id>',views.admin_deleteorder,name="admin_deleteorder"),
    path('admin_orderdetail/<int:id>',views.admin_orderdetail,name='admin_orderdetail'),
    path('admin_allCustomer',views.admin_allCustomer,name='admin_allCustomer'),
    path('admin_deleteCustomer/<int:id>',views.admin_deleteCustomer,name='admin_deleteCustomer'),
    path('admin_viewBikes',views.admin_viewBikes,name='admin_viewBikes'),
    path('admin_bikedetail/<str:name>',views.admin_bikedetail,name="admin_bikedetail"),
    path('admin_deleteBike/<int:id>',views.admin_deleteBike,name='admin_deleteBike'),
    path('admin_allCompany',views.admin_allCompany,name='admin_allCompany'),
    path('admin_deleteCompany/<int:id>',views.admin_deleteCompany,name='admin_deleteCompany'),
    path('admin_allTypes',views.admin_allTypes,name='admin_allTypes'),
    path('admin_deleteType/<int:id>',views.admin_deleteType,name='admin_deleteType'),
    path('pending_orders',views.pending_orders,name='pending_orders'),
    path('accepted_orders',views.accepted_orders,name='accepted_orders'),
    path('rejected_orders',views.rejected_orders,name='rejected_orders'),
    path('admin_editbikes/<int:id>',views.admin_editbikes,name='admin_editbikes'),
    path('search',views.search,name='search'),
    path('about_us',views.about_us,name='about_us'),
    path('contact_us',views.contact_us,name='contact_us')




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
