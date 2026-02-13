from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile


def home(request):
    return render(request, 'home.html')


# ---------------- SIGNUP ----------------
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        designation = request.POST.get('designation', 'Not set')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # ✅ Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # ✅ Create profile ONLY ONCE
        UserProfile.objects.get_or_create(
            user=user,
            defaults={"designation": designation}
        )

        messages.success(request, "Signup successful. Please login.")
        return redirect('login')

    return render(request, 'signup.html')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)

            # ADMIN
            if user.is_staff or user.is_superuser:
                return redirect('student_list')
            else:
                return redirect('profile_dashboard')

        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'login.html')


# ---------------- PROFILE DASHBOARD ----------------
@login_required
def profile_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"designation": "Not set"}
    )
    return render(request, 'profile_dashboard.html', {'profile': profile})


# ---------------- EDIT PROFILE ----------------
@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={"designation": "Not set"}
    )

    if request.method == "POST":
        request.user.first_name = request.POST.get('name')

        designation = request.POST.get('designation')

        # ✅ never allow empty designation
        if designation:
            profile.designation = designation.strip()

        age = request.POST.get('age')
        profile.age = int(age) if age else None

        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']

        request.user.save()
        profile.save()
        return redirect('profile_dashboard')

    return render(request, 'edit_profile.html', {'profile': profile})




# ---------------- LOGOUT ----------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CourseSelection

@login_required
def course_page(request):
    if request.method == "POST":
        course = request.POST.get("course")
        fee = request.POST.get("fee")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        CourseSelection.objects.create(
            user=request.user,
            course=course,
            fee=fee,
            from_date=from_date,
            to_date=to_date
        )

        return redirect("course_page")

    return render(request, "course.html")
