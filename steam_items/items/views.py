import json

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  RedirectView, UpdateView)

from .forms import ItemAdditionForm, ItemForm
from .models import Item, ItemAddition


@csrf_exempt
@require_POST
def save_current_price(request):
    data = json.loads(request.body)
    item = Item.objects.get(id=data['item_id'])
    item.current_price = data['current_price']
    item.save()
    return JsonResponse({'status': 'ok'})


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(quantity__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.get_queryset()
        total_quantity = sum(item.quantity for item in items)
        total_price = 0
        items_with_average_price = []
        for item in items:
            additions = ItemAddition.objects.filter(
                item=item, transaction_type='BUY', archived=False
            )
            item_average_price = additions.aggregate(
                avg_price=Avg('price_per_item')
            )['avg_price']
            total_price += (
                item_average_price * item.quantity if item_average_price else 0
            )
            item.average_price = item_average_price
            commission = additions.aggregate(
                commission=Avg('commission')
            )['commission']
            if item_average_price and commission:
                item.spread = (
                    (
                        item.current_price * (
                            (100 - commission) / 100
                        )
                    ) / item_average_price - 1
                ) * 100
                item.save()

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
    """Представление для добавления новой сделки по предмету."""
    model = ItemAddition
    form_class = ItemAdditionForm
    template_name = 'add_item.html'

    def form_valid(self, form):
        """Переопределенный метод form_valid для обработки валидной формы."""
        addition = form.save()

        item = addition.item
        if addition.transaction_type == 'BUY':
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        else:
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        item.save()

        if item.quantity == 0:
            ItemAddition.objects.filter(item=item).update(archived=True)

        return redirect(reverse('item_detail', args=[item.id]))

    def get_form_kwargs(self):
        """
        Переопределенный метод get_form_kwargs для передачи item_id в форму.
        """
        kwargs = super().get_form_kwargs()
        kwargs['item_id'] = self.kwargs.get('item_id')
        return kwargs


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
        return redirect(reverse('add_item', args=[item.id]))


class ItemUpdateMixin:
    """Миксин для обновления предмета на основе сделки."""
    def update_item(self, addition, item, reverse=False):
        """Обновляет предмет на основе типа сделки."""
        if addition.transaction_type == 'BUY':
            item.quantity -= addition.quantity if reverse else addition.quantity
            item.total_price -= (
                addition.quantity * addition.price_per_item
                if reverse
                else addition.quantity * addition.price_per_item
            )
        else:
            item.quantity += addition.quantity if reverse else addition.quantity
            item.total_price += (
                addition.quantity * addition.price_per_item
                if reverse
                else addition.quantity * addition.price_per_item
            )
        item.save()


class DeleteAdditionView(ItemUpdateMixin, DeleteView):
    """Обрабатывает удаление существующих сделок."""
    model = ItemAddition
    success_url = reverse_lazy('archived_additions')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаляет сделку."""
        return super().delete(*args, **kwargs)


class ArchiveAdditionView(ItemUpdateMixin, RedirectView):
    """Обрабатывает архивирование существующих сделок."""
    def get_redirect_url(self, *args, **kwargs):
        """Архивирует сделку, обновляет предмет и возвращает URL."""
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        addition.archived = True
        addition.save()
        item = addition.item
        self.update_item(addition, item)
        return reverse('item_detail', kwargs={'pk': addition.item.pk})


class ArchivedAdditionsView(ListView):
    template_name = 'archived_additions.html'
    context_object_name = 'additions'

    def get_queryset(self):
        return ItemAddition.objects.filter(
            archived=True).order_by('item__name')


class UnarchiveAdditionView(RedirectView):
    """Представление для восстановления архивированных сделок."""
    def get_redirect_url(self, *args, **kwargs):
        """Восстанавливает сделку, обновляет предмет и возвращает URL."""
        addition = ItemAddition.objects.get(id=kwargs['pk'])
        item = addition.item
        if addition.transaction_type == 'SELL' and item.quantity < 1:
            return reverse('archived_additions')
        addition.archived = False
        addition.save()

        if addition.transaction_type == 'BUY':
            item.quantity += addition.quantity
            item.total_price += addition.quantity * addition.price_per_item
        else:
            item.quantity -= addition.quantity
            item.total_price -= addition.quantity * addition.price_per_item
        item.save()

        if item.quantity == 0:
            ItemAddition.objects.filter(item=item).update(archived=True)
        return reverse('archived_additions')
