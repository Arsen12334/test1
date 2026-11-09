from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ItemForm
from .models import Item


class ItemListView(ListView):
    model = Item
    context_object_name = "items"


class ItemDetailView(DetailView):
    model = Item
    context_object_name = "item"


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy("crud:item_list")


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy("crud:item_list")


class ItemDeleteView(DeleteView):
    model = Item
    context_object_name = "item"
    success_url = reverse_lazy("crud:item_list")
