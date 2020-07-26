from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.views.generic import ( TemplateView, ListView, DetailView
                                , CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.utils import timezone
from blog.forms import PostForm, CommentForm
from blog.models import Post,Comment
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

#POST LIST VIEW
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
#POST DETAIL VIEW
class PostDetailView(DetailView):
    model = Post

#POST CREATE VIEW
class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

#POST UPDATE VIEW 
class PostUpdateView(UpdateView, LoginRequiredMixin):
    model = Post
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class=PostForm

#POST DELETE VIew
class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('post_list')

#POST DRAFT 
class DraftListView(ListView, LoginRequiredMixin):
    model = Post

    def get_queryset(self):
        return Post.objects.filter( published_date__isnull=True).order_by('created_date')

##############################################

#FUNCTIONS 

#############################################

#ADD COMMENT TO POST

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {
        'form':form
    })

#POST PUBLISH 
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk )

#COMMENT APPROVAL 
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

#COMMENT DELETE
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk=post_pk)

#Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
        else:
            return HttpResponse('Disabled account')
    else:
        return render(request, 'registration/login.html')
#LOGOUT
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))