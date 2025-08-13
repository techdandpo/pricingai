import streamlit as st
import pandas as pd

# Required columns for catalog sheet
KEY_COLUMNS = [
    'Category',
    'Dandpo SKU',
    'Combinations',
    'Printer Specifications',
    'Quantity',
    'Sample',
    'Lead Time',
    'Weight in kg'
]

def catalog_sheet_builder():
    """Main function for Catalog Sheet Builder tab"""
    
    catalog_upload = st.file_uploader("Upload Bidding Sheet CSV", type=["csv"], key="catalog_uploader")
    
    # Simple sample file download
    sample_bidding_data = {
        'Category': ['T-Shirts', 'Hoodies', 'Caps'],
        'Dandpo SKU': ['TS001', 'HD001', 'CP001'],
        'Combinations': ['Red, L', 'Blue, M', 'Black, One Size'],
        'Printer Specifications': ['DTG Print', 'Screen Print', 'Embroidery'],
        'Quantity': [100, 75, 50],
        'Sample': ['Yes', 'No', 'Yes'],
        'Lead Time': [7, 10, 5],
        'Weight in kg': [0.2, 0.4, 0.1],
        'Bid Selected Partners': ['Pname1', 'Pname1', 'Pname1'],
        'Bid Selected Price': [550, 618, 275],
        'Customer Price (35%)': [743, 834, 371],
        'Bid Selected Unit Price': [5.50, 8.24, 5.50],
        'Customer Unit Price': [7.43, 11.12, 7.42],
        'Pname1': [550, 618, 275],
        'Pname2': [575, 650, 290]
    }
    sample_bidding_df = pd.DataFrame(sample_bidding_data)
    sample_bidding_csv = sample_bidding_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download sample file",
        sample_bidding_csv,
        file_name="Bidding_Sheet_Sample.csv",
        mime="text/csv"
    )
    
    if catalog_upload:
        bidding_df = pd.read_csv(catalog_upload)
        # Clean empty rows and NaN values
        bidding_df = bidding_df.dropna(how='all')  # Remove completely empty rows
        bidding_df = bidding_df.fillna('')  # Replace NaN with empty string
        
        # Convert numeric columns to proper data types
        numeric_columns = ['Quantity', 'Bid Selected Price', 'Lead Time', 'Weight in kg', 'Bid Selected Unit Price', 'Customer Unit Price']
        for col in numeric_columns:
            if col in bidding_df.columns:
                bidding_df[col] = pd.to_numeric(bidding_df[col], errors='coerce').fillna(0)
        
        # Convert customer price columns to numeric
        customer_price_cols = [col for col in bidding_df.columns if 'Customer Price' in col]
        for col in customer_price_cols:
            if col in bidding_df.columns:
                bidding_df[col] = pd.to_numeric(bidding_df[col], errors='coerce').fillna(0)
        
        # Initialize session state for tracking applied percentage
        if 'catalog_applied_percentage' not in st.session_state:
            st.session_state.catalog_applied_percentage = 0.0
            
        # Percentage adjustment for Catalog Sheet
        catalog_markup_percentage = st.number_input(
            "Recalculate Customer Price Markup (%)",
            min_value=0.0,
            max_value=200.0,
            value=st.session_state.catalog_applied_percentage,
            step=0.1,
            help="Enter the percentage markup to recalculate customer prices from printer costs (press Enter to apply)",
            key="catalog_markup"
        )
        
        # Update applied percentage when input changes
        if 'catalog_previous_value' not in st.session_state:
            st.session_state.catalog_previous_value = st.session_state.catalog_applied_percentage
            
        # Check if value changed or if user pressed Enter (same value but different from previous)
        if (catalog_markup_percentage != st.session_state.catalog_applied_percentage or 
            (catalog_markup_percentage == st.session_state.catalog_applied_percentage and 
             catalog_markup_percentage != st.session_state.catalog_previous_value)):
            st.session_state.catalog_applied_percentage = catalog_markup_percentage
            
        st.session_state.catalog_previous_value = catalog_markup_percentage
        
        catalog_cols = [
            'Category', 'Dandpo SKU', 'Combinations', 'Printer Specifications',
            'Quantity', 'Sample', 'Lead Time', 'Weight in kg', 'Printer Cost',
            'Customer Price', 'Unit Price for Printer cost', 'Unit Price for customer cost',
            'Partners', 'Production Type', 'Production Time (Hours)',
            'Printer Delivery to Dandpo (Hours)', 'Packaging Dimensions', 'Product Dimensions'
        ]

        catalog_df = pd.DataFrame()
        catalog_df['Category'] = bidding_df['Category']
        catalog_df['Dandpo SKU'] = bidding_df['Dandpo SKU']
        catalog_df['Combinations'] = bidding_df['Combinations']
        catalog_df['Printer Specifications'] = bidding_df['Printer Specifications']
        catalog_df['Quantity'] = bidding_df['Quantity']
        catalog_df['Sample'] = bidding_df['Sample']
        catalog_df['Lead Time'] = bidding_df['Lead Time']
        catalog_df['Weight in kg'] = bidding_df['Weight in kg']
        catalog_df['Printer Cost'] = bidding_df['Bid Selected Price']

        quantity = bidding_df['Quantity'].replace(0, pd.NA).astype(float)
        printer_cost = bidding_df['Bid Selected Price'].astype(float)

        # Initially copy customer price from bidding sheet
        customer_price_cols = [col for col in bidding_df.columns if 'Customer Price' in col]
        if customer_price_cols:
            # Copy the exact column name and values from bidding sheet
            customer_price_col = customer_price_cols[0]
            catalog_df[customer_price_col] = bidding_df[customer_price_col]
        else:
            # Fallback if no customer price column exists
            catalog_df['Customer Price'] = printer_cost
        catalog_df['Unit Price for Printer cost'] = bidding_df.get('Bid Selected Unit Price', printer_cost / quantity).round(2)
        # Calculate unit price for customer cost using the correct customer price column
        customer_price_cols = [col for col in bidding_df.columns if 'Customer Price' in col]
        if customer_price_cols:
            customer_price_col = customer_price_cols[0]
            catalog_df['Unit Price for customer cost'] = bidding_df.get('Customer Unit Price', catalog_df[customer_price_col] / quantity).round(2)
        else:
            # Use the fallback customer price column we created
            catalog_df['Unit Price for customer cost'] = bidding_df.get('Customer Unit Price', catalog_df['Customer Price'] / quantity).round(2)

        # Recalculate customer prices if percentage is not 0
        if st.session_state.catalog_applied_percentage > 0:
            # Find the existing customer price column and replace its values
            customer_price_cols = [col for col in catalog_df.columns if 'Customer Price' in col]
            if customer_price_cols:
                existing_col = customer_price_cols[0]
                # Replace the existing column with new values
                new_customer_price = round(printer_cost * (1 + st.session_state.catalog_applied_percentage/100)).round().astype('Int64')
                catalog_df[existing_col] = new_customer_price
                # Rename the column to show the new percentage
                catalog_df = catalog_df.rename(columns={existing_col: f'Customer Price ({st.session_state.catalog_applied_percentage}%)'})
                # Update unit price for customer cost
                catalog_df['Unit Price for customer cost'] = (new_customer_price / quantity).round(2)
            else:
                # Create new column if none exists
                new_customer_price = round(printer_cost * (1 + st.session_state.catalog_applied_percentage/100)).round().astype('Int64')
                catalog_df[f'Customer Price ({st.session_state.catalog_applied_percentage}%)'] = new_customer_price
                # Update unit price for customer cost
                catalog_df['Unit Price for customer cost'] = (new_customer_price / quantity).round(2)

        # Exclude customer price columns from partners calculation
        customer_price_cols = [col for col in bidding_df.columns if 'Customer Price' in col]
        partner_cols = [col for col in bidding_df.columns if col not in catalog_cols and col not in KEY_COLUMNS and col not in [
            'Bid Selected Partners', 'Bid Selected Price', 'Bid Selected Unit Price', 'Customer Unit Price'] + customer_price_cols]
        catalog_df['Partners'] = bidding_df[partner_cols].apply(lambda row: ', '.join(row.dropna().index), axis=1)

        # Add missing columns from catalog_cols, but skip Customer Price if we already have a customer price column
        customer_price_exists = any('Customer Price' in col for col in catalog_df.columns)
        for col in catalog_cols:
            if col not in catalog_df.columns:
                if col == 'Customer Price' and customer_price_exists:
                    continue  # Skip adding 'Customer Price' if we already have a customer price column
                catalog_df[col] = ""

        st.subheader("📘 Catalog Sheet Preview")
        st.dataframe(catalog_df, use_container_width=True)

        catalog_csv = catalog_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Catalog Sheet (CSV)",
            catalog_csv,
            file_name="Catalog Sheet.csv",
            mime="text/csv"
        )
