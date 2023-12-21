from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    link = models.URLField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def average_price(self):
        additions = self.itemaddition_set.filter(transaction_type='BUY', 
                                                 archived=False)
        total_price = sum(addition.price_per_item * addition.quantity for addition in additions)
        total_quantity = sum(addition.quantity for addition in additions)
        return total_price / total_quantity if total_quantity else 0


class ItemAddition(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Купил'),
        ('SELL', 'Продал'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, 
        verbose_name='Предмет')
    transaction_type = models.CharField(max_length=4, 
        choices=TRANSACTION_TYPES, default='BUY', verbose_name='Тип сделки')
    quantity = models.IntegerField(verbose_name='Количество')
    price_per_item = models.FloatField(verbose_name='Цена за единицу')
    commission = models.IntegerField(default=13, verbose_name='% Комиссии')
    total = models.FloatField(default=0.0)
    date = models.DateTimeField()
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        old_archived = ItemAddition.objects.get(id=self.id).archived if self.id else None
        super().save(*args, **kwargs)
        # Если это новая сделка или сделка была восстановлена из архива
        if old_archived is None or (
            old_archived is True and self.archived is False):
            if self.transaction_type == 'BUY':
                self.item.quantity += self.quantity
                self.item.total_price += self.quantity * self.price_per_item
            else:
                self.item.quantity -= self.quantity
                self.item.total_price -= self.quantity * self.price_per_item

        # Если сделка была добавлена в архив
        elif old_archived is False and self.archived is True:
            if self.transaction_type == 'BUY':
                self.item.quantity -= self.quantity
                self.item.total_price -= self.quantity * self.price_per_item
            else:
                self.item.quantity += self.quantity
                self.item.total_price += self.quantity * self.price_per_item
        self.item.save()

        # Если все предметы проданы, архивируем все сделки
        if self.item.quantity == 0:
            ItemAddition.objects.filter(item=self.item).update(archived=True)

        def __str__(self):
            return f'{self.get_transaction_type_display()} {self.item.name}'

    def delete(self, *args, **kwargs):
        if not self.archived:
            if self.transaction_type == 'BUY':
                self.item.quantity -= self.quantity
                self.item.total_price -= self.quantity * self.price_per_item
            else:
                self.item.quantity += self.quantity
                self.item.total_price += self.quantity * self.price_per_item
            self.item.save()
        super().delete(*args, **kwargs)


