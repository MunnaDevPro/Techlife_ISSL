from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import BlogPost, Category, Review, SubCategory
from .models import BlogPost, BlogAdditionalImage, Category, Tag
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import IntegrityError # Required for handling database constraints
from .models import BlogPost, Like 

from accounts.models import CustomUserModel

from comments.models import Comment
# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from django.views.decorators.http import require_POST
from django.contrib import messages
from blog_post.models import BlogPost, compnay_logo
from comments.models import Comment, Reply

# from save_post.models import SavedPost
# In your app's views.py
from interactions.models import Share
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
# Assuming Share and BlogPost are imported from .models


def blog_details_view(request, slug):
    blog_detail = (
        BlogPost.objects.select_related("category", "author")
        .prefetch_related("reviews", "additional_images", "tags", "likes")
        .get(slug=slug, status="published")
    )
    
    related_news = BlogPost.objects.filter(
        status="published", category=blog_detail.category
    ).exclude(slug=slug)[:10]
    
    if blog_detail.description:
        word_count = len(blog_detail.description.split())
    else:
        word_count = 0 


    
    
    # most_viewed blog
    most_viewed_blogs = BlogPost.objects.filter(status="published").order_by("-views")


    # all comment section
    all_comments = (
        Comment.objects
        .filter(post=blog_detail) 
        .select_related("user", "post")  
        .prefetch_related("replies__user")
        .order_by("-created_at")
    )
    
    
   # total comment count (reply+main commnet) - এটি গণনা ঠিক আছে
    comment_count = all_comments.count() # এখন শুধু প্রধান কমেন্ট গণনা হবে
    reply_count = sum(comment.replies.count() for comment in all_comments)
    total_comments = comment_count + reply_count
    
    # --- Paginator Setup (এখন সঠিক কোয়েরির উপর চলবে) ---
    paginator = Paginator(all_comments, 5) 
    page_number = request.GET.get('page', 1) 
    try:
        page_obj = paginator.page(page_number)
    except Exception:
        # Invalid page number, deliver last page
        page_obj = paginator.page(paginator.num_pages)
    
    
    # sort by comment
    sort_by = request.GET.get('sort_by', 'newest')
    comment_order = '-created_at'

    if sort_by == 'oldest':
        comment_order = 'created_at'
    elif sort_by == 'recent':
        comment_order = '-updated_at'

    all_comments = Comment.objects.filter(post=blog_detail).order_by(comment_order)
        
        
    
    # user like system check
    user_has_liked = False
    if request.user.is_authenticated:
        try:
            Like.objects.get(post=blog_detail, user=request.user)
            user_has_liked = True
        except Like.DoesNotExist:
            user_has_liked = False
            

    context = {
        "blog_detail": blog_detail,
        "related_news":related_news,
        "word_count":word_count,
        "most_viewed_blogs":most_viewed_blogs,
        "all_comments" : page_obj,
        "total_comments":total_comments,
        "user_has_liked":user_has_liked,
        "sort_by":sort_by,
        # "is_saved" : is_saved,
        "action":"blog_details",
    }
    
    if request.headers.get("HX-Request"):
        return render(request, "components/blog_details/partial_blog_details_page.html", context)
    return render(request, "components/blog_details/blog_details_page.html", context)

    # return render(request, "components/blog_details/demo_blog_detail.html", context)



def home(request):
    """
    Home page view - handles both regular and HTMX requests
    """
    blogs = BlogPost.objects.filter(status="published")[:6]
    latest_blog = (
        BlogPost.objects.filter(status="published").order_by("-created_at").first()
    )
    
    all_category = Category.objects.all()

    # Get top 5 published blogs for carousel
    carousel_blogs = BlogPost.objects.filter(status="published").order_by(
        "-created_at"
    )[:5]

    top_users = CustomUserModel.objects.filter(is_verified=True) \
    .annotate(post_count=Count('authored_posts')) \
    .order_by('-post_count')[:4]

    # category wise 4 ta kore blogs nibo
    technology_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='technology'
    ).order_by("-created_at")[:4]

    news_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='news'
    ).order_by("-created_at")[:4]
    
    tips_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='tips-tricks'
    ).order_by("-created_at")[:4]

    # only latest blogs 
    Only_latest_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")[:1]
    ) 
    
    # latest and popular blogs
    latest_popular_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at", "-views", "-likes")[:8]
    ) 
    
    
    
    # popular category er popular blog gulo nibo, (popular category bolte, jei category er post beshi)
    # 1. Retrieve the top 6 categories based on the count of published posts.
    popular_categories = (
        Category.objects
        .annotate(
            published_post_count=Count(
                'blogpost',
                filter=Q(blogpost__status='published') 
            )
        )
        .filter(published_post_count__gt=0)
        .order_by('-published_post_count')[:7]
    )

    # 2. Prepare a single, flat list of the top blog posts (Latest by Category).
    popular_posts_flat_list = []

    for category in popular_categories:
       
        latest_post = (
            BlogPost.objects
            .filter(category=category, status='published')
            .order_by('-created_at')[:1] 
        )
        
        if latest_post:
            post = latest_post[0]
            
            # Add the post entry directly to the flat list
            popular_posts_flat_list.append({
                'title': post.title,
                'created_at':post.created_at,
                'slug': post.slug,
                'views': post.views,
                'author_username': post.author.username,
                'category_name': category.name, 
                'category_icon': category.font_awesome_icon, 
                'featured_image': post.featured_image,
                'featured_image_url': post.featured_image_url,
            })

        
        
    
    # news related post
    news__related_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='news'
    ).order_by("-views","-likes","-created_at")
    
    # technology related post
    Teacnology_related_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='technology'
    ).order_by("-views","-likes","-created_at")

    # programming related post
    programming_related_posts = BlogPost.objects.filter(
        status="published", 
        category__slug='programming'
    ).order_by("-views","-likes","-created_at")



    # Most viewed
    most_viewed_blogs = BlogPost.objects.filter(status="published").order_by("-views")


    #company logo
    company_logo = compnay_logo.objects.all()


    tags = Tag.objects.all()



    context = {
        "blogs": blogs,
        "latest_blog": latest_blog,
        "top_users": top_users,
        "carousel_blogs": carousel_blogs,
        "tags": tags,
        "technology_posts":technology_posts,
        "news_posts":news_posts,
        "tips_posts":tips_posts,
        "Only_latest_blogs":Only_latest_blogs,
        "latest_popular_blogs": latest_popular_blogs,
        "popular_posts_flat_list": popular_posts_flat_list,
        "news__related_posts":news__related_posts,
        "Teacnology_related_posts":Teacnology_related_posts,
        "programming_related_posts":programming_related_posts,
        "most_viewed_blogs":most_viewed_blogs,
        "all_category":all_category,
        "company_logo":company_logo,
        
        
        "action" : "home_page",
    }

    # If HTMX request, return only content
    if request.headers.get("HX-Request"):
        return render(request, "components/home/partial_homepage.html", context)

    # Regular request, return full page
    return render(request, "home.html", context)



def redirect_search_results(request):
    """
    Handles search queries and redirects to the relevant category page.
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return redirect('homepage') 

    try:
        category_match = Category.objects.get(name__iexact=query)
        return redirect('category_post', slug=category_match.slug)
    except Category.DoesNotExist:
        pass
    
    # 2. Search for SubCategory Match (Exact, case-insensitive)
    try:
        subcategory_match = SubCategory.objects.select_related('category').get(name__iexact=query)
        return redirect('category_post', slug=subcategory_match.category.slug)
    except SubCategory.DoesNotExist:
        pass
        

    blog_post_match = BlogPost.objects.select_related('category').filter(
        Q(title__icontains=query) | Q(subtitle__icontains=query), 
        status="published"
    ).first()

    if blog_post_match and blog_post_match.category:
        return redirect('category_post', slug=blog_post_match.category.slug)
            
    return redirect('homepage')



def blog_post_view(request):
    """
    All blogs page view - handles both regular and HTMX requests
    """
    blogs = BlogPost.objects.filter(status="published").select_related(
        "category", "author"
    )
    categories = Category.objects.all()
    

    # Sidebar content
    sidebar_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")[:10]
    )
    popular_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-views", "-likes")[:5]
    )
    

    

    context = {
        "blogs": blogs,
        "category": categories,
        "sidebar_blogs": sidebar_blogs,
        "popular_blogs": popular_blogs,
        "latest_popular_blogs":latest_popular_blogs,
        'action':'all_blogs',
    }


    # If HTMX request, return only content
    if request.headers.get("HX-Request"):
        return render(request, "components/blogs/partial_all_blog_page.html", context)
    # Regular request, return full page
    return render(request, "components/blogs/all_blog_page.html", context)


def popular_blog_post(request):

    blogs = BlogPost.objects.filter(status="published").select_related(
        "category", "author"
    )
    categories = Category.objects.all()
    


    popular_blogs = (
    BlogPost.objects.filter(
        status="published",
        views__gte=1000,
        likes__gte=100
    )
    .select_related("category", "author")
    .order_by("-views", "-likes")[:8]
    )
    
    popular_categories = Category.objects.filter(blogpost__in=popular_blogs).distinct()

    context = {
        "blogs": blogs,
        "popular_categories": popular_categories,
        "popular_blogs": popular_blogs,
        'action':'popular_blogs',
    }


    # If HTMX request, return only content
    if request.headers.get("HX-Request"):
        return render(request, "components/popular/popular_post_partial.html", context)
    # Regular request, return full page
    return render(request, "components/popular/popular_post.html", context)

def all_article(request):
    blogs = BlogPost.objects.filter(status="published").select_related(
        "category", "author"
    )
    categories = Category.objects.all()
    

    # Sidebar content
    sidebar_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")[:10]
    )
    popular_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-views", "-likes")[:5]
    )

    context = {
        "blogs": blogs,
        "category": categories,
        "sidebar_blogs": sidebar_blogs,
        "popular_blogs": popular_blogs,
        'action':'all_article',
    }


    # If HTMX request, return only content
    if request.headers.get("HX-Request"):
        return render(request, "components/category/all_article_partial.html", context)
    # Regular request, return full page
    return render(request, "components/category/all_article.html", context)



def right_blog_details_partial(request, slug):

    blog = get_object_or_404(BlogPost, slug=slug)
    

    content = blog.description.split()
    first_50_words = ' '.join(content[:50])
    remaining_words = ' '.join(content[50:])

    current_user = request.user if request.user.is_authenticated else None
    
    context = {
        'blog': blog,
        'first_50_words': first_50_words,
        'remaining_words': remaining_words,
        'user': current_user,
        'action' : 'right_side_update_in_blog_details'
      
    }
    
    if request.headers.get("HX-Request"):
        return render(request, "components/blog_details/blog_right_side_partial.html", context)
    return render(request, "components/blog_details/blog_right_side.html", context)


def update_blog_stat(request, slug, stat_type):
    blog = get_object_or_404(BlogPost, slug=slug)

    if stat_type == "like":
        blog.likes += 1
    elif stat_type == "view":
        blog.views += 1
    elif stat_type == "share":
        blog.shares += 1

    blog.save()

    # return only the new number
    return HttpResponse(
        blog.likes
        if stat_type == "like"
        else blog.views if stat_type == "view" else blog.shares
    )


def create_blog(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
        "categories": categories,
        "subcategories":subcategories,
        "action" : 'post_create'
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        
        featured_image_file = request.FILES.get('featured_image')
        featured_image_url = request.POST.get('featured_image_url')
        
        additional_image_files = request.FILES.getlist('additional_image')
        additional_image_url_list = request.POST.get('additional_image_url_list')

        tags_list_input = request.POST.get('tags_list')

        # Basic validation
        if not (title and description and category_id):
            messages.error(request, "Please fill in all required fields.")
            if request.headers.get("HX-Request"):
                return render(request, "components/blogs/partial_create_blog_content.html", context)
            return redirect(reverse('create_blog'))

        try:
            category = get_object_or_404(Category, pk=category_id)
            subcategory = None
            
            if subcategory_id: 
                subcategory = get_object_or_404(SubCategory, pk=subcategory_id, category=category)
        except:
            messages.error(request, "Invalid category selected.")
            return redirect(reverse('create_blog'))

        # --- Database Save Operations ---
        try:
            # 1. Create the BlogPost object
            new_blog = BlogPost.objects.create(
                author=request.user,
                category=category,
                subcategory=subcategory,
                title=title,
                description=description,
                
                # Directly map form data to BlogPost fields
                featured_image=featured_image_file if featured_image_file else None,
                featured_image_url=featured_image_url if featured_image_url and not featured_image_file else None
            )

            # --- 2. Handle Tags (New Logic) ---
            if tags_list_input:
                # Split the comma-separated string, strip whitespace, and filter out empty strings
                tag_names = [tag.strip().lower() for tag in tags_list_input.split(',') if tag.strip()]
                
                # Prepare a list to store Tag objects
                tag_objects = []
                
                for name in tag_names:
                    # Use get_or_create to find an existing tag or create a new one
                    # This is efficient and respects the 'unique=True' constraint on the Tag name.
                    tag, created = Tag.objects.get_or_create(name=name)
                    tag_objects.append(tag)
                
                # Add all collected Tag objects to the blog post's many-to-many field
                new_blog.tags.set(tag_objects)

            # 2. Handle Additional Image Files (using BlogAdditionalImage model)
            for file in additional_image_files:
                BlogAdditionalImage.objects.create(
                    blog=new_blog, 
                    additional_image=file # Matches model field name
                )
            
            # 3. Handle Additional Image URLs (using BlogAdditionalImage model)
            if additional_image_url_list:
                urls = [url.strip() for url in additional_image_url_list.split(',') if url.strip()]
                for url in urls:
                    BlogAdditionalImage.objects.create(
                        blog=new_blog, 
                        additional_image_url=url # Matches model field name
                    )

      
            if request.headers.get("HX-Request"):
                 return render(request, "components/blogs/partial_create_blog_success.html", {'blog': new_blog})

            return redirect(reverse('home')) 

        except Exception as e:
            messages.error(request, "An internal error occurred while creating the post/images.")
            return redirect(reverse('create_blog'))



    # Handle GET request (Form Display)
    if request.headers.get("HX-Request"):
        return render(request, "components/blogs/partial_create_blog_content.html", context)

    return render(request, "base.html", context)




# Blog filter by category
def category_post(request, slug):
    
    category = get_object_or_404(
        Category.objects.prefetch_related('subcategories'),
        slug=slug
    )

    blogs = (
        BlogPost.objects.filter(category=category, status="published")
        .select_related("category")
        .prefetch_related("shares")
    )
    
    subcategory_blogs_map = {}
    
    for subcategory in category.subcategories.all():
        sub_blogs = (
            BlogPost.objects.filter(subcategory=subcategory, status="published")
            .select_related("category", "subcategory")
            .prefetch_related("shares")
        )
        if sub_blogs.exists():
            subcategory_blogs_map[subcategory] = sub_blogs

    # Get sidebar content for HTMX requests
    sidebar_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-created_at")[:10]
    )
    popular_blogs = (
        BlogPost.objects.filter(status="published")
        .select_related("category", "author")
        .order_by("-views", "-likes")[:5]
    )

    context = {
        "category": category,
        "blogs": blogs,
        "sidebar_blogs": sidebar_blogs,
        "popular_blogs": popular_blogs,
        "subcategory_blogs_map": subcategory_blogs_map,
        "action" : 'category_post',
    }


    if request.headers.get("HX-Request"):
        return render(request, "components/category/category_post_partial.html", context)

    return render(request, "components/category/category_post.html", context)



def popular_category_post(request, slug):
    popular_category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()

    # Filter popular blogs globally
    all_popular_blogs = BlogPost.objects.filter(
        status="published",
        views__gte=1000,
        likes__gte=100
    ).select_related("category", "author").order_by("-views", "-likes")

    popular_blogs = all_popular_blogs[:8]

    # oi popular blogs jeishob category te ace
    popular_categories = Category.objects.filter(blogpost__in=popular_blogs).distinct()

    # oi category gulor popular blog 
    category_popular_blogs = all_popular_blogs.filter(category=popular_category)[:8]

    context = {
        "categories": categories,
        "popular_category": popular_category,
        "category_popular_blogs": category_popular_blogs,
        "popular_categories": popular_categories,
        "popular_blogs": popular_blogs,
        "action": "popular_category_post",
    }

    if request.headers.get("HX-Request"):
        return render(request, "components/popular/popular_category_post_partial.html", context)

    return render(request, "components/popular/popular_category_post.html", context)

def contact_page(request):
    context = {
        'action':'contact_page'
    }
    if request.headers.get("HX-Request"):
        return render(request, "partial_contact_us_page.html", context)
    return render(request, 'contact_us_page.html',context)





# comment section
@login_required
# requires POST method use kora valo, karon aita save
@require_POST 
def add_comment(request, post_slug):

    post = get_object_or_404(BlogPost, slug=post_slug)
    

    content = request.POST.get('content', '').strip()

    if not content:
        # messages.error(request, "Comment content cannot be empty.")
        return redirect('post_detail', slug=post_slug)


    Comment.objects.create(
        post=post,
        user=request.user, 
        content=content
    )
    
    # messages.success(request, "Your comment has been posted successfully.")
    
    
    return redirect('blog_details', slug=post_slug)



@login_required
@require_POST
def add_reply(request, comment_id):

    parent_comment = get_object_or_404(Comment, id=comment_id)
    post_slug = parent_comment.post.slug 
    
    
    content = request.POST.get('content', '').strip()

    if not content:
     
        return redirect('post_detail', slug=post_slug)


    Reply.objects.create(
        comment=parent_comment,
        user=request.user, 
        content=content
    )

    return redirect('blog_details', slug=post_slug)



@login_required
def user_like_toggle(request, like_slug):
   
    blog_post = get_object_or_404(BlogPost, slug=like_slug)
    user = request.user
    
    if request.headers.get("HX-Request"):
    
        try:
            like_instance = Like.objects.get(post=blog_post, user=user)
            like_instance.delete()
            
        except Like.DoesNotExist:
            try:
                Like.objects.create(post=blog_post, user=user)
               
            except IntegrityError:
            
                # messages.error(request, "An error occurred while liking the post.")
                logout(request)
                return redirect('login')
                # return redirect('blog_details', slug=like_slug)
    
    return redirect('blog_details', slug=like_slug)




# @login_required
# def save_post(request, save_slug):
#     post = get_object_or_404(BlogPost, slug=save_slug)

#     if request.method == "POST":
#         already_saved = SavedPost.objects.filter(post=post, user=request.user).exists()

#         if not already_saved:
#             SavedPost.objects.create(post=post, user=request.user)
#         else:
#             # Optional: Unsave if already saved
#             SavedPost.objects.filter(post=post, user=request.user).delete()

#         return redirect("blog_details", post_slug=save_slug)

#     return redirect("blog_details", post_slug=save_slug)






@require_POST
def record_share(request, post_slug):
    """
    Records a share event. Uses get_or_create for logged-in users 
    to prevent counting the same share multiple times.
    """
    platform = request.POST.get('platform')

    if not platform:
        return JsonResponse({"status": "error", "message": "Platform not provided"}, status=400)

    try:
        post = get_object_or_404(BlogPost, slug=post_slug)
        
        if request.user.is_authenticated:
            # Share already exists if created is False
            share_instance, created = Share.objects.get_or_create(
                post=post,
                user=request.user,
                platform=platform,
                defaults={'platform': platform} # Ensure platform is set if creating
            )

            if created:
                return JsonResponse({"status": "success", "message": f"New share recorded on {platform}."})
            else:
                return JsonResponse({"status": "info", "message": f"Share already counted for this user on {platform}."})

        else:
            # Anonymous users will be counted every time, as we can't reliably track them
            # without complex session/cookie management. 
            Share.objects.create(
                post=post,
                user=None, # user=None for anonymous
                platform=platform
            )
            return JsonResponse({"status": "success", "message": f"Share recorded (Anonymous) on {platform}."})

    except Exception as e:
        # It's better to log the exception, but for user feedback:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)