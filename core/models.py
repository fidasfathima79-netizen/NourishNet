
from django.db import models
from django.contrib.auth.models import AbstractUser


# --------------------------------------------------
# CUSTOM USER MODEL
# --------------------------------------------------

class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DONOR', 'Donor'),
        ('NGO', 'NGO'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='DONOR'
    )

    def __str__(self):
        return f"{self.username} - {self.role}"


# --------------------------------------------------
# FOOD DONATION MODEL
# --------------------------------------------------

class Donation(models.Model):

    FOOD_TYPE_CHOICES = [
        ('COOKED', 'Cooked Meals'),
        ('BAKERY', 'Bakery & Bread'),
        ('VEGETABLES', 'Vegetables & Fruits'),
        ('PACKAGED', 'Packaged Food'),
        ('DAIRY', 'Dairy Products'),
        ('OTHER', 'Other'),
    ]

    DIET_CHOICES = [
        ('VEGETARIAN', 'Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('NON_VEGETARIAN', 'Non-Vegetarian'),
        ('ANY', 'Any'),
    ]

    UNIT_CHOICES = [
        ('KG', 'Kilograms'),
        ('LITRE', 'Litres'),
        ('PORTIONS', 'Portions'),
        ('PIECES', 'Pieces'),
        ('PACKETS', 'Packets'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('COLLECTED', 'Collected'),
        ('EXPIRED', 'Expired'),
    ]

    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donations'
    )

    title = models.CharField(max_length=200)

    food_type = models.CharField(
        max_length=20,
        choices=FOOD_TYPE_CHOICES
    )

    dietary_suitability = models.CharField(
        max_length=20,
        choices=DIET_CHOICES,
        default='ANY'
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES
    )

    description = models.TextField()

    allergens = models.CharField(
        max_length=300,
        blank=True
    )

    food_image = models.ImageField(
        upload_to='donations/',
        blank=True,
        null=True
    )

    use_by = models.DateTimeField()

    collection_location = models.CharField(
        max_length=300
    )

    collection_start = models.DateTimeField()

    collection_end = models.DateTimeField()

    contact_person = models.CharField(
        max_length=150
    )

    contact_phone = models.CharField(
        max_length=20
    )

    collection_instructions = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Reservation(models.Model):

    STATUS_CHOICES = [
    ('CONFIRMED', 'Confirmed'),
    ('COLLECTED', 'Collected'),
    ('CANCELLED', 'Cancelled'),
    ]
    

    donation = models.OneToOneField(
        Donation,
        on_delete=models.CASCADE,
        related_name='reservation'
    )

    ngo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='CONFIRMED'
    )

    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ngo.username} - {self.donation.title}"

    class Meta:
        ordering = ['-reserved_at']
