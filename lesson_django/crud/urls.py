from django.urls import path

from . import views

app_name = "crud"

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path("create/", views.ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("<int:pk>/edit/", views.ItemUpdateView.as_view(), name="item_update"),
    path("<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
]
