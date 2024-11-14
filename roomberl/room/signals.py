from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from room.models import RoomType


@receiver(pre_save, sender=RoomType)
def update_hostel_price_on_roomtype_price_change(sender, instance: RoomType, **kwargs):
    """
    Handles price change for a RoomType. Subtracts the old price and adds the new price to the hostel.
    """
    try:
        old_instance = RoomType.objects.get(pk=instance.pk)
        old_price = old_instance.price
    except RoomType.DoesNotExist:
        old_price = 0  # If the instance is new, there's no old price

    if old_price != instance.price:  # Only adjust if the price has changed
        if instance.hostel:
            instance.hostel.price -= old_price
            instance.hostel.price += instance.price
            instance.hostel.save()


@receiver(post_save, sender=RoomType)
def update_hostel_price_on_roomtype_creation(sender, instance: RoomType, **kwargs):
    """
    Adds the price of the newly created RoomType to the hostel's price.
    """
    if instance.hostel:
        instance.hostel.price += instance.price
        instance.hostel.save()


@receiver(post_delete, sender=RoomType)
def subtract_room_type_price_on_delete(sender, instance: RoomType, **kwargs):
    """
    Subtracts the price of a deleted RoomType from the hostel's price.
    """
    if instance.hostel:
        instance.hostel.price -= instance.price
        instance.hostel.save()


def init_singals():
    pass
