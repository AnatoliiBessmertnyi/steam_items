from django.shortcuts import redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, RedirectView,) 
from django.urls import reverse
from django.db.models import Count
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from .models import Item, ItemAddition
from .forms import ItemForm, ItemAdditionForm


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(quantity__gt=0)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additions'] = ItemAddition.objects.filter(
            item=self.object, archived=False)
        return context


class AddItemView(CreateView):
    model = ItemAddition
    form_class = ItemAdditionForm
    template_name = 'add_item.html'

    def form_valid(self, form):
        form.save()
        return redirect('index')


class EditAdditionView(UpdateView):
    model = ItemAddition
    form_class = ItemAdditionForm
    template_name = 'edit_addition.html'

    def get_success_url(self):
        return reverse('item_detail', kwargs={'pk': self.object.item.id})


class CreateItemView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'create_item.html'

    def form_valid(self, form):
        form.save()
        return redirect('index')
    

class DeleteAdditionView(DeleteView):
    model = ItemAddition
    success_url = reverse_lazy('archived_additions')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


class ArchiveAdditionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        addition.archived = True
        addition.save()
        return reverse('item_detail', kwargs={'pk': addition.item.pk})
    

class ArchivedAdditionsView(ListView):
    template_name = 'archived_additions.html'
    context_object_name = 'additions'

    def get_queryset(self):
        return ItemAddition.objects.filter(archived=True).order_by('item__name')


class UnarchiveAdditionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        addition.archived = False
        addition.save()
        return reverse('archived_additions')
