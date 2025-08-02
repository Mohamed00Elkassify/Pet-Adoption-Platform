from django.urls import path
from .views import(SignupView, PetListView, PetDetailView, PetCreateView, PetUpdateView, PetDeleteView)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', PetListView.as_view(), name='pet_list'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('pets/add/', PetCreateView.as_view(), name='pet_add'),
    path('pets/edit/<int:pk>/', PetUpdateView.as_view(), name='pet_edit'),
    path('pets/delete/<int:pk>/', PetDeleteView.as_view(), name='pet_delete'),
]