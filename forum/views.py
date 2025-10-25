from django.shortcuts import render
from blog_post.models import BlogPost

def questions(request):
    blogs = BlogPost.objects.all()
    context = {"blogs":blogs}
    if request.headers.get('HX-Request'):
        return render(request, "forum/partial_question.html",context)
    return render(request, "forum/question_page.html",context)


def questions_list(request):
    blogs = BlogPost.objects.all()
    context = {"blogs":blogs}
    return render(request, "forum/all_question.html", context)
