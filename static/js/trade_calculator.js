// Trade Calculator - Simplified Popup Version
(function() {
    'use strict';
    
    // State
    const state = {
        currentSide: null,
        selectedItem: null,
        items: {
            offer: [],
            request: []
        }
    };
    
    // Initialize
    function init() {
        console.log('Trade calculator initializing...');
        
        // Setup add buttons
        document.querySelectorAll('.add-item-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                state.currentSide = this.getAttribute('data-side');
                state.selectedItem = null;
                console.log('Opening modal for side:', state.currentSide);
                openModal();
            });
        });
        
        // Setup confirm button
        const confirmBtn = document.getElementById('confirmAddBtn');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', confirmAdd);
        }
        
        // Setup search/filter
        const searchInput = document.getElementById('modalSearch');
        const categorySelect = document.getElementById('modalCategory');
        const raritySelect = document.getElementById('modalRarity');
        
        if (searchInput) {
            let timeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(timeout);
                timeout = setTimeout(loadItems, 300);
            });
        }
        
        if (categorySelect) {
            categorySelect.addEventListener('change', loadItems);
        }
        
        if (raritySelect) {
            raritySelect.addEventListener('change', loadItems);
        }
        
        // Load items when modal opens
        const modal = document.getElementById('itemModal');
        if (modal) {
            modal.addEventListener('show.bs.modal', function() {
                resetModal();
                loadItems();
            });
        }
        
        updateTotals();
        console.log('Trade calculator ready');
    }
    
    function openModal() {
        const modalEl = document.getElementById('itemModal');
        if (!modalEl) {
            console.error('Modal not found!');
            return;
        }
        
        if (typeof bootstrap === 'undefined') {
            console.error('Bootstrap not loaded!');
            return;
        }
        
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
    
    function resetModal() {
        state.selectedItem = null;
        document.getElementById('modalSearch').value = '';
        document.getElementById('modalCategory').value = '';
        document.getElementById('modalRarity').value = '';
        document.getElementById('selectedItemDisplay').style.display = 'none';
        document.getElementById('confirmAddBtn').disabled = true;
        document.getElementById('qtyInput').value = 1;
    }
    
    function loadItems() {
        const search = document.getElementById('modalSearch')?.value || '';
        const category = document.getElementById('modalCategory')?.value || '';
        const rarity = document.getElementById('modalRarity')?.value || '';
        
        const params = new URLSearchParams();
        if (search) params.set('q', search);
        if (category) params.set('category', category);
        if (rarity) params.set('rarity', rarity);
        params.set('sort', 'name');
        
        const listEl = document.getElementById('modalItemsList');
        const loadingEl = document.getElementById('modalLoading');
        const emptyEl = document.getElementById('modalEmpty');
        
        if (!listEl || !loadingEl || !emptyEl) return;
        
        listEl.innerHTML = '';
        loadingEl.style.display = 'block';
        emptyEl.style.display = 'none';
        
        fetch(`/api/items/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                loadingEl.style.display = 'none';
                
                if (!data.items || data.items.length === 0) {
                    emptyEl.style.display = 'block';
                    return;
                }
                
                data.items.forEach(item => {
                    const itemEl = createItemElement(item);
                    listEl.appendChild(itemEl);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                loadingEl.style.display = 'none';
                emptyEl.style.display = 'block';
                emptyEl.innerHTML = '<div class="text-danger">Error loading items</div>';
            });
    }
    
    function createItemElement(item) {
        const div = document.createElement('div');
        div.className = 'modal-item mb-2 p-2 border rounded cursor-pointer';
        div.style.cursor = 'pointer';
        div.style.transition = 'all 0.2s';
        
        div.innerHTML = `
            <div class="d-flex align-items-center gap-3">
                ${item.image_url ? `<img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.name)}" style="width: 60px; height: 60px; object-fit: contain;">` : '<div style="width: 60px; height: 60px; background: #333; display: flex; align-items: center; justify-content: center; color: #666;"><i class="bi bi-image"></i></div>'}
                <div class="flex-grow-1">
                    <div class="fw-bold">${escapeHtml(item.name)}</div>
                    <div class="small text-muted">
                        <span class="badge bg-secondary">${escapeHtml(item.rarity)}</span>
                        <span class="ms-2">${formatValue(item.value)}</span>
                    </div>
                </div>
            </div>
        `;
        
        div.addEventListener('click', function() {
            selectItem(item);
        });
        
        div.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(220, 38, 38, 0.1)';
            this.style.borderColor = '#dc2626';
        });
        
        div.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            this.style.borderColor = '';
        });
        
        return div;
    }
    
    function selectItem(item) {
        console.log('Item selected:', item.name);
        state.selectedItem = item;
        
        // Show selected item display
        const display = document.getElementById('selectedItemDisplay');
        const img = document.getElementById('selectedItemImg');
        const name = document.getElementById('selectedItemName');
        const value = document.getElementById('selectedItemValue');
        
        if (item.image_url) {
            img.src = item.image_url;
            img.style.display = 'block';
        } else {
            img.style.display = 'none';
        }
        
        name.textContent = item.name;
        value.textContent = `${item.rarity} • ${formatValue(item.value)}`;
        display.style.display = 'block';
        
        // Enable confirm button
        document.getElementById('confirmAddBtn').disabled = false;
        
        // Scroll to selected item display
        display.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    function confirmAdd() {
        if (!state.selectedItem || !state.currentSide) {
            console.error('Cannot add: missing item or side');
            return;
        }
        
        const qtyInput = document.getElementById('qtyInput');
        const quantity = parseInt(qtyInput?.value) || 1;
        
        console.log('Adding:', state.selectedItem.name, 'x' + quantity, 'to', state.currentSide);
        
        // Add item
        state.items[state.currentSide].push({
            id: state.selectedItem.id,
            name: state.selectedItem.name,
            value: state.selectedItem.value,
            image_url: state.selectedItem.image_url,
            quantity: quantity
        });
        
        // Close modal
        const modalEl = document.getElementById('itemModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) {
            modal.hide();
        }
        
        // Update display
        renderAll();
    }
    
    function renderAll() {
        renderSide('offer');
        renderSide('request');
        updateTotals();
    }
    
    function renderSide(side) {
        const container = document.getElementById(side + 'Items');
        if (!container) return;
        
        container.innerHTML = '';
        
        state.items[side].forEach((item, index) => {
            const itemEl = createTradeItemElement(item, side, index);
            container.appendChild(itemEl);
        });
    }
    
    function createTradeItemElement(item, side, index) {
        const div = document.createElement('div');
        div.className = 'trade-item';
        
        const totalValue = item.value * item.quantity;
        const imgHtml = item.image_url
            ? `<img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(item.name)}" class="trade-item-img">`
            : '<div class="trade-item-img no-img"><i class="bi bi-image"></i></div>';
        
        div.innerHTML = `
            ${imgHtml}
            <div class="trade-item-details">
                <div class="trade-item-name">${escapeHtml(item.name)}</div>
                <div class="trade-item-meta">
                    ${item.quantity > 1 ? `<span class="trade-item-qty">x${item.quantity}</span>` : ''}
                    <span class="trade-item-value">${formatValue(totalValue)}</span>
                </div>
            </div>
            <button class="trade-item-remove" type="button">
                <i class="bi bi-x"></i>
            </button>
        `;
        
        const removeBtn = div.querySelector('.trade-item-remove');
        removeBtn.addEventListener('click', function() {
            removeItem(side, index);
        });
        
        return div;
    }
    
    function removeItem(side, index) {
        state.items[side].splice(index, 1);
        renderAll();
    }
    
    function updateTotals() {
        let offerTotal = 0;
        let requestTotal = 0;
        
        state.items.offer.forEach(item => {
            offerTotal += item.value * item.quantity;
        });
        
        state.items.request.forEach(item => {
            requestTotal += item.value * item.quantity;
        });
        
        const offerEl = document.getElementById('offerTotal');
        const requestEl = document.getElementById('requestTotal');
        if (offerEl) offerEl.textContent = formatValue(offerTotal);
        if (requestEl) requestEl.textContent = formatValue(requestTotal);
        
        const summaryOffer = document.getElementById('summaryOffer');
        const summaryRequest = document.getElementById('summaryRequest');
        const summaryDiff = document.getElementById('summaryDiff');
        
        if (summaryOffer) summaryOffer.textContent = formatValue(offerTotal);
        if (summaryRequest) summaryRequest.textContent = formatValue(requestTotal);
        
        if (summaryDiff) {
            const diff = offerTotal - requestTotal;
            if (diff > 0) {
                summaryDiff.textContent = '+' + formatValue(diff);
                summaryDiff.style.color = 'var(--success)';
            } else if (diff < 0) {
                summaryDiff.textContent = '-' + formatValue(Math.abs(diff));
                summaryDiff.style.color = 'var(--danger)';
            } else {
                summaryDiff.textContent = '0';
                summaryDiff.style.color = 'var(--text-primary)';
            }
        }
    }
    
    function formatValue(value) {
        if (value >= 1000) {
            return (value / 1000).toFixed(1) + 'K';
        }
        return value.toString();
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
