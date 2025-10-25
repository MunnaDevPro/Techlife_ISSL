from blog_post.models import Category

def navbar_all_categorie(request):
    return {'categories': Category.objects.all()}
