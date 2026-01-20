from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView
from django.views.decorators.http import require_http_methods

from .forms import ItemForm
from .models import Category, Item


def is_admin(user):
    return user.is_authenticated and user.is_staff


class LandingPageView(TemplateView):
    template_name = "values/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "featured_items": Item.objects.filter(featured=True)[:6],
                "total_items": Item.objects.count(),
            }
        )
        return context


class ItemListView(ListView):
    model = Item
    template_name = "values/item_list.html"
    context_object_name = "items"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Item.objects.select_related("category")
            .all()
            .order_by("-featured", "-value", "name")
        )
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category")
        rarity = self.request.GET.get("rarity")
        item_type = self.request.GET.get("item_type")
        trend = self.request.GET.get("trend")
        min_value = self.request.GET.get("min_value")
        max_value = self.request.GET.get("max_value")

        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(notes__icontains=query)
                | Q(obtained_from__icontains=query)
            )
        if category:
            qs = qs.filter(category__slug=category)
        if rarity:
            qs = qs.filter(rarity=rarity)
        if item_type:
            qs = qs.filter(item_type=item_type)
        if trend:
            qs = qs.filter(trend=trend)
        if min_value and min_value.isdigit():
            qs = qs.filter(value__gte=int(min_value))
        if max_value and max_value.isdigit():
            qs = qs.filter(value__lte=int(max_value))

        sort = self.request.GET.get("sort")
        if sort == "value_asc":
            qs = qs.order_by("value", "name")
        elif sort == "name":
            qs = qs.order_by("name")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "rarity_choices": Item.Rarity.choices,
                "type_choices": Item.ItemType.choices,
                "trend_choices": Item.Trend.choices,
                "active_filters": self.request.GET,
                "is_admin": self.request.user.is_authenticated and self.request.user.is_staff,
            }
        )
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "values/item_detail.html"
    context_object_name = "item"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_authenticated and self.request.user.is_staff
        return context


class TradeCalculatorView(TemplateView):
    template_name = "values/trade_calculator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "rarity_choices": Item.Rarity.choices,
            }
        )
        return context


@require_http_methods(["GET"])
def api_items_list(request):
    """API endpoint to fetch items for the trade calculator modal"""
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category")
    rarity = request.GET.get("rarity")
    sort = request.GET.get("sort", "name")

    qs = Item.objects.select_related("category").all()

    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(notes__icontains=query))
    if category:
        qs = qs.filter(category__slug=category)
    if rarity:
        qs = qs.filter(rarity=rarity)

    if sort == "value_desc":
        qs = qs.order_by("-value", "name")
    elif sort == "value_asc":
        qs = qs.order_by("value", "name")
    elif sort == "rarity":
        rarity_order = {
            "exotic": 0,
            "limited": 1,
            "mythic": 2,
            "legendary": 3,
            "rare": 4,
            "uncommon": 5,
            "common": 6,
        }
        qs = sorted(qs, key=lambda x: rarity_order.get(x.rarity, 7))
    else:
        qs = qs.order_by("name")

    items_data = []
    for item in qs[:200]:  # Limit to 200 items for performance
        items_data.append(
            {
                "id": item.id,
                "name": item.name,
                "slug": item.slug,
                "value": item.value,
                "image_url": item.image_url or "",
                "category": item.category.name,
                "category_color": item.category.color,
                "rarity": item.get_rarity_display(),
                "rarity_key": item.rarity,
            }
        )

    return JsonResponse({"items": items_data})


class CustomLoginView(LoginView):
    template_name = 'values/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('values:landing')

    def get_success_url(self):
        return self.request.GET.get('next', self.next_page)


def logout_view(request):
    logout(request)
    return redirect('values:landing')


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin (staff) access"""
    login_url = 'values:login'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class ItemCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'values/item_form.html'
    success_url = reverse_lazy('values:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Item'
        return context


class ItemUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'values/item_form.html'
    slug_field = 'slug'
    success_url = reverse_lazy('values:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit {self.object.name}'
        return context

# Create your views here.
