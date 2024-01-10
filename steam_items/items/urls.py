from django.urls import path

from .views import (
    AddItemView, ArchiveAdditionView, ArchivedAdditionsView, CreateItemView,
    DeleteAdditionView, EditAdditionView, IndexView, ItemDetailView,
    PriceHistoryJsonView, PriceHistoryView, UnarchiveAdditionView,
    UpdatePriceView, save_current_price
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item_detail/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('create_deal/', AddItemView.as_view(), name='create_deal'),
    path('create_deal/<int:item_id>/', AddItemView.as_view(), name='create_deal'),
    path('update_price/<int:item_id>/', UpdatePriceView.as_view(), name='update_price'),
    path('create_item/', CreateItemView.as_view(), name='create_item'),
    path('edit_deal/<int:pk>/', EditAdditionView.as_view(),
         name='edit_deal'),
    path('delete_deal/<int:pk>/', DeleteAdditionView.as_view(),
         name='delete_deal'),
    path('archive_addition/<int:pk>/', ArchiveAdditionView.as_view(),
         name='archive_addition'),
    path('archived_additions/', ArchivedAdditionsView.as_view(),
         name='archived_additions'),
    path('unarchive_addition/<int:pk>/', UnarchiveAdditionView.as_view(),
         name='unarchive_addition'),
    path('save_current_price/', save_current_price,
         name='save_current_price'),
    path('price_history/<int:item_id>/', PriceHistoryView.as_view(),
         name='price_history'),
    path('price_history_json/<int:item_id>/', PriceHistoryJsonView.as_view(),
         name='price_history_json'),
]
