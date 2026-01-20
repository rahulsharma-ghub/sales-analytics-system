import os

# ==========================================
# Task 1.1: Read Sales Data with Encoding Handling
# ==========================================
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings).
    """
    raw_lines = []
    
    # List of encodings to try in order
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                # Read all lines
                lines = file.readlines()
                
                # Skip header if it exists and list is not empty
                if lines:
                    lines = lines[1:]
                
                # Clean up lines (remove whitespace/newlines) and skip empty ones
                for line in lines:
                    cleaned_line = line.strip()
                    if cleaned_line:
                        raw_lines.append(cleaned_line)
                
                # If we succeeded, stop trying other encodings
                print(f"Successfully read file using {encoding} encoding.")
                return raw_lines
                
        except UnicodeDecodeError:
            # If this encoding fails, continue to the next one
            continue
            
    print("Error: Failed to read file with supported encodings.")
    return []

# ==========================================
# Task 1.2: Parse and Clean Data
# ==========================================
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """
    parsed_data = []
    
    for line in raw_lines:
        parts = line.split('|')
        
        # Skip rows with incorrect number of fields (expecting 8)
        if len(parts) != 8:
            continue
            
        # Unpack and Clean fields
        try:
            # Handle commas in numeric fields (e.g., "1,500" -> "1500")
            qty_str = parts[4].replace(',', '').strip()
            price_str = parts[5].replace(',', '').strip()
            
            # Convert types
            quantity = int(qty_str)
            unit_price = float(price_str)
            
            # Handle commas in ProductName (replace with space)
            product_name = parts[3].replace(',', ' ').strip()
            
            transaction = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            parsed_data.append(transaction)
            
        except ValueError:
            # Skip if type conversion fails
            continue
            
    return parsed_data

# ==========================================
# Task 1.3: Data Validation and Filtering
# ==========================================
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """
    valid_filtered_transactions = []
    invalid_count = 0
    
    # Summary Dictionary
    summary = {
        'total_input': len(transactions),
        'invalid': 0,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }
    
    # 1. Display available options to user
    available_regions = set(t['Region'] for t in transactions if t.get('Region'))
    print(f"\n--- Filter Options ---")
    print(f"Available Regions: {sorted(list(available_regions))}")
    if min_amount or max_amount:
        print(f"Amount Range: {min_amount if min_amount else 0} to {max_amount if max_amount else 'Infinity'}")

    for t in transactions:
        # --- VALIDATION PHASE ---
        is_valid = True
        
        # Check IDs
        if not t['TransactionID'].startswith('T'): is_valid = False
        if not t['ProductID'].startswith('P'): is_valid = False
        if not t['CustomerID'].startswith('C'): is_valid = False
        
        # Check Values
        if t['Quantity'] <= 0: is_valid = False
        if t['UnitPrice'] <= 0: is_valid = False
        
        if not is_valid:
            invalid_count += 1
            continue

        # --- FILTER PHASE ---
        
        # Region Filter
        if region and t['Region'] != region:
            summary['filtered_by_region'] += 1
            continue
            
        # Amount Calculation and Filter
        total_amount = t['Quantity'] * t['UnitPrice']
        
        if min_amount is not None and total_amount < min_amount:
            summary['filtered_by_amount'] += 1
            continue
            
        if max_amount is not None and total_amount > max_amount:
            summary['filtered_by_amount'] += 1
            continue
            
        # If it passes all checks, add to final list
        valid_filtered_transactions.append(t)

    # Update Summary stats
    summary['invalid'] = invalid_count
    summary['final_count'] = len(valid_filtered_transactions)
    
    return valid_filtered_transactions, invalid_count, summary