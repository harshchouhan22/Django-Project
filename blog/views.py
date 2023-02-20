from django.shortcuts import get_object_or_404
from .models import Contact
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('all_appointments_for_dr')
        if request.user.is_CareCenter:
            return redirect('CareCenter')
        if request.user.CareCenter_Head:
            return redirect('CareCenter_Head')
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


from django.core.mail import EmailMessage
from django.template.loader import get_template

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")

            # Email the profile with the
            template = get_template('blog/email_template.html')

        context = {
            'phone':phone,
            'name': name,
            'email': email,
            'content': content,
        }
        content = template.render(context)

        email = EmailMessage(
            "Thanks For Contacting Us",
            content,
            "EVE Health Care Centers" + '',
            [email],
            headers={'Reply-To': email}
        )
        email.send()
    return render(request, 'blog/contact.html')



def post(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/post.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
