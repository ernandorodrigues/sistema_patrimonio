from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('manage_order_of_service/', views.manage_order_of_service, name='manage-order-of-service'),
    path('manage_order_of_service/<int:pk>/', views.manage_order_of_service, name='manage-order-of-service'),
    path('order_of_service_list/', views.order_of_service_list, name='order-of-service-list'),
    path('view_order_details/<int:pk>/', views.view_order_details, name='view-order-details'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete-order'),
    path('', views.home),
    path('login', views.login_page, name='login-page'),
    path('user_login', views.login_user, name='login-user'),
    path('home', views.home, name='home-page'),
    path('logout', views.logout_user, name='logout'),
    path('employee_list', views.employee_list, name='employee-page'),
    path('add_employee', views.manage_employee, name='add-employee'),
    path('edit_employee/<int:pk>', views.manage_employee, name='edit-employee'),
    path('save_employee', views.save_employee, name='save-employee'),
    path('view_card/<int:pk>', views.view_card, name='view-card'),
    path('view_details/<str:code>', views.view_details, name='view-details'),
    path('view_details', views.view_details, name='scanned-code'),
    path('scanner', views.view_scanner, name='view-scanner'),
    path('delete_employee/<int:pk>', views.delete_employee, name='delete-employee'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
