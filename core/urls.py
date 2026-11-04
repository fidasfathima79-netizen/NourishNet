
from django.urls import path

from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Donations
    path(
        'donations/create/',
        views.create_donation,
        name='create_donation'
    ),

    path(
        'donations/my/',
        views.my_donations,
        name='my_donations'
    ),

    path(
        'donations/<int:donation_id>/',
        views.donation_detail,
        name='donation_detail'
    ),
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'donor-dashboard/',
        views.donor_dashboard,
        name='donor_dashboard'
    ),

    path(
        'ngo-dashboard/',
        views.ngo_dashboard,
        name='ngo_dashboard'
    ),
    path(
    'donations/<int:donation_id>/reserve/',
    views.reserve_donation,
    name='reserve_donation'
    ),
    path(
        'ngo/my-reservations/',
        views.ngo_my_reservations,
        name='ngo_my_reservations'
    ),
    path(
    'donor/my-reservations/',
    views.donor_reservations,
    name='donor_reservations'
    ),
path(
    'donations/reservation/<int:reservation_id>/collected/',
    views.mark_as_collected,
    name='mark_as_collected'
),
path('admin-users/', views.admin_users, name='admin_users'),
path('admin-users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
path(
    'admin-users/<int:user_id>/toggle-status/',
    views.toggle_user_status,
    name='toggle_user_status'
),

path('admin-donations/', views.admin_donations, name='admin_donations'),
path(
    'admin-reservations/',
    views.admin_reservations,
    name='admin_reservations'
),

path(
    'donations/<int:donation_id>/edit/',
    views.update_donation,
    name='update_donation'
),

path(
    'donations/<int:donation_id>/delete/',
    views.delete_donation,
    name='delete_donation'
),

path('api/donations/', views.api_available_donations, name='api_available_donations'),
]
