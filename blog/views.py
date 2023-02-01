from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .forms import PostCreateForm
from .models import Post, Likes
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    
    def get(self, request):
        postList = Post.objects.all()
        likes = list()
        if request.user.is_authenticated:
            rows = request.user.liked_posts.values("id")
            likes = [row["id"] for row in rows]
        ctx = {"postList":postList, "likes":likes}
        return render(request, self.template_name, ctx)


class CreatePost(LoginRequiredMixin,View):
    template_name = "blog/postForm.html"
    success_url = reverse_lazy("blog:home")

    def get(self, request):
        form = PostCreateForm()
        ctx = {"form":form}
        return render(request, self.template_name,ctx)

    def post(self, request):
        form = PostCreateForm(request.POST)
        if not form.is_valid():
            ctx = {"form":form}
            return render(request, self.template_name, ctx)
        
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        form.save_m2m()
        messages.success(request, f"Submitted successfully {post}")
        return redirect(self.success_url)


class EditPost(LoginRequiredMixin, View):
    template_name = "blog/postForm.html"
    success_url = reverse_lazy("blog:home")

    def get(self, request, id):
        post = get_object_or_404(Post, id = id, user = self.request.user)
        form = PostCreateForm(instance = post)
        ctx = {"form":form}
        return render(request, self.template_name, ctx)

    def post(self, request, id):
        post = get_object_or_404(Post, id = id, user = self.request.user)
        form = PostCreateForm(request.POST, instance = post)

        if not form.is_valid():
            ctx = {"form":form}
            return render(request, self.template_name, ctx)

        post = form.save(commit=False)
        post.save()
        form.save_m2m()
        messages.success(request, f"Edited successfully {post}")
        return redirect(self.success_url)


class ListPosts(LoginRequiredMixin, View):
    template_name = "blog/listPosts.html"

    def get(self, request):
        posts = Post.objects.filter(user = self.request.user)
        return render(request, self.template_name, {'postList':posts})


class PostDetail(DetailView):
    model = Post
    template_name = "blog/blogDetail.html"

    def get(self, request, id):
        post = Post.objects.get(id = id)
        ctx = {"post":post}
        return render(request, self.template_name, ctx)


@requires_csrf_token
def uploadImage(request):
    f = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(f).split('.')[0]
    file = fs.save(filename, f)
    fileurl = fs.url(file)
    return JsonResponse({'success':1,'file':{'url':fileurl}})


def uploadLinkView(request):
    import requests
    from bs4 import BeautifulSoup  

    print(request.GET['url'])
    url = request.GET['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text,features="html.parser")
    metas = soup.find_all('meta')
    description=""
    title=""
    image=""
    for meta in metas:
        if 'property' in meta.attrs:
            if (meta.attrs['property']=='og:image'):
                image=meta.attrs['content']         
        elif 'name' in meta.attrs:         
            if (meta.attrs['name']=='description'):
                description=meta.attrs['content']
            if (meta.attrs['name']=='title'):
                title=meta.attrs['content']
    return JsonResponse({'success':1,'meta':
    {"description":description,"title":title, "image":{"url":image}
        }})

@method_decorator(csrf_exempt, name = "dispatch")
class AddLike(LoginRequiredMixin, View):
    def post(self, request, id):
        print('hello')
        p = get_object_or_404(Post, id = id)
        like = Likes(user = request.user, post = p)
        try:
            like.save()
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class RemoveLike(LoginRequiredMixin, View):
    def post(self, request, id):
        print('hello')
        p = get_object_or_404(Post, id=id)
        try:
            like = Likes.objects.get(user = request.user, post = p).delete()
        except Likes.DoesNotExist:
            pass

        return HttpResponse()
