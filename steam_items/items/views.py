from django.shortcuts import redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, RedirectView,) 
from django.urls import reverse
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from .models import Item, ItemAddition
from .forms import ItemForm, ItemAdditionForm


from django.db.models import Avg

class IndexView(ListView):
    """
    Отображает список всех предметов, которые имеют неархивированные
    сделки.
    """
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self):
        """
        Возвращает QuerySet всех предметов, которые имеют неархивированные
        сделки.
        """
        return Item.objects.filter(quantity__gt=0)

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст общее количество, общую стоимость, среднюю цену и
        список предметов с их средними ценами.
        """
        context = super().get_context_data(**kwargs)
        items = self.get_queryset()
        total_quantity = sum(item.quantity for item in items)
        total_price = 0
        items_with_average_price = []
        for item in items:
            additions = ItemAddition.objects.filter(
                item=item, transaction_type='BUY', archived=False)
            item_average_price = additions.aggregate(
                avg_price=Avg('price_per_item'))['avg_price']
            total_price += item_average_price * item.quantity if item_average_price else 0
            item.average_price = item_average_price
            items_with_average_price.append(item)
        average_price = total_price / total_quantity if total_quantity else 0
        context['total_quantity'] = total_quantity
        context['total_price'] = total_price
        context['average_price'] = average_price
        context['items'] = items_with_average_price
        return context


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
        addition = form.save()
        item = addition.item
        if addition.transaction_type == 'BUY':
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        else:
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        item.save()
        return redirect('index')


class EditAdditionView(UpdateView):
    """
    EditAdditionView обрабатывает обновление существующих сделок.
    """
    model = ItemAddition
    form_class = ItemAdditionForm
    template_name = 'edit_addition.html'

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления сделки.
        """
        return reverse('item_detail', kwargs={'pk': self.object.item.id})

    def update_item(self, item, addition, is_reversed=False):
        """
        Обновляет данные предмета на основе сделки.
        Если is_reversed=True, то обновление будет выполнено в обратном
        порядке.
        """
        factor = -1 if is_reversed else 1
        if addition.transaction_type == 'BUY':
            item.quantity += factor * addition.quantity
            item.total_price += factor * addition.quantity * addition.price_per_item
        else:
            item.quantity -= factor * addition.quantity
            item.total_price -= factor * addition.quantity * addition.price_per_item

    def form_valid(self, form):
        """
        Обрабатывает валидацию формы. Если форма валидна, обновляет сделку и
        соответствующий предмет.
        """
        old_addition = ItemAddition.objects.get(id=self.object.id)
        addition = form.save()
        item = addition.item
        self.update_item(item, old_addition, is_reversed=True)
        self.update_item(item, addition)
        item.save()
        return super().form_valid(form)



class CreateItemView(CreateView):
    '''Создание нового предмета.'''
    model = Item
    form_class = ItemForm
    template_name = 'create_item.html'

    def form_valid(self, form):
        item = form.save(commit=False)
        if not item.link:
            item.link = 'https://steamcommunity.com/market/'
        if not item.image:
            item.image = 'static/images/broken_image.png'
        item.save()
        return redirect('index')
    

class DeleteAdditionView(DeleteView):
    model = ItemAddition
    success_url = reverse_lazy('archived_additions')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        addition = self.get_object()
        item = addition.item
        if addition.transaction_type == 'BUY':
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        else:
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        item.save()
        return super().delete(*args, **kwargs)


class ArchiveAdditionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        addition.archived = True
        addition.save()
        item = addition.item
        if addition.transaction_type == 'BUY':
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        else:
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        item.save()
        return reverse('item_detail', kwargs={'pk': addition.item.pk})
    

class ArchivedAdditionsView(ListView):
    template_name = 'archived_additions.html'
    context_object_name = 'additions'

    def get_queryset(self):
        return ItemAddition.objects.filter(
            archived=True).order_by('item__name')


class UnarchiveAdditionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        addition.archived = False
        addition.save()
        item = addition.item
        if addition.transaction_type == 'BUY':
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        else:
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        item.save()
        return reverse('archived_additions')
