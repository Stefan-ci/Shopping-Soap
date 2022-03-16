from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


from blog.models import Post, Comment
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
    comment_form = CommentForm
    post = get_object_or_404(Post, slug=slug)
    post_comments = Comment.objects.filter(post=post)
    post_comments_count = Comment.objects.filter(post=post).count()
    
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
        'comments': post_comments,
        'comment_form': comment_form,
        'current_site': get_current_site(request),
        'post_comments_count': post_comments_count,
    }
    template_name = 'public/blog/post_detail.html'
    return render(request, template_name, context)





