from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Item, ItemAddition


class ItemAdditionForm(forms.ModelForm):
    """
    Форма для добавления сделки по предмету.
    """
    date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.DateTimeInput(format='%d.%m.%Y %H:%M'),
        required=False,
        label='Дата и время',
    )

    class Meta:
        """
        Внутренний класс для определения дополнительных параметров модели.
        """
        model = ItemAddition
        fields = ['item', 'transaction_type', 'quantity', 'price_per_item',
                  'commission', 'date']

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы. Устанавливает начальные значения для некоторых 
        полей.
        """
        item_id = kwargs.pop('item_id', None)
        super(ItemAdditionForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1
        if not self.instance.pk:
            self.initial['date'] = timezone.now()
        if item_id:
            self.initial['item'] = item_id

    def clean(self):
        """
        Переопределенный метод clean для проверки данных формы.
        """
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        item = cleaned_data.get('item')
        if transaction_type == 'SELL' and item.quantity < quantity:
            raise forms.ValidationError(
                'Недостаточное количество предметов для продажи.')
        return cleaned_data

    def clean_quantity(self):
        """
        Проверка поля 'quantity'. Должно быть больше 0.
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество должно быть больше 0.')
        return quantity

    def clean_price_per_item(self):
        """
        Проверка поля 'price_per_item'. Должно быть больше 0.
        """
        price_per_item = self.cleaned_data.get('price_per_item')
        if price_per_item <= 0:
            raise forms.ValidationError('Цена должна быть больше 0.')
        return price_per_item
    
    def clean_date(self):
        """
        Проверка поля 'date'. Должно быть заполнено.
        """
        date = self.cleaned_data.get('date')
        if not date:
            raise ValidationError('Дата и время обязательны.')
        return date


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'link', 'image']

