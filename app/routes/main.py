from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.db.connection import get_db

main_bp = Blueprint('main', __name__)

def _assign_nutriscore_data(score):
    """Calculate Nutri-Score letter and color from score"""
    if score is None:
        return None, None
    
    try:
        score = float(score)
    except (ValueError, TypeError):
        return None, None

    # E: 19 to 40+
    if score >= 19:
        return 'E', 'red'
    # D: 11 to 18
    elif score >= 11:
        return 'D', 'orange'
    # C: 3 to 10
    elif score >= 3:
        return 'C', 'yellow'
    # B: 0 to 2
    elif score >= 0:
        return 'B', 'lime'
    # A: -15 to -1
    elif score >= -15: 
        return 'A', 'green'
    # Fallback for unexpected scores below -15
    return 'A', 'green'

def _get_products(cur, limit, offset, sort_column='protein', **kwargs):
    """
    Flexible product query with optional filters
    
    Args:
        cur: Database cursor
        limit: Number of results
        offset: Pagination offset
        **kwargs: Optional filters
            - keyword: Search term for name/brand/store
            - min_protein: Minimum protein amount
            - max_fat: Maximum fat amount
            - nutri_score_max: Maximum nutri-score
    """
    # Base query parts
    base_query = """
        SELECT
            p.id, p.name, p.energy, p.fat, p.sat_fat, p.sodium,
            p.carbs, p.fiber, p.sugars, p.protein, p.c_vitamin,
            p.nutr_score_fr, p.ingredients_text,
            b.name as brand_name,
            pr.price, pr.weight, pr.date as price_date,
            s.name as store_name,
            c.country as country_name,
            curr.currency_code
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN LATERAL (
            SELECT price, weight, date, store_id, currency_id
            FROM prices
            WHERE product_id = p.id
            ORDER BY date DESC
            LIMIT 1
        ) pr ON true
        LEFT JOIN stores s ON pr.store_id = s.id
        LEFT JOIN countries c ON s.country_id = c.id
        LEFT JOIN currencies curr ON pr.currency_id = curr.id
    """
    
    conditions = []
    params = []
    
    # Add search keyword filter
    if 'keyword' in kwargs and kwargs['keyword']:
        keyword = kwargs['keyword']
        conditions.append("""
            (p.name ILIKE %s OR b.name ILIKE %s OR s.name ILIKE %s)
        """)
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
    
    # Add protein filter
    if 'min_protein' in kwargs and kwargs['min_protein'] is not None:
        conditions.append("p.protein >= %s")
        params.append(kwargs['min_protein'])
    
    # Add fat filter
    if 'max_fat' in kwargs and kwargs['max_fat'] is not None:
        conditions.append("p.fat <= %s")
        params.append(kwargs['max_fat'])
    
    # Add nutri-score filter
    if 'nutri_score_max' in kwargs and kwargs['nutri_score_max'] is not None:
        conditions.append("p.nutr_score_fr <= %s")
        params.append(kwargs['nutri_score_max'])
    
    # Build WHERE clause
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    # Add ordering and pagination
    base_query += f" ORDER BY p.{sort_column} DESC NULLS LAST LIMIT %s OFFSET %s" # <-- USE f-string for dynamic column
    params.extend([limit, offset])
    
    cur.execute(base_query, params)
    return cur.fetchall()

def get_protein_score():
    # To look for the highest Protein Score cost-effective products
    query = """
    SELECT
        products.id,
        products.name,
        products.energy,
        products.fat,
        products.sat_fat,
        products.sodium,
        products.carbs,
        products.fiber,
        products.sugars,
        products.protein,
        products.c_vitamin,
        products.nutr_score_fr,
        products.ingredients_text,
        brands."name" AS brand_name,
        prices.price * 0.01 AS price,
        prices.weight,
        ROUND((prices.price * 0.01) / (prices.weight * 0.001), 2) AS price_per_kg,
        prices."date" AS price_date,
        stores."name" AS store_name,
        countries.country,
        currencies.currency_code,
        CAST((products.protein / GREATEST(SUM(prices.weight * prices.price), 0.01))
        / GREATEST(products.fat, 0.001) * 10000000 AS INT) AS protein_score
    FROM products
    LEFT JOIN prices ON prices.product_id = products.id
    LEFT JOIN brands ON products.brand_id = brands.id
    LEFT JOIN stores ON prices.store_id = stores.id
    LEFT JOIN countries ON stores.country_id = countries.id
    LEFT JOIN currencies ON prices.currency_id = currencies.id
    GROUP BY
        products.id,
        products.name,
        products.energy,
        products.fat,
        products.sat_fat,
        products.sodium,
        products.carbs,
        products.fiber,
        products.sugars,
        products.protein,
        products.c_vitamin,
        products.nutr_score_fr,
        products.ingredients_text,
        brands."name",
        prices.price,
        prices.weight,
        prices."date",
        stores."name",
        countries.country,
        currencies.currency_code
    ORDER BY protein_score DESC NULLS LAST
    LIMIT %s OFFSET %s
        """
    return query


def get_c_vitamin_score():
    # To look for the highest C Vitamin Score cost-effective products
    query = """
    SELECT
        products.id,
        products.name,
        products.energy,
        products.fat,
        products.sat_fat,
        products.sodium,
        products.carbs,
        products.fiber,
        products.sugars,
        products.protein,
        products.c_vitamin,
        products.nutr_score_fr,
        products.ingredients_text,
        brands."name" AS brand_name,
        prices.price * 0.01 AS price,
        prices.weight,
        ROUND((prices.price * 0.01) / (prices.weight * 0.001), 2) AS price_per_kg,
        prices."date" AS price_date,
        stores."name" AS store_name,
        countries.country,
        currencies.currency_code,
        CAST((products.c_vitamin / GREATEST(SUM(prices.weight * prices.price), 0.01))
        / GREATEST(products.sodium, 0.001) * 1000000000 AS INT) AS c_vitamin_score
    FROM products
    LEFT JOIN prices ON prices.product_id = products.id
    LEFT JOIN brands ON products.brand_id = brands.id
    LEFT JOIN stores ON prices.store_id = stores.id
    LEFT JOIN countries ON stores.country_id = countries.id
    LEFT JOIN currencies ON prices.currency_id = currencies.id
    GROUP BY
        products.id,
        products.name,
        products.energy,
        products.fat,
        products.sat_fat,
        products.sodium,
        products.carbs,
        products.fiber,
        products.sugars,
        products.protein,
        products.c_vitamin,
        products.nutr_score_fr,
        products.ingredients_text,
        brands."name",
        prices.price,
        prices.weight,
        prices."date",
        stores."name",
        countries.country,
        currencies.currency_code
    ORDER BY c_vitamin_score DESC NULLS LAST
    LIMIT %s OFFSET %s;
        """
    return query

def _get_api_products(cur, keyword, sort_by=None):
    """
    Fetches products based on keyword, with optional dynamic sorting (for AJAX).
    
    NOTE: This uses simplified SQL for quick completion. For production, you 
    would need to copy the full price/brand joins from your score queries 
    and adjust the complex ORDER BY using a CASE statement or CTEs.
    """
    limit = 100 # Keep the limit for API search
    
    # Base query (must match the columns your renderProducts expects)
    base_query = """
        SELECT
            p.id, p.name, p.energy, p.fat, p.sat_fat, p.sodium,
            p.carbs, p.fiber, p.sugars, p.protein, p.c_vitamin,
            p.nutr_score_fr, p.ingredients_text,
            b.name as brand_name,
            pr.price, pr.weight, pr.date as price_date,
            s.name as store_name,
            curr.currency_code
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN LATERAL (
            SELECT price, weight, date, store_id, currency_id
            FROM prices
            WHERE product_id = p.id
            ORDER BY date DESC
            LIMIT 1
        ) pr ON true
        LEFT JOIN stores s ON pr.store_id = s.id
        LEFT JOIN currencies curr ON pr.currency_id = curr.id
        WHERE (p.name ILIKE %s OR b.name ILIKE %s OR s.name ILIKE %s)
    """
    
    params = [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
    
    # Dynamic ORDER BY Logic
    if sort_by == 'protein_value':
        # NOTE: Using raw protein for simplicity. For complex score, you must 
        # add the full score calculation here or use a CTE.
        order_clause = "ORDER BY p.protein DESC NULLS LAST"
    elif sort_by == 'vitamin_c_value':
        order_clause = "ORDER BY p.c_vitamin DESC NULLS LAST"
    else:
        # Default API search sort (can be simple name match or the default protein)
        order_clause = "ORDER BY p.protein DESC NULLS LAST"

    final_query = f"{base_query} {order_clause} LIMIT %s"
    params.append(limit)

    cur.execute(final_query, params)
    return cur.fetchall()

def _process_products(products):
    """Process products: add nutri-score letter/color"""
    processed = []
    for product_row in products:
        product = dict(product_row)
        letter, color = _assign_nutriscore_data(product['nutr_score_fr'])
        product['nutri_letter'] = letter
        product['nutri_color'] = color
        processed.append(product)
    return processed

@main_bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page
    
    sort_by = request.args.get('sort')
    products = []
    
    simple_sort_column = 'protein'
    
    if sort_by == 'protein_value':
        sql_query = get_protein_score()
        cur.execute(sql_query, (per_page, offset))
        products = cur.fetchall()
    elif sort_by == 'vitamin_c_value':
        sql_query = get_c_vitamin_score()
        cur.execute(sql_query, (per_page, offset))
        products = cur.fetchall()
    else:
        products = _get_products(cur, per_page, offset, sort_column=simple_sort_column)
        
    processed_products = _process_products(products)
    
    cur.execute("SELECT COUNT(*) as count FROM products")
    total_products = cur.fetchone()['count']
    total_pages = (total_products + per_page - 1) // per_page
        
    return render_template('main/index.html',
                            products=processed_products,
                            page=page,
                            total_pages=total_pages,
                            max=max,
                            min=min)

                        
@main_bp.route('/api/search')
def api_search():
    """API endpoint for dynamic search - returns JSON"""
    db = get_db()
    cur = db.cursor()
    
    keyword = request.args.get('keyword', '').strip()
    # 1. Read the sort parameter from the request
    sort_by = request.args.get('sort') 
    
    if not keyword:
        # If there's no keyword, don't execute a search
        return jsonify({'products': [], 'count': 0})
    
    # Pass the sort_by parameter to a new helper function
    products = _get_api_products(cur, keyword, sort_by) # New function call
    processed_products = _process_products(products)
    
    return jsonify({
        'products': processed_products,
        'count': len(processed_products)
    })
    
