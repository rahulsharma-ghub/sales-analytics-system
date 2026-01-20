import requests
import os

# ==========================================
# Task 3.1: Fetch Product Details
# ==========================================

def fetch_all_products():
    """Fetches all products from DummyJSON API."""
    url = "https://dummyjson.com/products?limit=100"
    print(f"Connecting to API: {url}")
    
    try:
        response = requests.get(url, timeout=10) # 10 second timeout
        
        # Check if request was successful (Status Code 200)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"Success: Fetched {len(products)} products from API.")
            return products
        else:
            print(f"Error: API returned status code {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error: Connection failed. {e}")
        return []

def create_product_mapping(api_products):
    """Creates a mapping of product IDs to product info."""
    mapping = {}
    
    for p in api_products:
        p_id = p['id']
        mapping[p_id] = {
            'title': p.get('title'),
            'category': p.get('category'),
            'brand': p.get('brand'),
            'rating': p.get('rating')
        }
    return mapping

# ==========================================
# Task 3.2: Enrich Sales Data
# ==========================================

def enrich_sales_data(transactions, product_mapping):
    """Enriches transaction data with API product information."""
    enriched_data = []
    
    for t in transactions:
        # Create a copy so we don't mess up original data
        record = t.copy()
        
        # Extract numeric ID from "P101" -> 101
        p_id_str = record['ProductID']
        
        numeric_id = None
        # Try to strip 'P' and convert to int
        if p_id_str.startswith('P') and p_id_str[1:].isdigit():
            numeric_id = int(p_id_str[1:])
        
        # Look up in mapping
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            record['API_Category'] = info['category']
            record['API_Brand'] = info['brand']
            record['API_Rating'] = info['rating']
            record['API_Match'] = True
        else:
            # If product not found in API
            record['API_Category'] = None
            record['API_Brand'] = None
            record['API_Rating'] = None
            record['API_Match'] = False
            
        enriched_data.append(record)
        
    return enriched_data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """Saves enriched transactions back to file."""
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            f.write(header)
            
            for t in enriched_transactions:
                # Handle None values for string formatting
                cat = t['API_Category'] if t['API_Category'] else 'N/A'
                brand = t['API_Brand'] if t['API_Brand'] else 'N/A'
                rating = str(t['API_Rating']) if t['API_Rating'] is not None else '0.0'
                match = str(t['API_Match'])
                
                line = f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|{cat}|{brand}|{rating}|{match}\n"
                f.write(line)
                
        print(f"Successfully saved enriched data to {filename}")
        
    except IOError as e:
        print(f"Error saving file: {e}")