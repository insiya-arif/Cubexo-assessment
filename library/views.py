from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, send_mass_mail
from django.utils import timezone
from .models import CustomUser, Book, ReadingList, OTP
import random
from datetime import timedelta

# Create your views here.

def landing(request):
       return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        if 'otp' in request.POST:
            otp_code = request.POST['otp']
            email = request.session.get('signup_email')
            otp = OTP.objects.filter(code=otp_code, user_email=email).first()
            if otp and otp.expires_at > timezone.now():
                #since user is verified, store its data
                user = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    password=request.session['signup_password'],
                    first_name=request.session['signup_first_name'],
                    last_name=request.session['signup_last_name'],
                    is_verified=True
                )
                OTP.objects.filter(user_email=email).delete()
                #clearing up space (beacuase we dont need session data anymore)
                for key in ['signup_email', 'signup_password', 'signup_first_name', 'signup_last_name']:
                    request.session.pop(key, None)
                login(request, user)
                return redirect('dashboard')
            return render(request, 'verify_otp.html', {'error': 'Invalid or expired OTP', 'email': email})
        else:
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'Email already exists'})
            #session details
            request.session['signup_email'] = email
            request.session['signup_password'] = password
            request.session['signup_first_name'] = first_name
            request.session['signup_last_name'] = last_name
            #generating OTP and sending 
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(
                user_email=email,
                code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=10)
            )
            try:
                send_mail(
                    'Verify Your Email',
                    f'Your OTP is {otp_code}. It is valid for 10 minutes.',
                    'insiya.edu@gmail.com',  
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return render(request, 'signup.html', {'error': f'Failed to send OTP: {str(e)}'})
            return render(request, 'verify_otp.html', {'email': email})
    return render(request, 'signup.html')

def resend_otp(request):
    if request.method == 'POST':
        email = request.session.get('signup_email')
        if not email:
            return redirect('signup')
        #getting latest otp
        otp = OTP.objects.filter(user_email=email).order_by('-created_at').first()
        if otp:
            #reusing old otp + resetting time
            otp_code = otp.code
            otp.expires_at = timezone.now() + timedelta(minutes=10)
            otp.save()
        else:
            #create a new otp (for fallback, shouldn't happen in normal flow)
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(
                user_email=email,
                code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=10)
            )
        try:
            send_mail(
                'Verify Your Email',
                f'Your OTP is {otp_code}. It is valid for 10 minutes.',
                'insiya.edu@gmail.com',  
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return render(request, 'verify_otp.html', {'error': f'Failed to resend OTP: {str(e)}', 'email': email})
        return render(request, 'verify_otp.html', {'message': 'OTP resent', 'email': email})
    return redirect('signup')



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_verified:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials or unverified email'})
    return render(request, 'login.html')

def dashboard(request):
    books = Book.objects.all()
    return render(request, 'dashboard.html', {'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        ReadingList.objects.get_or_create(user=request.user, book=book)
        return redirect('book_detail', book_id=book_id)
    return render(request, 'book_detail.html', {'book': book})

def reading_list(request):
    reading_list = ReadingList.objects.filter(user=request.user)
    return render(request, 'reading_list.html', {'reading_list': reading_list})

@staff_member_required
def staff_dashboard(request):
    books = Book.objects.all()
    if request.method == 'POST':
        if 'add_book' in request.POST:
            title = request.POST['title']
            description = request.POST['description']
            image = request.FILES['image']
            book = Book.objects.create(title=title, description=description, image=image)
            users = CustomUser.objects.filter(is_verified=True)
            emails = [
                (
                    f'New Book Added: {book.title}',
                    f'A new book "{book.title}" has been added to the library.',
                    'from@example.com',
                    [user.email]
                ) for user in users
            ]
            send_mass_mail(emails, fail_silently=True)
        elif 'edit_book' in request.POST:
            book_id = request.POST['book_id']
            book = Book.objects.get(id=book_id)
            book.title = request.POST['title']
            book.description = request.POST['description']
            if 'image' in request.FILES:
                book.image = request.FILES['image']
            book.save()
        elif 'delete_book' in request.POST:
            book_id = request.POST['book_id']
            Book.objects.get(id=book_id).delete()
        return redirect('staff_dashboard')
    return render(request, 'staff_dashboard.html', {'books': books})

