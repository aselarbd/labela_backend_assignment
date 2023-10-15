from . import views
from django.urls import path

urlpatterns = [
    path("", views.CartRetrieveView.as_view(), name="get_shopping_cart"),
    path("add", views.AddCartView.as_view(), name="add_shopping_cart"),
    path("remove", views.RemoveCartView.as_view(), name="remove_shopping_cart"),
]
