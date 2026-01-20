from django.urls import path

from .views import (
    ItemDetailView,
    ItemListView,
    LandingPageView,
    TradeCalculatorView,
    api_items_list,
)

app_name = "values"

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),
    path("items/", ItemListView.as_view(), name="item_list"),
    path("calculator/", TradeCalculatorView.as_view(), name="trade_calculator"),
    path("api/items/", api_items_list, name="api_items_list"),
    path("<slug:slug>/", ItemDetailView.as_view(), name="item_detail"),
]

