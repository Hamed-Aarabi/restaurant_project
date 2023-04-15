from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from blog.models import Blog
from contact_us.forms import ContactUsForm
from contact_us.models import Message


class BlogView(View):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-date', )
        form = ContactUsForm
        return render(request, 'blog/blogs_list.html', {'blogs': blogs, 'form': form})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(name=cd['name'], email=cd['email'], phone=cd['phone'], message=cd['message'])
            return redirect('blog:blogs')
        else:
            form = ContactUsForm()
        return render(request, 'blog/blogs_list.html', {'form': form})


class BlogDetailView(View):

    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        liked = False
        form = ContactUsForm()
        if blog.like.filter(id=request.user.id).exists():
            liked = True
        return render(request, 'blog/blog_detail.html', {'blog': blog, 'liked': liked, 'form': form})

    def post(self, request, pk):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Message.objects.create(name=cd['name'], email=cd['email'], phone=cd['phone'], message=cd['message'])
            return redirect('blog:detail', pk)
        else:
            form = ContactUsForm()
        return render(request, 'blog/blog_detail.html', {'form': form})


def like_blog(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    if blog.like.filter(id=request.user.id).exists():
        blog.like.remove(request.user)
        return JsonResponse({'response': 'disliked'})
    else:
        blog.like.add(request.user)
        return JsonResponse({'response': 'liked'})
