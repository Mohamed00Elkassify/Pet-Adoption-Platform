from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, TemplateView, FormView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pet, AdoptionRequest
from .forms import PetForm, AdoptionRequestForm, SignupForm

# Create your views here.
class SignupView(FormView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PetListView(ListView):
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = "pets"

    def get_queryset(self):
        qs = Pet.objects.all()
        species = self.request.GET.get('species')
        city = self.request.GET.get('city')
        status = self.request.GET.get('status')
        if species:
            qs = qs.filter(species=species)
        if city:
            qs = qs.filter(city=city)
        if status:
            qs = qs.filter(status=status)
        return qs

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pets/pet_detail.html'

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pet_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class PetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pet_list')

    def test_func(self):
        return Pet.objects.filter(
          id=self.kwargs['pk'], owner=self.request.user
        ).exists()

class PetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet_confirm_delete.html'
    success_url = reverse_lazy('pet_list')

    def test_func(self):
        return Pet.objects.filter(
          id=self.kwargs['pk'], owner=self.request.user
        ).exists()
    
class AdoptionRequestCreateView(CreateView):
    model = AdoptionRequest
    form_class = AdoptionRequestForm
    template_name = 'pets/adoption_form.html'

    def form_valid(self, form):
        pet = Pet.objects.get(pk=self.kwargs['pk'])
        form.instance.pet = pet
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pet_detail', kwargs={'pk': self.kwargs['pk']})

class AdoptionRequestListView(LoginRequiredMixin, ListView):
    model = AdoptionRequest
    template_name = 'pets/adoption_requests.html'
    context_object_name = "requests"

    def get_queryset(self):
        return AdoptionRequest.objects.filter(pet__owner=self.request.user)
