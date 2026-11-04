from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Donation, Reservation


# Custom User Admin
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('NourishNet Role', {
            'fields': ('role',),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('NourishNet Role', {
            'fields': ('role',),
        }),
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
    )


admin.site.register(User, CustomUserAdmin)


# Donation Admin
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'donor',
        'food_type',
        'quantity',
        'unit',
        'status',
        'use_by',
    )

    list_filter = ('status', 'food_type')
    search_fields = ('title', 'donor__username')


# Reservation Admin
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'donation',
        'ngo',
        'status',
        'reserved_at',
    )

    list_filter = ('status',)
    search_fields = ('donation__title', 'ngo__username')