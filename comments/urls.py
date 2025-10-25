from django.urls import path
from . import views

app_name = 'blog_post'

urlpatterns = [
    # Main Blog detail view (Apnar 'get_comments' view-ti ami 'blog_detail_view'-e rename korechi)
    path('<slug:slug>/', views.blog_detail_view, name='detail'),

    # HTMX Endpoint for posting a new comment
    path('<slug:slug>/comment/', views.post_comment, name='post_comment'),

    # HTMX Endpoint for posting a reply to a comment
    path('comment/<int:comment_id>/reply/', views.post_reply, name='post_reply'),
]
