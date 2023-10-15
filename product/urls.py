from . import views
from django.urls import path

urlpatterns = [
    path("", views.ProductListCreateView.as_view(), name="product_list_create"),
    path(
        "<int:pk>",
        views.ProductRetrieveUpdateDeleteView.as_view(),
        name="product_details_update_delete",
    ),
]
