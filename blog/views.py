from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.db.models import Count

from blog.models import Post
from blog.forms import CommentForm




def posts_list_view(request):
    posts = Post.objects.filter(is_public=True)[:10]
    context = {
        'posts': posts,
        'current_site': get_current_site(request),
    }
    template_name = 'public/blog/posts.html'
    return render(request, template_name, context)







def post_detail_view(request, slug):
    posts = Post.objects.filter(is_public=True)
    post = get_object_or_404(posts, slug=slug)
    
    recent_posts = Post.objects.filter(is_public=True).exclude(id=post.id).order_by('-date')[:3]
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids, is_public=True).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-id')[:9]


    comment_form = CommentForm
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        
        if comment_form.is_valid():
            comment_form.instance.post = post
            comment_form.save()
            
            return redirect('post-detail', post.slug)
        
        else:
            messages.error(request, "Veuillez remplir correctement le formulaire svp !")
    
    else:
        comment_form = CommentForm
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'current_site': get_current_site(request),
    }
    template_name = 'public/blog/post_detail.html'
    return render(request, template_name, context)





