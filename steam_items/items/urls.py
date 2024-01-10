from django.urls import path

from . import views
from .views import UpdatePriceView


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('item_detail/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('create_deal/', views.AddItemView.as_view(), name='create_deal'),
    path('create_deal/<int:item_id>/', views.AddItemView.as_view(), name='create_deal'),
    path('update_price/<int:item_id>/', UpdatePriceView.as_view(), name='update_price'),
    path('create_item/', views.CreateItemView.as_view(), name='create_item'),
    path('edit_deal/<int:pk>/', views.EditAdditionView.as_view(),
         name='edit_deal'),
    path('delete_deal/<int:pk>/', views.DeleteAdditionView.as_view(),
         name='delete_deal'),
    path('archive_addition/<int:pk>/', views.ArchiveAdditionView.as_view(),
         name='archive_addition'),
    path('archived_additions/', views.ArchivedAdditionsView.as_view(),
         name='archived_additions'),
    path('unarchive_addition/<int:pk>/', views.UnarchiveAdditionView.as_view(),
         name='unarchive_addition'),
    path('save_current_price/', views.save_current_price,
         name='save_current_price'),
    path('price_history/<int:item_id>/', views.PriceHistoryView.as_view(),
         name='price_history'),
    path('price_history_json/<int:item_id>/', views.PriceHistoryJsonView.as_view(),
         name='price_history_json'),
]
