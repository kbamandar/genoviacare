#!/usr/bin/env python3
"""
Analyze Categories sheet and rank workflows by cost and improvement opportunity
"""

import pandas as pd
import json
import sys
from pathlib import Path

def safe_str(value):
    """Safely convert value to string handling encoding issues."""
    if pd.isna(value):
        return ""
    try:
        return str(value)
    except:
        return repr(value)

def main():
    file_path = "Workflow Team Starting Point Draft.xlsx"
    
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    # Read Categories sheet
    df = pd.read_excel(file_path, sheet_name='Categories', header=0)
    
    print(f"Categories sheet shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Save raw data to inspect
    categories_data = []
    
    # Check what's in the header row and identify ranking columns
    print("\nFirst row values:")
    for i, col in enumerate(df.columns):
        val = df.iloc[0, i] if len(df) > 0 else None
        val_str = safe_str(val)[:100]
        try:
            print(f"  Column {i} ({col}): {val_str}")
        except:
            print(f"  Column {i} ({col}): [encoding issue]")
    
    # Look for ranking columns in header or row 0
    cost_rank_col = None
    improvement_rank_col = None
    
    # Check column names
    for i, col in enumerate(df.columns):
        col_str = str(col).lower()
        if 'cost' in col_str and 'rank' in col_str:
            cost_rank_col = i
        if 'improvement' in col_str or ('opportunity' in col_str and 'rank' in col_str):
            improvement_rank_col = i
    
    # Check first row for header text
    if len(df) > 0:
        for i in range(len(df.columns)):
            val = safe_str(df.iloc[0, i]).lower()
            if 'cost' in val and ('rank' in val or 'highest' in val):
                cost_rank_col = i
                print(f"Found cost rank column in row 0, column {i}")
            if ('improvement' in val or 'opportunity' in val) and ('rank' in val or 'highest' in val):
                improvement_rank_col = i
                print(f"Found improvement rank column in row 0, column {i}")
    
    print(f"\nCost Rank Column: {cost_rank_col}")
    print(f"Improvement Rank Column: {improvement_rank_col}")
    
    # Process each workflow row
    for idx in range(len(df)):
        row = df.iloc[idx]
        
        # Skip header rows
        workflow_num = row.get('#', None) if '#' in df.columns else None
        category = safe_str(row.get('Category', ''))
        workflow_name = safe_str(row.get('Workflow Name', ''))
        timing = safe_str(row.get('Operational Timing', ''))
        
        # Try to get rankings
        cost_rank = None
        improvement_rank = None
        
        # Check named columns first
        for col in df.columns:
            col_str = str(col).lower()
            val = row.get(col, None)
            if pd.notna(val):
                val_str = safe_str(val)
                # Look for numeric rankings
                if 'cost' in col_str and ('highest' in val_str.lower() or '1=' in val_str.lower()):
                    # This might be a header
                    continue
                elif 'cost' in col_str and val_str.strip().isdigit():
                    cost_rank = int(val_str.strip())
                elif ('improvement' in col_str or 'opportunity' in col_str) and val_str.strip().isdigit():
                    improvement_rank = int(val_str.strip())
        
        # Check unnamed columns if rankings not found
        if cost_rank is None and cost_rank_col is not None:
            val = row.iloc[cost_rank_col] if cost_rank_col < len(row) else None
            if pd.notna(val):
                val_str = safe_str(val)
                if val_str.strip().isdigit():
                    cost_rank = int(val_str.strip())
        
        if improvement_rank is None and improvement_rank_col is not None:
            val = row.iloc[improvement_rank_col] if improvement_rank_col < len(row) else None
            if pd.notna(val):
                val_str = safe_str(val)
                if val_str.strip().isdigit():
                    improvement_rank = int(val_str.strip())
        
        # Only include rows with workflow data
        if pd.notna(workflow_num) or (category and category != 'nan' and len(category) > 3):
            categories_data.append({
                'workflow_num': int(workflow_num) if pd.notna(workflow_num) else None,
                'category': category,
                'workflow_name': workflow_name,
                'operational_timing': timing,
                'cost_rank': cost_rank,
                'improvement_rank': improvement_rank,
                'row_index': idx
            })
    
    # Save to JSON
    with open('categories_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessed {len(categories_data)} workflow entries")
    print("\nSample entries:")
    for entry in categories_data[:5]:
        print(f"  #{entry['workflow_num']}: {entry['workflow_name']}")
        print(f"    Cost Rank: {entry['cost_rank']}, Improvement Rank: {entry['improvement_rank']}")

if __name__ == "__main__":
    main()

