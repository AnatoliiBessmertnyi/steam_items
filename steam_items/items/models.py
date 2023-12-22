from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    link = models.URLField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f'{self.get_transaction_type_display()} {self.item.name}'

