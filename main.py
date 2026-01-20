#!/usr/bin/env python3
import sys
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import calculate_total_revenue
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report

def main():
    print("=" * 40)
    print(f"{'SALES ANALYTICS SYSTEM':^40}")
    print("=" * 40 + "\n")

    try:
        # [1/10] Reading sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data('sales_data.txt')
        print(f"✓ Successfully read {len(raw_data)} transactions\n")

        # [2/10] Parsing and cleaning data
        print("[2/10] Parsing and cleaning data...")
        parsed_data = parse_transactions(raw_data)
        print(f"✓ Parsed {len(parsed_data)} records\n")

        # [3/10] Filter Options Available
        print("[3/10] Filter Options Available:")
        
        # Calculate available options dynamically
        regions = sorted(list(set(t['Region'] for t in parsed_data if t.get('Region'))))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed_data]
        min_amt = min(amounts) if amounts else 0
        max_amt = max(amounts) if amounts else 0
        
        print(f"   Regions: {', '.join(regions)}")
        print(f"   Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}\n")

        # User Interaction
        user_filter = input("   Do you want to filter data? (y/n): ").strip().lower()
        
        selected_region = None
        min_val = None
        max_val = None

        if user_filter == 'y':
            print("   --- Enter Filter Criteria (Press Enter to skip) ---")
            
            # Ask for Region
            reg_input = input(f"   Enter Region ({', '.join(regions)}): ").strip()
            if reg_input in regions:
                selected_region = reg_input
            
            # Ask for Min Amount
            min_input = input("   Enter Minimum Amount: ").strip()
            if min_input:
                try:
                    min_val = float(min_input)
                except ValueError:
                    print("   ! Invalid number, ignoring minimum filter.")

            # Ask for Max Amount
            max_input = input("   Enter Maximum Amount: ").strip()
            if max_input:
                try:
                    max_val = float(max_input)
                except ValueError:
                    print("   ! Invalid number, ignoring maximum filter.")
            print("")

        # [4/10] Validating transactions
        print("[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(
            parsed_data, 
            region=selected_region, 
            min_amount=min_val, 
            max_amount=max_val
        )
        print(f"✓ Valid: {len(valid_data)} | Invalid/Filtered Out: {len(parsed_data) - len(valid_data)}\n")

        if not valid_data:
            print("Error: No valid data found after filtering. Exiting.")
            sys.exit()

        # [5/10] Analyzing sales data
        print("[5/10] Analyzing sales data...")
        # (The actual deep analysis happens inside the report generator, 
        # but we can do a quick check here to simulate the step)
        total_rev = calculate_total_revenue(valid_data)
        print(f"✓ Analysis complete (Current Revenue: ₹{total_rev:,.2f})\n")

        # [6/10] Fetching product data from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if api_products:
            print(f"✓ Fetched {len(api_products)} products\n")
        else:
            print("! Warning: API fetch failed. Proceeding without enrichment.\n")

        # [7/10] Enriching sales data
        print("[7/10] Enriching sales data...")
        mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(valid_data, mapping)
        
        match_count = sum(1 for t in enriched_data if t.get('API_Match'))
        match_pct = (match_count / len(enriched_data) * 100) if enriched_data else 0
        print(f"✓ Enriched {match_count}/{len(enriched_data)} transactions ({match_pct:.1f}%)\n")

        # [8/10] Saving enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_data, 'data/enriched_sales_data.txt')
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # [9/10] Generating report
        print("[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data, 'output/sales_report.txt')
        print("✓ Report saved to: output/sales_report.txt\n")

        # [10/10] Process Complete
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n!!! CRITICAL SYSTEM ERROR !!!")
        print(f"An unexpected error occurred: {e}")
        print("Please check your data files and try again.")
        print("=" * 40)

if __name__ == "__main__":

    main()
