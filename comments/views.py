from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Assuming these models are available in the project
from .models import Comment, Reply
from blog_post.models import BlogPost 
from django.contrib.auth.decorators import login_required

# --- Helper Function (Content Split) ---

def process_blog_content(blog):
    """Blog content ke 50 words and remaining words e split kore."""
    # Assuming the BlogPost model has a 'description' field
    if hasattr(blog, 'description') and blog.description:
        content = blog.description.split()
        return {
            'first_50_words': ' '.join(content[:50]),
            'remaining_words': ' '.join(content[50:]),
        }
    return {'first_50_words': '', 'remaining_words': ''}

# --- Main Blog Detail View ---

def blog_detail_view(request, slug):
    """
    Blog details page er main content render kore.
    Eta full page load and HTMX partial update du-to-i handle korbe.
    """
    blog = get_object_or_404(BlogPost, slug=slug)
    current_user = request.user if request.user.is_authenticated else None
    
    # Content splitting kora holo
    content_parts = process_blog_content(blog)
    
    context = {
        'blog': blog,
        'first_50_words': content_parts['first_50_words'],
        'remaining_words': content_parts['remaining_words'],
        'user': current_user,
        # Apnar chaoa 'action' variable
        'action' : 'right_side_update_in_blog_details' 
    }
    
    # Ekhon HTMX header check kora holo
    if request.headers.get("HX-Request"):
        # Jodi HTMX request thake, shudhu partial content pathano hobe
        return render(request, "components/blog_details/blog_right_side_partial.html", context)
        
    # Full page load-er jonno main template pathano hobe
    return render(request, "components/blog_details/blog_right_side.html", context) 

# --- HTMX Interaction Views (Comment and Reply - No change needed here) ---

@login_required
def post_comment(request, slug):
    """
    Notun comment post kore ebong HTMX er jonno single comment partial return kore.
    """
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip() 
        
        if content:
            comment = Comment.objects.create(
                post=blog,
                user=request.user,
                content=content
            )
            
            # HTMX Response: Notun comment-ti render kore HTML partial pathano holo
            context = {'comment': comment, 'blog': blog, 'user': request.user}
            
            # Ekhane 'components/blogs/comment_single_partial.html' use kora holo (jemon amra aage fix korechi)
            return render(request, 'components/blogs/comment_single_partial.html', context)
        
        return HttpResponse(status=204) # 204 No Content

    return redirect('blog_post:detail', slug=slug)

@login_required
def post_reply(request, comment_id):
    """
    Kono comment er upor reply post kore ebong HTMX er jonno single reply partial return kore.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if content:
            reply = Reply.objects.create(
                comment=comment,
                user=request.user,
                content=content
            )
            
            # HTMX Response: Notun reply-ti render kore HTML partial pathano holo
            context = {'reply': reply, 'user': request.user}
            # Ekhane 'components/blogs/reply_single_partial.html' use kora holo (jemon amra aage fix korechi)
            return render(request, 'components/blogs/reply_single_partial.html', context)
        
        return HttpResponse(status=204)

    return redirect('blog_post:detail', slug=comment.post.slug)
