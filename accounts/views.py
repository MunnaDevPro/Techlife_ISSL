from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserSignupForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from django.http import HttpResponse
from accounts.utils import send_password_reset_email, send_verification_email
from accounts.models import CustomUserModel

from blog_post.models import BlogPost

from blog_post.models import BlogPost
from comments.models import Comment
from django.db.models import Sum,Count

from earnings.models import EarningSetting

def signup_form(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save()
            # send_verification_email(request, user)  # your email function
            messages.success(
                request, "Account created. Check your email for verification."
            )
            return redirect("homepage")  # or redirect to homepage
        else:
            # helpful for debugging server logs
            print("SIGNUP form errors:", form.errors.as_json())
            return render(request, "account/register_page.html", {"form": form})
    else:
        form = CustomUserSignupForm()
        return render(request, "account/register_page.html", {"form": form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("signup")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Invalid username or password.")
        elif not user.is_verified:
            messages.error(request, "Your email is not verified yet.")
        else:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("homepage")

    return render(request, "account/login_page.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


 

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("password-reset")

        send_password_reset_email(request, user)
        messages.info(
            request, "We have sent you an email with password reset instructions"
        )
        return redirect("login")

    return render(request, "accounts/forget.html")


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect("new-password")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("login")


@login_required
def set_new_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, "Password updated successfully.")
        return redirect("profile")
    return render(request, "accounts/new-password.html")


def contact_us_view(request):
    # Check if it's an HTMX request
    if request.headers.get('HX-Request'):
        # Return only the content without base layout
        return render(request, "contact_us_content.html")
    
    # Return full page with base layout
    return render(request, "contact_us_page.html")




# User dashboard section
@login_required

def user_dashboard_view(request):
    user = request.user

    user_posts = BlogPost.objects.filter(author=user).select_related('author').prefetch_related('comments')
    
    total_likes = user_posts.aggregate(total=Sum('likes'))['total'] or 0
    total_views = user_posts.aggregate(total=Sum('views'))['total'] or 0
    total_quality = user_posts.aggregate(total=Sum('content_quality'))['total'] or 0

    comment_count = Comment.objects.filter(post__author=user).count()
    reply_count = Comment.objects.filter(post__author=user).annotate(
        num_replies=Count('replies')
    ).aggregate(total_replies=Sum('num_replies'))['total_replies'] or 0
    total_comments = comment_count + reply_count




    # earning section logic
    earning = EarningSetting.objects.first()  

    post_point = earning.quality_rate * total_quality

    others_point = (
        total_views * earning.view_rate +
        total_likes * earning.like_rate +
        total_comments * earning.comment_rate
    )

    total_point = post_point + others_point


    # badge section
    badge_level  = ""
    if (1<total_point<=50):
        badge_level +="Bronze"
    elif (50<total_point<=80):
        badge_level +="Silver"
    elif (80<total_point<=120):
        badge_level +="Gold"
    elif (120<total_point<=150):
        badge_level +="Platinum"
    elif (150<total_point<=200):
        badge_level +="Diamond"
    elif (200<total_point<=250):
        badge_level +="Master"
    elif (250<total_point<=300):
        badge_level +="Legend"
    elif total_point > 300:
        badge_level  += "Grand Master"   


    context = {
        "user": user,
        "user_posts": user_posts,
        "total_views": total_views,
        "total_comments": total_comments,
        "total_likes" : total_likes,
        "others_point" : others_point,
        "post_point" : post_point,
        "total_point" : total_point,
        "badge_level" : badge_level,
       
    }

    return render(request, "account/user_dashboard.html", context)



