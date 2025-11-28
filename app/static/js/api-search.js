const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const mainProducts = document.querySelector('.grid');

let searchTimeout;

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
                
                <!-- Energy -->
                <div class="grid grid-cols-2 items-baseline border-b border-gray-200 py-1">
                    <p class="text-lg font-semibold text-gray-700">Energy</p>
                    <p class="text-xl font-bold text-right text-gray-700">${product.energy} kj</p>
                    <p class="col-span-2 text-xl font-bold text-right text-gray-700">${kcal} kcal</p>
                </div>

                ${product.fat ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Fat</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.fat.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.protein ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Protein</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.protein.toFixed(1)} g</p>
                </div>
                ` : ''}

                ${product.carbs ? `
                <div class="flex justify-between border-b border-gray-200 py-1">
                    <p class="text-base font-normal text-gray-700 ml-2">Carbohydrates</p>
                    <p class="text-base font-semibold text-right text-gray-700">${product.carbs.toFixed(1)} g</p>
                </div>
                ` : ''}
                
                <hr class="bg-gray-900 h-px mt-4 mb-2">

                <div class="text-sm text-gray-600 space-y-1">
                    ${product.brand_name ? `<p>Brand: <span class="font-bold">${product.brand_name}</span></p>` : ''}
                    
                    ${product.nutri_letter ? `
                    <p>Nutri-Score: 
                        <span class="bg-${product.nutri_color}-600 font-bold text-white rounded-lg px-2 py-1">
                            ${product.nutri_letter}
                        </span>
                    </p>
                    ` : ''}

                    ${product.store_name ? `<p>Store: <span class="font-semibold">${product.store_name}</span></p>` : ''}
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