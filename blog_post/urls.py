from django.urls import path

from .views import (
    home,
    blog_post_view,
    blog_details_view,
    update_blog_stat,
    category_post,
    create_blog,
    contact_page,
    popular_blog_post,
    all_article,
    popular_category_post,
    # blog_partial_view
    # more_blog_details
    right_blog_details_partial,
    
    blog_details_view,
)

from interactions.views import share_post
from save_post.views import save_post,check_saved
from .views import add_comment, add_reply

urlpatterns = [
    path("", home, name="homepage"),
    path("blogs/", blog_post_view, name="blogs"),
    
    # path("blog/details/<slug:slug>/", blog_details_view, name="blog_details"),

    path('blog/detials/update/<slug:slug>/', right_blog_details_partial, name='right_blog_details_partial'),
    
    # path("blog/more-details/<slug:slug>/", more_blog_details, name="more_blog_details"),

    # path("blog/partial/<slug:slug>/", blog_partial_view, name="blog_partial"),  # HTMX partial
    path('category/<slug:slug>/', category_post, name='category_post'),
    path(
        "update/<slug:slug>/<str:stat_type>/",
        update_blog_stat,
        name="update_blog_stat",
    ),

    path("blogs/create_blog/" , create_blog , name="create_blog"),

    path("contact/", contact_page, name="contact_page" ),
    
    path("popular-blogs/", popular_blog_post, name="popular_blogs"),
    
    path("popular/<slug:slug>/", popular_category_post, name="popular_category_post"),
    
    path("all-blog/", all_article, name='all_article'),
    
    
    path("blog_details/<slug:slug>/", blog_details_view, name="blog_details"),
    
    
    
    path('share-post/',share_post, name='share_post'),
    
    path('save-post/', save_post, name='save_post'),
    path('check-saved/<int:post_id>/', check_saved, name='check_saved'),
    
    
    # add commnets
    path('post/<slug:post_slug>/comment/', add_comment, name='add_comment'),

    path('comment/<int:comment_id>/reply/', add_reply, name='add_reply'),

    
]



