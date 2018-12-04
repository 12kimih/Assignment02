from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm

# Create your views here.
class PostListView(ListView):
    model = Post
    paginate_by = 15

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.hit += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if object.password != request.POST.get('password', ''):
            messages.error(request, 'Wrong Password. Deletion Failed.')
            return HttpResponseRedirect(
                    reverse('post_detail', args=[object.pk]))

        messages.info(request, f'Successfully Deleted - {object.title}')
        return super().post(self, request, *args, **kwargs)
