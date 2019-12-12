from django.shortcuts import render
from django.views import generic

from django.db.models import Count

from killboard.models import VictimLog, Item

# Create your views here.

__all__ = ['KillBoard']

class KillBoard(generic.ListView):
    template_name = "killboard/toplist.html"
    context_object_name = "context"

    def get_queryset(self):
        data = VictimLog.objects.all()

        return {'data': data}