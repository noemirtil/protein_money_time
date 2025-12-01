const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const mainProducts = document.getElementById('main-products-block')
const proteinIcon = document.getElementById('protein-icon');
const vitaminCIcon = document.getElementById('vitamin-c-icon'); // Correctly defined here

// Inactive classes
// Using the new Tailwind classes you defined
const inactiveProtein = ['bg-orange-100', 'text-brand-orange']; 
const inactiveVitamin = ['bg-green-100', 'text-brand-green'];

// Active classes
const activeProtein = ['bg-brand-orange', 'text-white', 'ring-4', 'ring-orange-200', 'scale-105'];
const activeVitamin = ['bg-brand-green', 'text-white', 'ring-4', 'ring-green-200', 'scale-105'];

let searchTimeout;

// ... (renderProducts function remains unchanged) ...

function renderProducts(products) {
    if (products.length === 0) {
        return '<p class="text-gray-600 text-center py-8">No products found</p>';
    }
    
    const cardsHTML = products.map(product => {
        const kcal = Math.round(product.energy * 0.239006);
        
        return `
            <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
                <h3 class="text-2xl font-extrabold text-gray-900 tracking-tight mb-2">
                    ${product.name ? product.name.toUpperCase() : 'N/A'}
                </h3>
                
                <hr class="bg-gray-900 h-px mb-2">
                <div class="flex flex-row justify-between text-base font-medium text-gray-700">
                    <p>Serving size</p>
                    <p>100g</p>
                </div>
                
                <hr class="bg-gray-900 h-3 my-4">
                
                <p class="text-xs font-medium text-gray-500 mb-2">Amount per serving (per 100g)</p>
                
                <div class="grid grid-cols-2 items-baseline border-b border-gray-200 py-1">
                    <p class="text-lg font-semibold text-gray-700">Energy</p>
                    <p class="text-xl font-bold text-right text-gray-700">${product.energy} kj</p>
                    <p class="col-span-2 text-xl font-bold text-right text-gray-700">${kcal} kcal</p>
                </div>

                ${product.fat != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Fat</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.fat.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.sat_fat != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1 pl-4">
                    <p class="text-sm font-light text-gray-600">— Saturated Fat</p>
                    <p class="text-sm font-normal text-right text-gray-600">${product.sat_fat.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.carbs != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Carbohydrates</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.carbs.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.sugars != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1 pl-4">
                    <p class="text-sm font-light text-gray-600">— Sugars</p>
                    <p class="text-sm font-normal text-right text-gray-600">${product.sugars.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.fiber != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Fiber</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.fiber.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.protein ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Protein</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.protein.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.sodium != null ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Sodium</p>
                    <p class="text-base font-semibold text-right text-gray-700">${(product.sodium * 1000).toFixed(1)} mg</p>
                </div>
                ` : ''}

                ${product.c_vitamin != null ? `
                <div class="flex justify-between py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Vitamin C</p>
                    <p class="text-base font-semibold text-right text-gray-700">${(product.c_vitamin * 1000).toFixed(1)} mg</p>
                </div>
                ` : ''}
                
                <hr class="bg-gray-900 h-px mt-4 mb-2">

                <div class="text-sm text-gray-600 space-y-1">
                    ${product.brand_name ? `<p>Brand: <span class="font-bold">${product.brand_name}</span></p>` : ''}
                    
                    ${product.nutr_score_fr != null ? `
                    <p>Nutri-Score: ${product.nutr_score_fr} 
                        <span class="bg-${product.nutri_color}-600 font-bold text-white rounded-lg p-1 text-center">
                            ${product.nutri_letter}
                        </span>
                    </p>
                    ` : ''}

                    ${product.price && product.currency_code ? `
                    <p>Latest Price: <span class="font-semibold">${product.currency_code} ${parseFloat(product.price/2).toFixed(2)}</span> 
                        ${product.price_date ? `(${new Date(product.price_date).toLocaleDateString()})` : ''}
                    </p>
                    ` : ''}

                    ${product.store_name ? `<p>Last Seen At: <span class="font-semibold text-gray-800">${product.store_name}</span></p>` : ''}
                    
                    ${product.ingredients_text ? `
                    <details class="pt-1">
                        <summary class="cursor-pointer font-medium text-xs">Ingredients</summary>
                        <p class="text-xs mt-1 italic max-h-16 overflow-y-auto">${product.ingredients_text}</p>
                    </details>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    return `<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3">${cardsHTML}</div>`;
}

searchInput.addEventListener('input', () => {
    const keyword = searchInput.value.trim();
    const paginationDiv = document.querySelector('.pagination');
    
    clearTimeout(searchTimeout);
    
    if (keyword.length < 2) {
        searchResults.classList.add('hidden');
        mainProducts.classList.remove('hidden');
        paginationDiv.classList.remove('hidden');
        return;
    }
    
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/api/search?keyword=${encodeURIComponent(keyword)}`);
            const data = await response.json();
            
            console.log('Search results:', data);
            
            mainProducts.classList.add('hidden');
            paginationDiv.classList.add('hidden');
            searchResults.classList.remove('hidden');
            
            const resultCount = `<p class="text-gray-600 mb-4">Found ${data.count} products</p>`;
            searchResults.innerHTML = resultCount + renderProducts(data.products);
            
        } catch (error) {
            console.error('Search error:', error);
            searchResults.innerHTML = '<p class="text-red-600">Error loading results</p>';
        }
    }, 300);
});


// --- KEEP ONLY THIS Initialization Logic ---
const urlParams = new URLSearchParams(window.location.search);
const currentSort = urlParams.get('sort');

function setIconState(icon, isActive, activeClasses, inactiveClasses) {
    if (icon) {
        // Clear both active and inactive classes first (in case of residue)
        icon.classList.remove(...activeClasses, ...inactiveClasses);
        
        // Apply the correct state
        if (isActive) {
            icon.classList.add(...activeClasses);
        } else {
            icon.classList.add(...inactiveClasses);
        }
    }
}

// Set Protein Icon State
const proteinActive = currentSort === 'protein_value';
setIconState(proteinIcon, proteinActive, activeProtein, inactiveProtein);

// Set Vitamin C Icon State
const vitaminActive = currentSort === 'vitamin_c_value'; // Checks for the correct value
setIconState(vitaminCIcon, vitaminActive, activeVitamin, inactiveVitamin);

// Add these click handlers to the end of api-search.js

function handleScoreClick(event) {
    // 1. Get the requested sort type
    const sortType = event.currentTarget.dataset.sort;
    const keyword = searchInput.value.trim();

    // 2. If there's a keyword, perform a dynamic search
    if (keyword.length >= 2) {
        // Run the search with the keyword AND the new sort type
        performDynamicSearch(keyword, sortType);
    } else {
        // If there's no keyword, revert to the old full page reload for the main view
        window.location.href = `/?sort=${sortType}`;
    }
}

// Re-wire your event listeners (since the old functions are removed)
if (proteinIcon) {
    proteinIcon.addEventListener('click', handleScoreClick);
}
if (vitaminCIcon) {
    vitaminCIcon.addEventListener('click', handleScoreClick);
}

// 3. Create a new function to combine keyword and sort search
async function performDynamicSearch(keyword, sortType) {
    const paginationDiv = document.querySelector('.pagination');
    
    // Deactivate the other icon manually in JS (visual feedback)
    if (sortType === 'protein_value') {
        setIconState(vitaminCIcon, false, activeVitamin, inactiveVitamin);
        setIconState(proteinIcon, true, activeProtein, inactiveProtein);
    } else if (sortType === 'vitamin_c_value') {
        setIconState(proteinIcon, false, activeProtein, inactiveProtein);
        setIconState(vitaminCIcon, true, activeVitamin, inactiveVitamin);
    }
    
    try {
        // Update the API endpoint to include the 'sort' parameter
        const response = await fetch(`/api/search?keyword=${encodeURIComponent(keyword)}&sort=${sortType}`);
        const data = await response.json();
        
        // ... (rest of search rendering logic remains the same) ...
        mainProducts.classList.add('hidden');
        paginationDiv.classList.add('hidden');
        searchResults.classList.remove('hidden');
        
        const resultCount = `<p class="text-gray-600 mb-4">Found ${data.count} products</p>`;
        searchResults.innerHTML = resultCount + renderProducts(data.products);
        
    } catch (error) {
        console.error('Search error:', error);
        searchResults.innerHTML = '<p class="text-red-600">Error loading results</p>';
    }
}