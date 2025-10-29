from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from blog_post.models import BlogPost
from .models import SavedPost
import json

@login_required
@require_POST
def save_post(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        if not post_id:
            return JsonResponse({'status': 'error', 'message': 'Post ID is required'})

        post = BlogPost.objects.get(id=post_id)
        saved, created = SavedPost.objects.get_or_create(post=post, user=request.user)

        if created:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'exists'})  # already saved

    except BlogPost.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def check_saved(request, post_id):
    # Check if user already saved the post
    already_saved = SavedPost.objects.filter(post_id=post_id, user=request.user).exists()
    return JsonResponse({'already_saved': already_saved})
