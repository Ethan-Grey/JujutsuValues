// Trade Calculator JavaScript

let currentSlot = null;
let currentSide = null;
let selectedItem = null;
let tradeData = {
    offer: Array(9).fill(null),
    request: Array(9).fill(null)
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTradeCalculator();
});

function initializeTradeCalculator() {
    // Set up slot click handlers
    document.querySelectorAll('.trade-slot').forEach(slot => {
        slot.addEventListener('click', function() {
            openItemSelectModal(this);
        });
    });

    // Set up search and filter handlers
    const searchInput = document.getElementById('itemSearchInput');
    const categoryFilter = document.getElementById('itemCategoryFilter');
    const rarityFilter = document.getElementById('itemRarityFilter');
    const sortSelect = document.getElementById('itemSort');

    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => loadItems(), 300);
        });
    }

    if (categoryFilter) {
        categoryFilter.addEventListener('change', loadItems);
    }

    if (rarityFilter) {
        rarityFilter.addEventListener('change', loadItems);
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', loadItems);
    }

    // Set up quantity modal handlers
    const confirmQuantityBtn = document.getElementById('confirmQuantityBtn');
    if (confirmQuantityBtn) {
        confirmQuantityBtn.addEventListener('click', confirmQuantity);
    }

    // Load items when modal opens
    const itemModal = document.getElementById('itemSelectModal');
    if (itemModal) {
        itemModal.addEventListener('show.bs.modal', function() {
            loadItems();
        });
    }

    updateTotals();
}

function openItemSelectModal(slotElement) {
    currentSlot = slotElement;
    currentSide = slotElement.dataset.side;
    const modal = new bootstrap.Modal(document.getElementById('itemSelectModal'));
    modal.show();
}

function loadItems() {
    const searchQuery = document.getElementById('itemSearchInput').value;
    const category = document.getElementById('itemCategoryFilter').value;
    const rarity = document.getElementById('itemRarityFilter').value;
    const sort = document.getElementById('itemSort').value;

    const params = new URLSearchParams();
    if (searchQuery) params.append('q', searchQuery);
    if (category) params.append('category', category);
    if (rarity) params.append('rarity', rarity);
    if (sort) params.append('sort', sort);

    const itemsGrid = document.getElementById('itemsGrid');
    const itemsLoading = document.getElementById('itemsLoading');
    const itemsEmpty = document.getElementById('itemsEmpty');

    itemsGrid.innerHTML = '';
    itemsLoading.style.display = 'block';
    itemsEmpty.style.display = 'none';

    fetch(`/api/items/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            itemsLoading.style.display = 'none';
            
            if (data.items.length === 0) {
                itemsEmpty.style.display = 'block';
                return;
            }

            data.items.forEach(item => {
                const itemCard = createItemCard(item);
                itemsGrid.appendChild(itemCard);
            });
        })
        .catch(error => {
            console.error('Error loading items:', error);
            itemsLoading.style.display = 'none';
            itemsEmpty.style.display = 'block';
            itemsEmpty.textContent = 'Error loading items. Please try again.';
        });
}

function createItemCard(item) {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4 col-lg-3';

    const card = document.createElement('div');
    card.className = 'modern-item-card card h-100 border-0';
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => selectItem(item));

    const imageContainer = document.createElement('div');
    imageContainer.className = 'modern-card-image';
    if (item.image_url) {
        const img = document.createElement('img');
        img.src = item.image_url;
        img.alt = item.name;
        imageContainer.appendChild(img);
    } else {
        imageContainer.className = 'modern-card-image no-image';
        imageContainer.innerHTML = '<i class="bi bi-image"></i>';
    }

    const cardBody = document.createElement('div');
    cardBody.className = 'modern-card-body';

    const badges = document.createElement('div');
    badges.className = 'modern-card-badges';
    
    const typeBadge = document.createElement('span');
    typeBadge.className = 'item-type-badge';
    typeBadge.textContent = item.category.toUpperCase();
    
    const rarityBadge = document.createElement('span');
    rarityBadge.className = 'rarity-badge rarity-' + item.rarity_key;
    rarityBadge.textContent = item.rarity.toUpperCase();
    
    badges.appendChild(typeBadge);
    badges.appendChild(rarityBadge);

    const category = document.createElement('div');
    category.className = 'modern-card-category';
    category.textContent = item.category.toUpperCase();

    const name = document.createElement('h5');
    name.className = 'modern-card-name';
    name.textContent = item.name;

    const valueDiv = document.createElement('div');
    valueDiv.className = 'modern-card-value';
    const valueAmount = document.createElement('span');
    valueAmount.className = 'value-amount';
    valueAmount.textContent = formatValue(item.value);
    valueDiv.appendChild(valueAmount);

    cardBody.appendChild(badges);
    cardBody.appendChild(category);
    cardBody.appendChild(name);
    cardBody.appendChild(valueDiv);

    card.appendChild(imageContainer);
    card.appendChild(cardBody);
    col.appendChild(card);

    return col;
}

function selectItem(item) {
    selectedItem = item;
    const itemModal = bootstrap.Modal.getInstance(document.getElementById('itemSelectModal'));
    itemModal.hide();
    
    // Show quantity modal
    const quantityModal = new bootstrap.Modal(document.getElementById('quantityModal'));
    document.getElementById('quantityInput').value = 1;
    quantityModal.show();
}

function confirmQuantity() {
    const quantity = parseInt(document.getElementById('quantityInput').value) || 1;
    
    if (!selectedItem || !currentSlot || !currentSide) return;

    const slotIndex = parseInt(currentSlot.dataset.slot);
    
    // Store item data
    tradeData[currentSide][slotIndex] = {
        id: selectedItem.id,
        name: selectedItem.name,
        value: selectedItem.value,
        image_url: selectedItem.image_url,
        category: selectedItem.category,
        category_color: selectedItem.category_color,
        quantity: quantity
    };

    // Update slot display
    updateSlotDisplay(currentSlot, tradeData[currentSide][slotIndex]);

    // Close quantity modal
    const quantityModal = bootstrap.Modal.getInstance(document.getElementById('quantityModal'));
    quantityModal.hide();

    // Reset selection
    selectedItem = null;
    currentSlot = null;
    currentSide = null;

    updateTotals();
}

function updateSlotDisplay(slotElement, itemData) {
    if (!itemData) {
        slotElement.innerHTML = `
            <div class="trade-slot-content">
                <span class="trade-slot-label">SELECT</span>
            </div>
        `;
        slotElement.addEventListener('click', function() {
            openItemSelectModal(this);
        });
        return;
    }

    const totalValue = itemData.value * itemData.quantity;
    const side = slotElement.dataset.side;
    const slotIndex = slotElement.dataset.slot;
    
    slotElement.innerHTML = `
        <div class="trade-slot-content">
            ${itemData.image_url ? `<img src="${itemData.image_url}" alt="${itemData.name}" class="trade-slot-image">` : ''}
            <div class="trade-slot-info">
                <div class="trade-slot-name">${itemData.name}</div>
                <div class="trade-slot-value">${formatValue(totalValue)}</div>
                ${itemData.quantity > 1 ? `<div class="trade-slot-quantity">x${itemData.quantity}</div>` : ''}
            </div>
            <button class="trade-slot-remove" onclick="removeItem(event, '${side}', ${slotIndex})">
                <i class="bi bi-x"></i>
            </button>
        </div>
    `;
    
    // Re-add click handler to allow replacing items
    slotElement.addEventListener('click', function(e) {
        if (!e.target.closest('.trade-slot-remove')) {
            openItemSelectModal(this);
        }
    });
}

function removeItem(event, side, slotIndex) {
    event.stopPropagation();
    event.preventDefault();
    tradeData[side][slotIndex] = null;
    const slotElement = document.querySelector(`[data-side="${side}"][data-slot="${slotIndex}"]`);
    if (slotElement) {
        updateSlotDisplay(slotElement, null);
    }
    updateTotals();
}

function updateTotals() {
    let offerTotal = 0;
    let requestTotal = 0;

    tradeData.offer.forEach(item => {
        if (item) {
            offerTotal += item.value * item.quantity;
        }
    });

    tradeData.request.forEach(item => {
        if (item) {
            requestTotal += item.value * item.quantity;
        }
    });

    document.getElementById('offerTotal').textContent = formatValue(offerTotal);
    document.getElementById('requestTotal').textContent = formatValue(requestTotal);
    document.getElementById('summaryOfferTotal').textContent = formatValue(offerTotal);
    document.getElementById('summaryRequestTotal').textContent = formatValue(requestTotal);

    const difference = offerTotal - requestTotal;
    const differenceElement = document.getElementById('summaryDifference');
    differenceElement.textContent = formatValue(Math.abs(difference));
    
    if (difference > 0) {
        differenceElement.className = 'text-success';
        differenceElement.textContent = '+' + formatValue(difference);
    } else if (difference < 0) {
        differenceElement.className = 'text-danger';
        differenceElement.textContent = '-' + formatValue(Math.abs(difference));
    } else {
        differenceElement.className = '';
        differenceElement.textContent = '0';
    }
}

function formatValue(value) {
    if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'K';
    }
    return value.toString();
}

// Make removeItem available globally
window.removeItem = removeItem;
