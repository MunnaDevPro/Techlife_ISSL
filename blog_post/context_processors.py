from django.shortcuts import render , redirect , get_object_or_404

from blog_post.models import Category

# def all_category_view(request):
#     category = Category.objects.all()
#     context = {
#         "category": category,
#     }
#     return(context) 

from datetime import datetime

def all_category_view(request):
    
    now = datetime.now()
    
    # %A: পূর্ণাঙ্গ দিনের নাম (e.g., Saturday)
    # %B: পূর্ণাঙ্গ মাসের নাম (e.g., October)
    # %d: দিনের সংখ্যা (e.g., 25)
    # %Y: পূর্ণাঙ্গ বছর (e.g., 2025)
    formatted_date = now.strftime("%A, %B %d, %Y")
    
    return{
        'current_date': formatted_date,
        "categories": Category.objects.all()
    }