from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('add_item/', views.AddItemView.as_view(), name='add_item'),
    path('create_item/', views.CreateItemView.as_view(), name='create_item'),
    path('edit_addition/<int:pk>/', views.EditAdditionView.as_view(),
         name='edit_addition'),
    path('delete_addition/<int:pk>/', views.DeleteAdditionView.as_view(), 
         name='delete_addition'),
    path('archive_addition/<int:pk>/', views.ArchiveAdditionView.as_view(), 
         name='archive_addition'),
    path('archived_additions/', views.ArchivedAdditionsView.as_view(), 
         name='archived_additions'),
    path('unarchive_addition/<int:pk>/', views.UnarchiveAdditionView.as_view(),
         name='unarchive_addition'),
]
