from django.db import models

__all__ = {"Item", "VictimLog", "Item2Victim"}

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=64, default=None, unique=True)
    price = models.IntegerField(default=0)


class Item2Victim(models.Model):
    item = models.ForeignKey("Item", default=None, null=True, on_delete=models.CASCADE, )
    victim = models.ForeignKey("VictimLog", default=None, null=True, on_delete=models.CASCADE, )
    count = models.IntegerField(default=0)


class VictimLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event_id = models.IntegerField(default=None, null=True)

    items = models.ManyToManyField("Item", through="Item2Victim")

    class Meta:
        unique_together = ("timestamp", "event_id")