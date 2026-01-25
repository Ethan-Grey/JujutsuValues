from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    FormView,
)
from django.views.decorators.http import require_http_methods
import json

from .forms import ItemForm, UserRegistrationForm, ValueChangeRequestForm
from .models import Category, Item, InventoryItem, SavedTrade, VerificationToken, Profile, ValueChangeRequest
from django.contrib.auth.models import Group
from django.utils import timezone


def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_value_reviewer(user):
    """Check if user is in the Value Reviewers group"""
    if not user.is_authenticated:
        return False
    try:
        reviewers_group = Group.objects.get(name="Value Reviewers")
        return reviewers_group in user.groups.all()
    except Group.DoesNotExist:
        return False


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
        context['is_value_reviewer'] = is_value_reviewer(self.request.user)
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


class RegistrationView(FormView):
    template_name = "values/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user)
        return redirect("values:profile")


@require_http_methods(["GET"])
def verify_account(request, token):
    try:
        vt = VerificationToken.objects.select_related("user").get(token=token, is_used=False)
    except VerificationToken.DoesNotExist:
        return render(request, "values/verify_invalid.html", status=400)

    user = vt.user
    user.is_active = True
    user.save()

    profile = getattr(user, "profile", None)
    if profile:
        profile.is_verified = True
        profile.save()

    vt.is_used = True
    vt.save()

    return render(request, "values/verify_complete.html", {"verified_user": user})


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    inventory = (
        InventoryItem.objects.filter(user=request.user)
        .select_related("item", "item__category")
        .order_by("-added_at")
    )
    return render(
        request,
        "values/profile.html",
        {"profile": profile, "inventory_items": inventory},
    )


@login_required
@require_http_methods(["POST"])
def add_to_inventory(request, slug):
    item = get_object_or_404(Item, slug=slug)
    qty = 1
    try:
        if "quantity" in request.POST:
            qty = max(1, int(request.POST.get("quantity", "1")))
    except ValueError:
        qty = 1

    inv, created = InventoryItem.objects.get_or_create(user=request.user, item=item)
    inv.quantity += qty if not created else max(qty, 1)
    inv.save()
    return redirect(item.get_absolute_url())


@login_required
@require_http_methods(["POST"])
def remove_inventory_item(request, pk):
    inv = get_object_or_404(InventoryItem, pk=pk, user=request.user)
    inv.delete()
    return redirect("values:profile")


 # Saved trade calculator feature removed per request.


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


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def item_delete(request, slug):
    """Delete an item (admin only)"""
    item = get_object_or_404(Item, slug=slug)
    item_name = item.name
    item.delete()
    return redirect('values:item_list')



# Value Change Request Views

class ValueReviewerRequiredMixin(UserPassesTestMixin):
    """Mixin to require Value Reviewer group membership"""
    login_url = 'values:login'

    def test_func(self):
        return is_value_reviewer(self.request.user)


@login_required
@user_passes_test(is_value_reviewer)
def request_value_change(request, slug):
    """Allow value reviewers to submit value change requests"""
    item = get_object_or_404(Item, slug=slug)
    
    if request.method == 'POST':
        form = ValueChangeRequestForm(request.POST)
        if form.is_valid():
            value_request = form.save(commit=False)
            value_request.item = item
            value_request.requested_by = request.user
            value_request.current_value = item.value
            value_request.save()
            return redirect('values:value_requests')
    else:
        form = ValueChangeRequestForm(initial={'requested_value': item.value})
    
    return render(request, 'values/value_request_form.html', {
        'form': form,
        'item': item,
    })


@login_required
@user_passes_test(is_value_reviewer)
def value_requests_list(request):
    """List all value change requests submitted by the current reviewer"""
    requests = ValueChangeRequest.objects.filter(
        requested_by=request.user
    ).select_related('item', 'reviewed_by').order_by('-created_at')
    
    return render(request, 'values/value_requests_list.html', {
        'requests': requests,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_value_requests(request):
    """Superuser view to manage all value change requests"""
    status_filter = request.GET.get('status', 'pending')
    requests = ValueChangeRequest.objects.select_related(
        'item', 'requested_by', 'reviewed_by'
    ).order_by('-created_at')
    
    if status_filter != 'all':
        requests = requests.filter(status=status_filter)
    
    return render(request, 'values/admin_value_requests.html', {
        'requests': requests,
        'status_filter': status_filter,
        'status_choices': ValueChangeRequest.Status.choices,
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def approve_value_request(request, pk):
    """Superuser approves a value change request"""
    value_request = get_object_or_404(ValueChangeRequest, pk=pk, status=ValueChangeRequest.Status.PENDING)
    
    value_request.status = ValueChangeRequest.Status.APPROVED
    value_request.reviewed_by = request.user
    value_request.reviewed_at = timezone.now()
    value_request.review_notes = request.POST.get('review_notes', '')
    value_request.save()
    
    # Update the item value
    value_request.item.value = value_request.requested_value
    value_request.item.save()
    
    return redirect('values:admin_value_requests')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["POST"])
def reject_value_request(request, pk):
    """Superuser rejects a value change request"""
    value_request = get_object_or_404(ValueChangeRequest, pk=pk, status=ValueChangeRequest.Status.PENDING)
    
    value_request.status = ValueChangeRequest.Status.REJECTED
    value_request.reviewed_by = request.user
    value_request.reviewed_at = timezone.now()
    value_request.review_notes = request.POST.get('review_notes', '')
    value_request.save()
    
    return redirect('values:admin_value_requests')

# Create your views here.
