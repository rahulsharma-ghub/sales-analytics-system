# utils/data_processor.py

# ==========================================
# Task 2.1: Sales Summary Calculator
# ==========================================

def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    total_revenue = 0.0
    for t in transactions:
        total_revenue += (t['Quantity'] * t['UnitPrice'])
    return round(total_revenue, 2)

def region_wise_sales(transactions):
    """Analyzes sales by region with percentages."""
    region_stats = {}
    grand_total = calculate_total_revenue(transactions)
    
    # 1. Aggregate data
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
            
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
        
    # 2. Calculate percentages and format
    # Note: We can't sort a dictionary in place, so we'll return a sorted dictionary
    # However, standard dicts preserve insertion order in modern Python.
    
    # Convert to list to sort
    sorted_regions = sorted(
        region_stats.items(), 
        key=lambda item: item[1]['total_sales'], 
        reverse=True
    )
    
    final_stats = {}
    for region, stats in sorted_regions:
        stats['percentage'] = round((stats['total_sales'] / grand_total * 100), 2)
        stats['total_sales'] = round(stats['total_sales'], 2)
        final_stats[region] = stats
        
    return final_stats

def top_selling_products(transactions, n=5):
    """Finds top n products by total quantity sold."""
    product_stats = {}
    
    # Aggregate
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if name not in product_stats:
            product_stats[name] = {'qty': 0, 'revenue': 0.0}
            
        product_stats[name]['qty'] += qty
        product_stats[name]['revenue'] += revenue
        
    # Convert to list of tuples
    product_list = []
    for name, stats in product_stats.items():
        product_list.append((name, stats['qty'], round(stats['revenue'], 2)))
        
    # Sort by Quantity (index 1) descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]

def customer_analysis(transactions):
    """Analyzes customer purchase patterns."""
    cust_stats = {}
    
    for t in transactions:
        c_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']
        
        if c_id not in cust_stats:
            cust_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_set': set() # Use set for uniqueness
            }
            
        cust_stats[c_id]['total_spent'] += amount
        cust_stats[c_id]['purchase_count'] += 1
        cust_stats[c_id]['products_set'].add(product)
        
    # Final formatting
    final_stats = {}
    
    # Sort customers by total_spent descending
    sorted_customers = sorted(
        cust_stats.items(),
        key=lambda item: item[1]['total_spent'],
        reverse=True
    )
    
    for c_id, stats in sorted_customers:
        final_stats[c_id] = {
            'total_spent': round(stats['total_spent'], 2),
            'purchase_count': stats['purchase_count'],
            'avg_order_value': round(stats['total_spent'] / stats['purchase_count'], 2),
            'products_bought': list(stats['products_set']) # Convert set back to list
        }
        
    return final_stats

# ==========================================
# Task 2.2: Date-based Analysis
# ==========================================

def daily_sales_trend(transactions):
    """Analyzes sales trends by date."""
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        c_id = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers_set': set()
            }
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers_set'].add(c_id)
        
    # Sort by Date (strings "YYYY-MM-DD" sort correctly alphabetically)
    sorted_dates = sorted(daily_stats.keys())
    
    final_daily = {}
    for date in sorted_dates:
        stats = daily_stats[date]
        final_daily[date] = {
            'revenue': round(stats['revenue'], 2),
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers_set'])
        }
        
    return final_daily

def find_peak_sales_day(transactions):
    """Identifies the date with highest revenue."""
    daily_data = daily_sales_trend(transactions)
    
    best_date = None
    max_rev = -1.0
    count = 0
    
    for date, stats in daily_data.items():
        if stats['revenue'] > max_rev:
            max_rev = stats['revenue']
            best_date = date
            count = stats['transaction_count']
            
    return (best_date, max_rev, count)

# ==========================================
# Task 2.3: Product Performance
# ==========================================

def low_performing_products(transactions, threshold=10):
    """Identifies products with total quantity < threshold."""
    # We can reuse our logic from top_selling_products to get the totals first
    # but we need all products, not just top N
    
    product_stats = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if name not in product_stats:
            product_stats[name] = {'qty': 0, 'revenue': 0.0}
        
        product_stats[name]['qty'] += qty
        product_stats[name]['revenue'] += revenue
        
    # Filter and Format
    low_performers = []
    for name, stats in product_stats.items():
        if stats['qty'] < threshold:
            low_performers.append((name, stats['qty'], round(stats['revenue'], 2)))
            
    # Sort by Quantity ascending (lowest first)
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers