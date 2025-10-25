from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import BlogPost, Category, Review
from .models import BlogPost, BlogAdditionalImage, Category, Tag
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import CustomUserModel

# Create your views here.


def home(request):
    """
    Home page view - handles both regular and HTMX requests
    """
    blogs = BlogPost.objects.filter(status="published")[:6]
    latest_blog = (
        BlogPost.objects.filter(status="published").order_by("-created_at").first()
    )

    # Get top 5 published blogs for carousel
    carousel_blogs = BlogPost.objects.filter(status="published").order_by(
        "-created_at"
    )[:5]

    top_users = CustomUserModel.objects.filter(is_verified=True).order_by(
        "-created_at"
    )[:4]

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
        .order_by('-published_post_count')[:6]
    )

    # 2. Prepare a single, flat list of the top blog posts.
    popular_posts_flat_list = []

    for category in popular_categories:
        # Retrieve the top 6 published blog posts within the current category, ordered by 'views'
        top_posts = (
            BlogPost.objects
            .filter(category=category, status='published')
            .order_by('-views')[:6]
        )
        
        # Add individual post entries directly to the flat list
        for post in top_posts:
            popular_posts_flat_list.append({
                'title': post.title,
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
        
        
        "action" : "home_page",
    }

    # If HTMX request, return only content
    if request.headers.get("HX-Request"):
        return render(request, "components/home/partial_homepage.html", context)

    # Regular request, return full page
    return render(request, "home.html", context)


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


def blog_details_view(request, slug):

    try:
        blog = (
            BlogPost.objects.select_related("category", "author")
            .prefetch_related("reviews", "additional_images", "tags")
            .get(slug=slug, status="published")
        )
    except BlogPost.DoesNotExist:
        return render(request, "components/home/404.html")

    # Get related blogs from the same category
    category_blogs = (
        BlogPost.objects.filter(category=blog.category, status="published")
        .exclude(slug=slug)
        .select_related("category", "author")[:5]
    )

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

    # All blogs for sidebar or other sections
    all_blogs = BlogPost.objects.filter(status="published").select_related(
        "category", "author"
    )[:10]

    # Split description for "Read More" functionality
    words = blog.description.split()
    first_50_words = " ".join(words[:50])
    remaining_words = " ".join(words[50:]) if len(words) > 50 else ""

    # # Update view count
    # blog.views += 1
    # blog.save(update_fields=["views"])

    context = {
        "blog": blog,
        "all_blogs": all_blogs,
        "sidebar_blogs": sidebar_blogs,
        "popular_blogs": popular_blogs,
        "category_blogs": category_blogs,
        "first_50_words": first_50_words,
        "remaining_words": remaining_words,
        # "is_htmx_request": False,  # Flag for regular page load
        "action" : "blog_details",
    }
    if request.headers.get("HX-Request"):
        return render(request, "components/blog_details/partial_blog_details_page.html", context)
    return render(request, "components/blog_details/blog_details_page.html", context)


    # return render(request, "components/blog_details/blog_details_page.html", context)


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
    context = {
        "categories": categories,
        "action" : 'post_create'
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        
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
        except:
            messages.error(request, "Invalid category selected.")
            return redirect(reverse('create_blog'))

        # --- Database Save Operations ---
        try:
            # 1. Create the BlogPost object
            new_blog = BlogPost.objects.create(
                author=request.user,
                category=category,
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
    category = get_object_or_404(Category, slug=slug)

    blogs = (
        BlogPost.objects.filter(category=category, status="published")
        .select_related("category")
        .prefetch_related("shares")
    )

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

