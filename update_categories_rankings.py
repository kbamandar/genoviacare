#!/usr/bin/env python3
"""
Update Categories Sheet with Rankings from Report.md Analysis

This script reads the Excel file and updates the Categories sheet with:
1. Top 10 rankings by Total Labor Cost
2. Top 10 rankings by Magnitude of Improvement Opportunity
"""

import pandas as pd
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter

# Rankings from Report.md Part B.1: Top 10 by Total Labor Cost
LABOR_COST_RANKINGS = {
    18: 1,   # Denials Management & Appeals
    2: 2,    # Prior Authorization (PA) Processing
    4: 3,    # Nursing Coordination & Skilled Visit Scheduling
    27: 4,   # Accreditation Maintenance & Continuous Readiness
    28: 5,   # Clinical Oversight Committee (COC) Operations
    29: 6,   # Quality Management Program (QMP) & Reporting
    9: 7,    # Special Programs & Ancillary Services (REMS)
    19: 8,   # Payment Posting & Reconciliation
    13: 9,   # Inventory Management - Returns & Reverse Distribution
    12: 10,  # Inventory Management - Procurement
}

# Rankings from Report.md Part B.2: Top 10 by Improvement Opportunity
IMPROVEMENT_RANKINGS = {
    18: 1,   # Denials Management & Appeals
    2: 2,    # Prior Authorization (PA) Processing
    1: 3,    # Referral Intake, Enrollment & Benefits Verification
    6: 4,    # Refill Clinical Follow-Up
    10: 5,   # Prescription Processing & Order Entry
    15: 6,   # Patient Receipt & Delivery Confirmation
    5: 7,    # Patient Onboarding & Initial Clinical Assessment
    7: 8,    # Ongoing Clinical Assessment
    16: 9,   # Claims Submission: Pharmacy Benefit
    3: 10,   # Transfer Triage & Payer Lockout Management
}


def find_workflow_number_column(df):
    """Find the column that contains workflow numbers."""
    # Based on the Excel structure, workflow numbers are in the first column
    # Check if first column contains integers 1-30
    first_col = df.columns[0]
    sample_values = df[first_col].dropna().head(10)
    
    # Check if values are workflow numbers (integers 1-30)
    workflow_count = 0
    for val in sample_values:
        try:
            num = int(float(val))
            if 1 <= num <= 30:
                workflow_count += 1
        except (ValueError, TypeError):
            pass
    
    # If at least 5 values look like workflow numbers, use this column
    if workflow_count >= 5:
        return first_col
    
    # Fallback: check other columns
    for col in df.columns:
        col_str = str(col).strip()
        if 'workflow' in col_str.lower() or '#' in col_str.lower():
            return col
    
    return first_col


def find_ranking_columns(df):
    """Find columns for Cost Rank and Improvement Rank."""
    # Based on the Excel structure:
    # Column 4 (index 4) = "FORCE RANK TOP 10\n1=Highest Labor Cost"
    # Column 5 (index 5) = "FORCE RANK TOP 10\n1=Highest Imp Opportunity"
    
    cost_col = None
    improvement_col = None
    
    # Check column names/headers for ranking indicators
    for idx, col in enumerate(df.columns):
        col_str = str(col).strip().lower()
        col_val = str(df.iloc[0, idx] if len(df) > 0 else '').strip().lower()
        
        # Check column name or first row value
        check_str = col_str + ' ' + col_val
        
        if 'labor cost' in check_str or ('cost' in check_str and 'rank' in check_str):
            cost_col = col
        elif 'imp opportunity' in check_str or ('improvement' in check_str and 'rank' in check_str):
            improvement_col = col
    
    # If not found by name, use columns 4 and 5 (indices 4 and 5)
    if cost_col is None and len(df.columns) > 4:
        cost_col = df.columns[4]
    
    if improvement_col is None and len(df.columns) > 5:
        improvement_col = df.columns[5]
    
    return cost_col, improvement_col


def update_categories_sheet(file_path, output_path=None):
    """
    Update the Categories sheet with rankings from Report.md.
    
    Args:
        file_path: Path to the Excel file
        output_path: Optional path for output file (default: overwrites original)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    print(f"Reading Excel file: {file_path}")
    
    # Read the Categories sheet
    try:
        df = pd.read_excel(file_path, sheet_name='Categories')
        print(f"Successfully read Categories sheet: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        raise ValueError(f"Error reading Categories sheet: {e}")
    
    # Find workflow number column
    wf_col = find_workflow_number_column(df)
    print(f"Using workflow number column: '{wf_col}'")
    
    # Find ranking columns
    cost_col, improvement_col = find_ranking_columns(df)
    print(f"Cost Rank column: '{cost_col}'")
    print(f"Improvement Rank column: '{improvement_col}'")
    
    # If columns don't exist, we'll need to create them
    if cost_col is None:
        cost_col = 'Cost Rank (Labor Cost)'
        df[cost_col] = None
        print(f"Created new column: '{cost_col}'")
    
    if improvement_col is None:
        improvement_col = 'Improvement Opportunity Rank'
        df[improvement_col] = None
        print(f"Created new column: '{improvement_col}'")
    
    # Update rankings
    updated_cost = 0
    updated_improvement = 0
    
    for idx, row in df.iterrows():
        # Skip header row (row 0 typically has description text)
        wf_num = row[wf_col]
        
        # Handle different data types
        if pd.isna(wf_num):
            continue
        
        # Skip if it's not a number (e.g., header text)
        try:
            wf_num = int(float(wf_num))
        except (ValueError, TypeError):
            continue
        
        # Only process valid workflow numbers (1-30)
        if not (1 <= wf_num <= 30):
            continue
        
        # Update Cost Rank if workflow is in top 10
        if wf_num in LABOR_COST_RANKINGS:
            df.at[idx, cost_col] = LABOR_COST_RANKINGS[wf_num]
            updated_cost += 1
            wf_name = str(row.get('Workflow Name', f'#{wf_num}'))
            print(f"  Workflow #{wf_num} ({wf_name[:50]}...): Cost Rank = {LABOR_COST_RANKINGS[wf_num]}")
        
        # Update Improvement Rank if workflow is in top 10
        if wf_num in IMPROVEMENT_RANKINGS:
            df.at[idx, improvement_col] = IMPROVEMENT_RANKINGS[wf_num]
            updated_improvement += 1
            wf_name = str(row.get('Workflow Name', f'#{wf_num}'))
            print(f"  Workflow #{wf_num} ({wf_name[:50]}...): Improvement Rank = {IMPROVEMENT_RANKINGS[wf_num]}")
    
    print(f"\nUpdated {updated_cost} Cost Rankings")
    print(f"Updated {updated_improvement} Improvement Rankings")
    
    # Determine output path
    if output_path is None:
        output_path = file_path
    else:
        output_path = Path(output_path)
    
    # Save the updated sheet
    print(f"\nSaving updated file to: {output_path}")
    
    # Use openpyxl to preserve formatting and other sheets
    try:
        # Load the workbook
        wb = openpyxl.load_workbook(file_path)
        
        # Remove existing Categories sheet if it exists
        if 'Categories' in wb.sheetnames:
            wb.remove(wb['Categories'])
        
        # Create new Categories sheet
        ws = wb.create_sheet('Categories', index=1)  # Insert at position 1
        
        # Write header row
        for col_idx, col_name in enumerate(df.columns, 1):
            cell = ws.cell(row=1, column=col_idx, value=col_name)
            cell.font = openpyxl.styles.Font(bold=True)
        
        # Write data rows
        for row_idx, (_, row_data) in enumerate(df.iterrows(), 2):
            for col_idx, value in enumerate(row_data, 1):
                ws.cell(row=row_idx, column=col_idx, value=value)
        
        # Auto-adjust column widths
        for col_idx, col_name in enumerate(df.columns, 1):
            max_length = max(
                len(str(col_name)),
                df[col_name].astype(str).str.len().max() if df[col_name].notna().any() else 0
            )
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max_length + 2, 50)
        
        # Save workbook
        wb.save(output_path)
        print("[SUCCESS] Successfully saved updated Excel file")
        
    except Exception as e:
        # Fallback to pandas if openpyxl fails
        print(f"Warning: Could not use openpyxl ({e}), using pandas fallback")
        try:
            # Try to update existing file
            with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Categories', index=False)
            print("[SUCCESS] Successfully saved updated Excel file (pandas fallback)")
        except Exception as e2:
            # Last resort: create new file
            print(f"Warning: Could not update in place ({e2}), creating new file")
            new_path = str(output_path).replace('.xlsx', '_updated.xlsx')
            with pd.ExcelWriter(new_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Categories', index=False)
            print(f"[SUCCESS] Saved to new file: {new_path}")
    
    return df, cost_col, improvement_col


def main():
    """Main function."""
    import sys
    
    # File path
    file_path = "Workflow Team Starting Point Draft - Mandar.xlsx"
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found.")
        print("Please ensure the file exists in the current directory.")
        sys.exit(1)
    
    # Optional: create backup
    backup_path = file_path.replace('.xlsx', '_backup.xlsx')
    if Path(file_path).exists():
        import shutil
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}\n")
    
    try:
        # Update the Categories sheet
        df, cost_col, improvement_col = update_categories_sheet(file_path)
        
        print("\n" + "="*80)
        print("UPDATE COMPLETE")
        print("="*80)
        print(f"\nSummary:")
        print(f"  - Total workflows in Categories sheet: {len(df)}")
        
        # Count updated rankings
        cost_count = sum(df[cost_col].notna()) if cost_col and cost_col in df.columns else 0
        improvement_count = sum(df[improvement_col].notna()) if improvement_col and improvement_col in df.columns else 0
        
        print(f"  - Cost Rankings updated: {cost_count}")
        print(f"  - Improvement Rankings updated: {improvement_count}")
        print(f"\nFile saved: {file_path}")
        if Path(backup_path).exists():
            print(f"Backup saved: {backup_path}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

