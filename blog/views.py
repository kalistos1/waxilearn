from django.shortcuts import render,HttpResponse
from .models import Post, BlogCategory, BlogComments

# Create your views here.

def PostList(request):
    allPosts = Post.published.all().order_by('date_created')
    context={
        'allPosts':allPosts,
    }
    return render(request,'blog/bloglist.html', context)


def PostDetail(request,slug):
    post = Post.objects.get(slug=slug)
    context ={
        'post':post
    }
    return render (request, 'blog/blogdetail.html', context)
