from django import forms
from django.utils import timezone

from .models import Item, ItemAddition


class ItemAdditionForm(forms.ModelForm):
    """Форма для добавления предметов."""
    date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        required=False,
        label='Дата и время',
    )
    seconds = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = ItemAddition
        fields = ['item', 'transaction_type', 'quantity', 'price_per_item',
                  'commission', 'date', 'seconds']

    def __init__(self, *args, **kwargs):
        """Инициализация формы. Устанавливает начальные значения."""
        item_id = kwargs.pop('item_id', None)
        super(ItemAdditionForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1
        if not self.instance.pk:
            self.initial['date'] = timezone.now().strftime('%d.%m.%Y %H:%M')
            self.initial['seconds'] = timezone.now().second
        else:
            self.initial['seconds'] = self.instance.date.second
        if item_id:
            self.initial['item'] = item_id

    def clean(self):
        """Очистка и проверка данных формы."""
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        item = cleaned_data.get('item')
        if transaction_type == 'SELL' and item.quantity < quantity:
            raise forms.ValidationError(
                'Недостаточное количество предметов для продажи.')
        return cleaned_data

    def clean_date(self):
        """Очистка и проверка поля 'date'."""
        date = self.cleaned_data.get('date')
        if date is None:
            return timezone.now()
        return date

    def clean_quantity(self):
        """Очистка и проверка поля 'quantity'."""
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество должно быть больше 0.')
        return quantity

    def clean_price_per_item(self):
        """Очистка и проверка поля 'price_per_item'."""
        price_per_item = self.cleaned_data.get('price_per_item')
        if price_per_item <= 0:
            raise forms.ValidationError('Цена должна быть больше 0.')
        return price_per_item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'link', 'image']
