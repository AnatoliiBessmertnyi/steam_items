from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    """Модель предмета. Представляет собой предмет, который может быть куплен
    или продан."""
    name = models.CharField(max_length=200, unique=True)
    link = models.URLField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0.0)
    spread = models.FloatField(default=0.0)
    last_deal_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-last_deal_time']

    def __str__(self):
        return self.name


class ItemAddition(models.Model):
    """Модель добавления предмета. Представляет собой сделку с предметом."""
    TRANSACTION_TYPES = [
        ('BUY', 'Купил'),
        ('SELL', 'Продал'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    transaction_type = models.CharField(
        max_length=4,
        choices=TRANSACTION_TYPES,
        default='BUY',
        verbose_name='Тип сделки'
    )
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


@receiver(post_save, sender=ItemAddition)
def update_item_last_deal_time(sender, instance, **kwargs):
    """Обработчик сигнала, который вызывается после сохранения экземпляра
    ItemAddition. Обновляет поле last_deal_time в соответствующем экземпляре
    Item временем последней неархивированной сделки.

    Если сделка архивирована, то время последней сделки у предмета обновляется
    до времени последней неархивированной сделки. Если все сделки с предметом
    архивированы, то last_deal_time устанавливается в None.

    Если сделка не архивирована, то last_deal_time устанавливается во время
    этой сделки."""
    if instance.archived:
        last_non_archived_deal = ItemAddition.objects.filter(
            item=instance.item,
            archived=False
        ).order_by('-date').first()
        if last_non_archived_deal is not None:
            instance.item.last_deal_time = last_non_archived_deal.date
        else:
            instance.item.last_deal_time = None
    else:
        instance.item.last_deal_time = instance.date
    instance.item.save()
