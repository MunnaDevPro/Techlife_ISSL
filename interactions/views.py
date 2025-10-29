from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Share
from blog_post.models import BlogPost


# for share section using ajax request handle

@csrf_exempt
@require_POST
def share_post(request):
    post_id = request.POST.get('post_id')
    platform = request.POST.get('platform')

    if not post_id or not platform:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    try:
        post = BlogPost.objects.get(id=post_id)
        user = request.user if request.user.is_authenticated else None
        Share.objects.create(post=post, platform=platform, user=user)
        return JsonResponse({'status': 'success'})
    except BlogPost.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'})
