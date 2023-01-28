from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from creator.models import UserProfile, UserInstance
from .models import Category, Post, PostInstance, Comment, Reply
from .forms import PostForm
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword =  self.request.GET.get('search')
        context['keyword'] = keyword if keyword else ''

        featured = Post.objects.filter(
            publish_date__lte=timezone.now(), featured=True).order_by('publish_date')
        popular = Post.objects.filter()
        
        if featured.count() > 0:
            context['featured1'] = featured[0]
        context['featured'] = featured
        context['popular'] = popular[:4]
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):

        category = self.request.GET.get('category')
        keyword = self.request.GET.get('search')
        queryset = Post.objects.filter() if not keyword else Post.objects.filter(title__icontains=keyword)

        return queryset.filter(publish_date__lte=timezone.now()).order_by('-publish_date').exclude(featured=True)




class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post).order_by('-created_at')

        if self.request.user.is_authenticated:
            author = post.author
            context['following'] = UserInstance.objects.filter(
                user__user=self.request.user, following=author)

            context['starred'] = PostInstance.objects.filter(
                starrer=self.request.user, post=post)

            if self.request.user == author:
                context['author'] = author
        context['comments'] = comments

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = 'signin'
    redirect_field_name = 'stories'

    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = UserProfile.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'signin'
    redirect_field_name = 'post-detail'

    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'signin'
    model = Post
    success_url = reverse_lazy('stories')


############################################################

##############################################################

@login_required(redirect_field_name='next', login_url='signin')
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('stories')


def add_comment_to_post(request, pk):
    """_summary_

    Args:
        request (request): session
        pk (int): post's primary key

    Returns:
        template: returns a template with context data
    """
    # get the specific post for which to create comment or a 404 code
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            name = request.POST.get('name')
            check = request.POST.get('check')
            if check:
                Comment.objects.create(
                    post=post, text=content, author=request.user.userprofile)

            else:
                Comment.objects.create(
                    post=post, text=content, author_name=name)

    return redirect(post.get_absolute_url())


@login_required(redirect_field_name='next', login_url='signin')
def star_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        post_instance = PostInstance(post=post, starrer=request.user)
        post_instance.star(request)
        post_instance.save()
    except:
        return redirect('post-detail', pk)

    return redirect('post-detail', pk)


@login_required(redirect_field_name='next', login_url='signin')
def unstar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_instance = PostInstance.objects.filter(post=post)[0]
    post_instance.delete()
    return redirect('post-detail', pk)


@login_required(redirect_field_name='next', login_url='signin')
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post-detail', pk=post_pk)


@login_required(redirect_field_name='next', login_url='signin')
def stories(request):
    posts = Post.objects.filter(author=request.user)
    pub_posts = posts.filter(
        publish_date__lte=timezone.now()).order_by('publish_date')
    drafts = posts.filter(
        publish_date__isnull=True).order_by('create_date')
    context = {
        'published': pub_posts,
        'drafts': drafts,
        'posts': posts,
    }
    return render(request, 'stories.html', context=context)


@login_required(redirect_field_name='next', login_url='signin')
def add_reply(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        author = request.user.userprofile
        text = request.POST.get('text')

        Reply.objects.create(comment=comment, author=author, text=text)
        return redirect(Post.objects.get(comments=comment))
