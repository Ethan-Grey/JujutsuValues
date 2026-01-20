from django.urls import path

from .views import (
    ItemCreateView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
    LandingPageView,
    TradeCalculatorView,
    CustomLoginView,
    RegistrationView,
    profile_view,
    api_items_list,
    logout_view,
    verify_account,
    add_to_inventory,
    remove_inventory_item,
    request_value_change,
    value_requests_list,
    admin_value_requests,
    approve_value_request,
    reject_value_request,
)

app_name = "values"

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing"),
    path("items/", ItemListView.as_view(), name="item_list"),
    path("calculator/", TradeCalculatorView.as_view(), name="trade_calculator"),
    path("api/items/", api_items_list, name="api_items_list"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/<str:token>/", verify_account, name="verify"),
    path("profile/", profile_view, name="profile"),
    path("profile/inventory/add/<slug:slug>/", add_to_inventory, name="inventory_add"),
    path("profile/inventory/remove/<int:pk>/", remove_inventory_item, name="inventory_remove"),
    path("items/create/", ItemCreateView.as_view(), name="item_create"),
    path("items/<slug:slug>/edit/", ItemUpdateView.as_view(), name="item_edit"),
    path("items/<slug:slug>/request-value-change/", request_value_change, name="request_value_change"),
    path("value-requests/", value_requests_list, name="value_requests"),
    path("manage/value-requests/", admin_value_requests, name="admin_value_requests"),
    path("manage/value-requests/<int:pk>/approve/", approve_value_request, name="approve_value_request"),
    path("manage/value-requests/<int:pk>/reject/", reject_value_request, name="reject_value_request"),
    path("<slug:slug>/", ItemDetailView.as_view(), name="item_detail"),
]

 