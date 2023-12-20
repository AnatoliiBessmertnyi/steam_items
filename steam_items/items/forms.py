from django import forms
from .models import Item, ItemAddition


class ItemAdditionForm(forms.ModelForm):
    class Meta:
        model = ItemAddition
        fields = ['item', 'transaction_type', 'quantity', 'price_per_item', 'commission']

    def __init__(self, *args, **kwargs):
        super(ItemAdditionForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1
        self.fields['price_per_item'].initial = 1

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        quantity = cleaned_data.get('quantity')
        item = cleaned_data.get('item')
        if transaction_type == 'SELL' and item.quantity < quantity:
            raise forms.ValidationError(
                'Недостаточное количество предметов для продажи.')
        return cleaned_data

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Количество должно быть больше 0.')
        return quantity

    def clean_price_per_item(self):
        price_per_item = self.cleaned_data.get('price_per_item')
        if price_per_item <= 0:
            raise forms.ValidationError('Цена должна быть больше 0.')
        return price_per_item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'link', 'image']

