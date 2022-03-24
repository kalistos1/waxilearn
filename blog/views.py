from django.shortcuts import render,redirect,HttpResponse
from .models import Post, BlogCategory, BlogComments
from.forms import PostForm
from django.contrib import messages

# Create your views here.

def PostList(request):
    allPosts = Post.published.all().order_by('date_created')
    allcategory = BlogCategory.objects.all()
    context={
        'allcategory':allcategory,
        'allPosts':allPosts,
    }
    return render(request,'blog/blog_all.html', context)


def PostDetail(request):
    # post = Post.objects.get(slug=slug)
    # context ={
    #     'post':post
    # }
    return render (request, 'blog/single_post.html')


def category_post_list(request,slug):
    get_cat = BlogCategory.objects.get(slug=slug)
    cat_id =get_cat.id
    get_cat_posts = Post.objects.filter(category = cat_id)
    context = {
        'get_cat_posts':get_cat_posts,
    }
    return render(request,'blog/blog_all.html',context)


def create_post(request):
    if request.method =="POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            messages.success(request,'Blog post saved succesfully')
            return redirect('create_post')
        else:
            post_form =PostForm()
            messages.error(request,'blog post was not saved retry')
            context ={
                'post_form':post_form,
            }
            return render(request,"dashboard/instructor/add_blog_post.html",context)
    else:
        post_form = PostForm()
        messages.error(request, 'blog post was not saved. retry')
        context={
            'post_form':post_form,
        }
        return render(request,'dashboard/instructor/add_blog_post.html',context)


def edit_post(request,slug):
    if request.method =="POST":
        blog_post =Post.objects.get(slug=slug)
        post_form =PostForm(request.POST, instance=blog_post)
        
        if  post_form.is_valid():
            post_form.save()
            messages.success(request,"blog post was saved succesfully")
            return redirect('')
        else:
            messages.error(request,'please correct the error before submiting')
    else:
        blog_post =Post.objects.get(slug=slug)
        post_form =PostForm(instance =blog_post)
        context = {
               'post_form':post_form,
           }
    return render(request, "dashboard/instructor/edit_blog_post.html", context)



def admin_all_blog_post(request):
    all_posts = Post.objects.all().order_by('date_created')
    context={
        'all_posts':all_posts,
    }
    return render(request,'dashboard/instructor/all_blog_posts.html',context)



def delete_post(request,slug):
    blog_post =Post.objects.filter(slug=slug).delete()
    return redirect('admin_all_post')
    