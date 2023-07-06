from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mysite.views import OwnerOnlyMixin
from photo.forms import PhotoInlineFormSet
from photo.models import Photo, Album


# Create your views here.
class AlbumLV(ListView):
	model = Album


class AlbumDV(DetailView):
	model = Album


class PhotoDV(DetailView):
	model = Photo


# photo view
class PhotoCV(LoginRequiredMixin, CreateView):
	model = Photo
	fields = ('album', 'title', 'image', 'description')
	success_url = reverse_lazy('photo:index')


class PhotoChangeLV(LoginRequiredMixin, ListView):
	model = Photo
	template_name = 'photo/photo_change_list.html'

	def	get_queryset(self):
		return Photo.objects.filter(owner=self.request.user)


class PhotoUV(OwnerOnlyMixin, UpdateView):
	model = Photo
	success_url = reverse_lazy('photo:index')


class PhotoDelV(OwnerOnlyMixin, DeleteView):
	model = Photo
	success_url = reverse_lazy('photo:index')


# album view
class AlbumPhotoCV(LoginRequiredMixin, CreateView):
	model = Album
	fields = ('name', 'description')
	success_url = reverse_lazy('photo:index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES)
		else:
			context['formset'] = PhotoInlineFormSet()
		return context

	def form_valid(self, form):
		form.instance.owner = self.request.user
		context = self.get_context_data()
		formset = context['formset']
		for photoform in formset:
			photoform.instance.owner = self.request.user
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))


class AlbumChangeLV(LoginRequiredMixin, ListView):
	model = Album
	template_name = 'photo/album_change_list.html'

	def	get_queryset(self):
		return Album.objects.filter(owner=self.request.user)


class AlbumPhotoUV(OwnerOnlyMixin, UpdateView):
	model = Album
	fields = ('name', 'description')
	success_url = reverse_lazy('photo:index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			context['formset'] = PhotoInlineFormSet(instance=self.object)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return redirect(self.success_url())
		else:
			self.render_to_response(self.get_context_data(form=form))


class AlbumPhotoDelV(OwnerOnlyMixin, DeleteView):
	model = Album
	success_url = reverse_lazy('photo:index')



