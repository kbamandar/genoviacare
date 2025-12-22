#!/usr/bin/env python3
"""
Excel File Reader and Summarizer
Reads an Excel file and provides a comprehensive summary of its contents.
"""

import pandas as pd
import sys
from pathlib import Path
import io


def safe_print(text):
    """Print text safely handling encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic characters
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)


def summarize_excel(file_path):
    """
    Read and summarize an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
    """
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        safe_print("=" * 80)
        safe_print(f"EXCEL FILE SUMMARY: {Path(file_path).name}")
        safe_print("=" * 80)
        safe_print(f"\nTotal number of sheets: {len(sheet_names)}")
        safe_print(f"Sheet names: {', '.join(sheet_names)}")
        safe_print("\n" + "-" * 80)
        
        # Summarize each sheet
        for idx, sheet_name in enumerate(sheet_names, 1):
            safe_print(f"\n[Sheet {idx}/{len(sheet_names)}] {sheet_name}")
            safe_print("-" * 80)
            
            # Read the sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Basic information
            num_rows, num_cols = df.shape
            safe_print(f"Dimensions: {num_rows} rows x {num_cols} columns")
            
            # Show column information
            if num_cols > 0:
                safe_print(f"\nColumns ({num_cols}):")
                for i, col in enumerate(df.columns, 1):
                    dtype = df[col].dtype
                    non_null = df[col].notna().sum()
                    null_count = df[col].isna().sum()
                    # Clean column name for display
                    col_display = str(col) if not str(col).startswith('Unnamed') else f"Column {i-1}"
                    safe_print(f"  {i}. {col_display} ({dtype}) - {non_null} non-null, {null_count} null")
                
                # Show data types summary
                safe_print(f"\nData types summary:")
                dtype_counts = df.dtypes.value_counts()
                for dtype, count in dtype_counts.items():
                    safe_print(f"  {dtype}: {count} column(s)")
            
            # Show first few rows
            if num_rows > 0:
                safe_print(f"\nFirst 5 rows (preview):")
                # Use buffer to handle encoding
                buffer = io.StringIO()
                df.head().to_string(buf=buffer, max_cols=10, max_colwidth=50)
                safe_print(buffer.getvalue())
                
                # Show summary statistics for numeric columns
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    safe_print(f"\nSummary statistics for numeric columns:")
                    buffer = io.StringIO()
                    df[numeric_cols].describe().to_string(buf=buffer)
                    safe_print(buffer.getvalue())
                
                # Show unique value counts for non-numeric columns (sample)
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns[:10]  # Limit to first 10
                if len(categorical_cols) > 0:
                    safe_print(f"\nUnique value counts for categorical columns (first 10):")
                    for col in categorical_cols:
                        unique_count = df[col].nunique()
                        col_display = str(col) if not str(col).startswith('Unnamed') else f"Column {list(df.columns).index(col)}"
                        safe_print(f"  {col_display}: {unique_count} unique values")
                        if unique_count <= 5:
                            try:
                                unique_vals = [str(v)[:50] for v in df[col].dropna().unique()[:5]]
                                safe_print(f"    Sample values: {', '.join(unique_vals)}")
                            except:
                                pass
            
            # Memory usage
            memory_usage = df.memory_usage(deep=True).sum() / 1024  # KB
            safe_print(f"\nMemory usage: {memory_usage:.2f} KB")
        
        safe_print("\n" + "=" * 80)
        safe_print("SUMMARY COMPLETE")
        safe_print("=" * 80)
        
    except FileNotFoundError:
        safe_print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        safe_print(f"Error reading Excel file: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Default file path
    default_file = "Workflow Team Starting Point Draft.xlsx"
    
    # Check if file path is provided as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = default_file
    
    # Check if file exists
    if not Path(file_path).exists():
        safe_print(f"Error: File '{file_path}' not found.")
        safe_print(f"Usage: python summarize_excel.py [file_path]")
        sys.exit(1)
    
    summarize_excel(file_path)

