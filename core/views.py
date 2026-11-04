
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, IntegrityError
from .forms import UserRegistrationForm, DonationForm
from .models import User, Donation,Reservation
from django.db.models import Q
from django.http import JsonResponse

# =====================================================
# HOME PAGE
# =====================================================

def home(request):
    return render(request, 'home.html')


# =====================================================
# USER REGISTRATION
# =====================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Your NourishNet account has been created successfully. Please log in.'
            )

            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# =====================================================
# USER LOGIN
# =====================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f'Welcome to NourishNet, {user.first_name or user.username}!'
            )

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password. Please try again.'
        )

    return render(
        request,
        'accounts/login.html'
    )


# =====================================================
# USER LOGOUT
# =====================================================

@login_required
def logout_view(request):

    if request.method != 'POST':
        return redirect('dashboard')

    logout(request)

    messages.success(
        request,
        'You have logged out successfully.'
    )

    return redirect('login')


# =====================================================
# ROLE-BASED DASHBOARD REDIRECTION
# =====================================================

@login_required
def dashboard(request):

    if request.user.is_superuser or request.user.role == 'ADMIN':
        return redirect('admin_dashboard')

    elif request.user.role == 'DONOR':
        return redirect('donor_dashboard')

    elif request.user.role == 'NGO':
        return redirect('ngo_dashboard')

    else:
        messages.error(request, 'Invalid user role.')
        logout(request)
        return redirect('login')


# =====================================================
# CREATE FOOD DONATION
# =====================================================

@login_required
def create_donation(request):

    if request.user.role != 'DONOR':
        messages.error(
            request,
            'Only registered food donors can publish donations.'
        )
        return redirect('dashboard')

    if request.method == 'POST':

        form = DonationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()

            messages.success(
                request,
                'Your food donation has been published successfully!'
            )

            return redirect('my_donations')

    else:
        form = DonationForm()

    return render(
        request,
        'donations/create_donation.html',
        {'form': form}
    )


# =====================================================
# DONOR - MY DONATIONS
# =====================================================

@login_required
def my_donations(request):

    if request.user.role != 'DONOR':
        messages.error(
            request,
            'You do not have permission to view this page.'
        )
        return redirect('dashboard')

    donations = Donation.objects.filter(
        donor=request.user
    ).order_by('-created_at')

    return render(
        request,
        'donations/my_donations.html',
        {'donations': donations}
    )


# =====================================================
# DONATION DETAILS
# =====================================================

@login_required
def donation_detail(request, donation_id):

    donation = get_object_or_404(
        Donation,
        id=donation_id
    )

    if (
        request.user.role != 'ADMIN'
        and not request.user.is_superuser
        and donation.donor != request.user
    ):
        messages.error(
            request,
            'You cannot access this donation.'
        )
        return redirect('dashboard')

    return render(
        request,
        'donations/donation_detail.html',
        {'donation': donation}
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@login_required
def admin_dashboard(request):

    # Allow only administrators
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # User statistics
    total_users = User.objects.filter(is_active=True).count()

    total_donors = User.objects.filter(
        role='DONOR',
        is_active=True
    ).count()

    total_ngos = User.objects.filter(
        role='NGO',
        is_active=True
    ).count()

    # Donation statistics
    total_donations = Donation.objects.count()

    available_donations = Donation.objects.filter(
        status='AVAILABLE'
    ).count()

    reserved_donations = Donation.objects.filter(
        status='RESERVED'
    ).count()

    collected_donations = Donation.objects.filter(
        status='COLLECTED'
    ).count()

    # Reservation statistics
    total_reservations = Reservation.objects.count()

    confirmed_reservations = Reservation.objects.filter(
        status='CONFIRMED'
    ).count()

    collected_reservations = Reservation.objects.filter(
        status='COLLECTED'
    ).count()

    # Recent activities
    recent_donations = Donation.objects.select_related(
        'donor'
    ).order_by('-created_at')[:5]

    recent_reservations = Reservation.objects.select_related(
        'donation',
        'ngo',
        'donation__donor'
    ).order_by('-reserved_at')[:5]

    context = {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_ngos': total_ngos,

        'total_donations': total_donations,
        'available_donations': available_donations,
        'reserved_donations': reserved_donations,
        'collected_donations': collected_donations,

        'total_reservations': total_reservations,
        'confirmed_reservations': confirmed_reservations,
        'collected_reservations': collected_reservations,

        'recent_donations': recent_donations,
        'recent_reservations': recent_reservations,
    }

    return render(request, 'admin/dashboard.html', context)

# =====================================================
# DONOR DASHBOARD
# =====================================================

@login_required
def donor_dashboard(request):

    if request.user.role != 'DONOR':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    donations = Donation.objects.filter(
        donor=request.user
    ).order_by('-created_at')

    context = {
        'donations': donations[:5],
        'total_donations': donations.count(),
    }

    return render(
        request,
        'donor/dashboard.html',
        context
    )


# =====================================================
# NGO DASHBOARD
# =====================================================



@login_required
def ngo_dashboard(request):

    if request.user.role != 'NGO':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Get all donations
    all_donations = Donation.objects.all()

    # Get currently available donations
    available_donations = all_donations.filter(
        status='AVAILABLE',
        use_by__gt=timezone.now(),
        collection_end__gt=timezone.now()
    ).select_related('donor').order_by('-created_at')

    # Search & filter (title, description, location, donor name)
    search_query = request.GET.get('q', '').strip()
    selected_food_type = request.GET.get('food_type', '').strip()
    valid_food_types = [c[0] for c in Donation.FOOD_TYPE_CHOICES]

    if search_query:
        available_donations = available_donations.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(collection_location__icontains=search_query)
            | Q(donor__username__icontains=search_query)
        )

    if selected_food_type in valid_food_types:
        available_donations = available_donations.filter(
            food_type=selected_food_type
        )
    else:
        selected_food_type = ''

    # Count food donations collected by this NGO
    food_distribution = Reservation.objects.filter(
        ngo=request.user,
        status='COLLECTED'
    ).count()

    context = {
        'donations': available_donations,
        'total_donations': all_donations.count(),
        'available_donations': available_donations.count(),
        'food_distribution': food_distribution,
        'search_query': search_query,
        'selected_food_type': selected_food_type,
        'food_type_choices': Donation.FOOD_TYPE_CHOICES,
    }

    return render(
        request,
        'ngo/dashboard.html',
        context
    )

# ==========================================
# NGO MY RESERVATIONS
# ==========================================

@login_required
def ngo_my_reservations(request):

    if request.user.role != 'NGO':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    reservations = Reservation.objects.filter(
        ngo=request.user
    ).select_related(
        'donation',
        'donation__donor'
    ).order_by('-reserved_at')

    context = {
        'reservations': reservations,
        'total_reservations': reservations.count(),
    }

    return render(
        request,
        'ngo/my_reservations.html',
        context
    )


@login_required
def reserve_donation(request, donation_id):

    if request.user.role != 'NGO':
        messages.error(request, 'Only NGOs can reserve food donations.')
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('ngo_dashboard')

    try:
        with transaction.atomic():

            donation = Donation.objects.select_for_update().get(
                id=donation_id
            )

            if donation.status != 'AVAILABLE':
                messages.error(
                    request,
                    'Sorry! This donation is no longer available.'
                )
                return redirect('ngo_dashboard')

            if donation.use_by <= timezone.now():
                messages.error(
                    request,
                    'This food donation has expired.'
                )
                return redirect('ngo_dashboard')

            if donation.collection_end <= timezone.now():
                messages.error(
                    request,
                    'The collection period has ended.'
                )
                return redirect('ngo_dashboard')

            Reservation.objects.create(
                donation=donation,
                ngo=request.user
            )

            donation.status = 'RESERVED'
            donation.save(update_fields=['status'])

        messages.success(
            request,
            'Food donation reserved successfully!'
        )

    except Donation.DoesNotExist:
        messages.error(request, 'Donation not found.')

    except IntegrityError:
        messages.error(
            request,
            'This donation has already been reserved.'
        )

    return redirect('ngo_dashboard')
# ==========================================
# DONOR RESERVATION MANAGEMENT
# ==========================================
# ==========================================
# MARK DONATION AS COLLECTED
# ==========================================

@login_required
def mark_as_collected(request, reservation_id):

    if request.user.role != 'DONOR':
        messages.error(
            request,
            'Only donors can confirm food collection.'
        )
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('donor_reservations')

    try:
        with transaction.atomic():

            reservation = Reservation.objects.select_for_update().get(
                id=reservation_id,
                donation__donor=request.user
            )

            if reservation.status != 'CONFIRMED':
                messages.error(
                    request,
                    'This reservation cannot be marked as collected.'
                )
                return redirect('donor_reservations')

            donation = reservation.donation

            reservation.status = 'COLLECTED'
            reservation.save(update_fields=['status'])

            donation.status = 'COLLECTED'
            donation.save(update_fields=['status', 'updated_at'])

        messages.success(
            request,
            'Food collection confirmed successfully!'
        )

    except Reservation.DoesNotExist:
        messages.error(request, 'Reservation not found.')

    return redirect('donor_reservations')
@login_required
def donor_reservations(request):

    if request.user.role != 'DONOR':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    reservations = Reservation.objects.filter(
        donation__donor=request.user
    ).select_related(
        'donation',
        'ngo'
    ).order_by('-reserved_at')

    context = {
        'reservations': reservations,
        'total_reservations': reservations.count(),
    }

    return render(
        request,
        'donor/reservations.html',
        context
    )

@login_required
def admin_users(request):

    # Allow only administrators
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Get all registered users
    users = User.objects.all().order_by('-date_joined')

    # Search users by username, first name, last name or email
    search = request.GET.get('search', '').strip()

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    # Filter users by role
    selected_role = request.GET.get('role', '')

    if selected_role in ['DONOR', 'NGO', 'ADMIN']:
        users = users.filter(role=selected_role)
    else:
        selected_role = ''

    # Overall user statistics
    total_users = User.objects.count()
    total_donors = User.objects.filter(role='DONOR').count()
    total_ngos = User.objects.filter(role='NGO').count()

    # Send data to the template
    context = {
        'users': users,
        'search': search,
        'selected_role': selected_role,
        'total_users': total_users,
        'total_donors': total_donors,
        'total_ngos': total_ngos,
    }

    return render(request, 'admin/users.html', context)


@login_required
def admin_user_detail(request, user_id):
    # Only Admin can access this page
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)

    context = {
        'selected_user': user,
    }

    return render(request, 'admin/user_detail.html', context)

@login_required
def toggle_user_status(request, user_id):

    # Check admin permission
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Allow only POST requests
    if request.method != 'POST':
        return redirect('admin_users')

    selected_user = get_object_or_404(User, id=user_id)

    # Protect the logged-in admin and superuser accounts
    if selected_user.id == request.user.id or selected_user.is_superuser:
        messages.error(request, 'This account cannot be deactivated.')
        return redirect('admin_users')

    # Change account status
    selected_user.is_active = not selected_user.is_active
    selected_user.save(update_fields=['is_active'])

    if selected_user.is_active:
        messages.success(request, 'User account activated successfully.')
    else:
        messages.success(request, 'User account deactivated successfully.')

    return redirect('admin_users')

@login_required
def admin_donations(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    donations = Donation.objects.select_related('donor').all()

    search = request.GET.get('search', '')
    if search:
        donations = donations.filter(
            Q(title__icontains=search) |
            Q(donor__username__icontains=search) |
            Q(collection_location__icontains=search)
        )

    selected_status = request.GET.get('status', '')
    if selected_status:
        donations = donations.filter(status=selected_status)

    context = {
        'donations': donations,
        'search': search,
        'selected_status': selected_status,
        'total_donations': Donation.objects.count(),
        'available_donations': Donation.objects.filter(status='AVAILABLE').count(),
        'reserved_donations': Donation.objects.filter(status='RESERVED').count(),
        'collected_donations': Donation.objects.filter(status='COLLECTED').count(),
    }

    return render(request, 'admin/donations.html', context)

@login_required
def admin_reservations(request):

    # Check admin permission
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    reservations = Reservation.objects.select_related(
        'donation', 'ngo', 'donation__donor'
    ).all()

    # Search reservations
    search = request.GET.get('search', '')

    if search:
        reservations = reservations.filter(
            Q(donation__title__icontains=search) |
            Q(ngo__username__icontains=search) |
            Q(donation__donor__username__icontains=search)
        )

    # Filter by reservation status
    selected_status = request.GET.get('status', '')

    if selected_status:
        reservations = reservations.filter(status=selected_status)

    context = {
        'reservations': reservations,
        'search': search,
        'selected_status': selected_status,
        'total_reservations': Reservation.objects.count(),
        'confirmed_reservations': Reservation.objects.filter(
            status='CONFIRMED'
        ).count(),
        'collected_reservations': Reservation.objects.filter(
            status='COLLECTED'
        ).count(),
        'cancelled_reservations': Reservation.objects.filter(
            status='CANCELLED'
        ).count(),
    }

    return render(request, 'admin/reservations.html', context)

# ==========================================
# EDIT / UPDATE FOOD DONATION
# ==========================================

@login_required
def update_donation(request, donation_id):

    donation = get_object_or_404(Donation, id=donation_id)

    # Allow only donors and administrators
    is_admin = request.user.is_superuser or request.user.role == 'ADMIN'

    if not is_admin and request.user.role != 'DONOR':
        messages.error(request, 'You do not have permission to edit donations.')
        return redirect('dashboard')

    # Donors can edit only their own donations
    if not is_admin and donation.donor != request.user:
        messages.error(request, 'You cannot edit another donor\'s donation.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = DonationForm(
            request.POST,
            request.FILES,
            instance=donation
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Food donation updated successfully!'
            )

            if is_admin:
                return redirect('admin_donations')

            return redirect('my_donations')

    else:
        form = DonationForm(instance=donation)

    return render(
        request,
        'donations/edit_donation.html',
        {'form': form, 'donation': donation}
    )

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    # Only the donor who created the donation can delete it
    if request.user != donation.donor:
        messages.error(request, 'You cannot delete this donation.')
        return redirect('my_donations')

    # Only available donations can be deleted
    if donation.status != 'AVAILABLE':
        messages.error(
            request,
            'Only available donations can be deleted.'
        )
        return redirect('my_donations')

    # Delete only after confirmation through POST
    if request.method == 'POST':
        donation.delete()
        messages.success(
            request,
            'Donation deleted successfully.'
        )
        return redirect('my_donations')

    return render(
        request,
        'donations/delete_donation.html',
        {'donation': donation}
    )


# =====================================================
# REST-STYLE JSON API (read-only, role-restricted)
# =====================================================

@login_required
def api_available_donations(request):
    """
    GET /api/donations/?q=<text>&food_type=<TYPE>
    Returns currently available donations as JSON.
    Only NGO and Admin accounts may use it.
    """

    is_admin = request.user.is_superuser or request.user.role == 'ADMIN'

    if not is_admin and request.user.role != 'NGO':
        return JsonResponse({'error': 'Forbidden'}, status=403)

    now = timezone.now()

    donations = Donation.objects.filter(
        status='AVAILABLE',
        use_by__gt=now,
        collection_end__gt=now
    ).select_related('donor')

    q = request.GET.get('q', '').strip()
    if q:
        donations = donations.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(collection_location__icontains=q)
        )

    food_type = request.GET.get('food_type', '').strip()
    if food_type in [c[0] for c in Donation.FOOD_TYPE_CHOICES]:
        donations = donations.filter(food_type=food_type)

    data = [
        {
            'id': d.id,
            'title': d.title,
            'food_type': d.food_type,
            'dietary_suitability': d.dietary_suitability,
            'quantity': str(d.quantity),
            'unit': d.unit,
            'collection_location': d.collection_location,
            'use_by': d.use_by.isoformat(),
            'collection_start': d.collection_start.isoformat(),
            'collection_end': d.collection_end.isoformat(),
            'donor': d.donor.username,
        }
        for d in donations.order_by('use_by')
    ]

    return JsonResponse({'count': len(data), 'results': data})
