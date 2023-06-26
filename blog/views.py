from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


# Create your views here.
class PostLV(ListView):
	model = Post
	template_name = 'blog/post_all.html'
	context_object_name = 'posts'
	paginate_by = 2  # 두개씩 보여줌(전체 글중에)


class PostDV(DetailView):
	model = Post
