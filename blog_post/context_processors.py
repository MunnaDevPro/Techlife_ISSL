from django.shortcuts import render , redirect , get_object_or_404

from blog_post.models import Category

# def all_category_view(request):
#     category = Category.objects.all()
#     context = {
#         "category": category,
#     }
#     return(context) 


def all_category_view(request):
    return{
        "categories": Category.objects.all()
    }