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
    path('companies/<str:cat_slug/prod_slug>',views.bike_view,name='bike_view'),
    path('bikes',views.all_bikes,name='bikes'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
