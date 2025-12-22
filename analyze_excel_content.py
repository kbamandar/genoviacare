#!/usr/bin/env python3
"""
Excel Content Analyzer
Reads an Excel file and provides content analysis, ranking information, and correlations.
"""

import pandas as pd
import sys
from pathlib import Path
import io
import re
from collections import Counter


def safe_print(text):
    """Print text safely handling encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)


def extract_column_name(df, idx):
    """Try to extract meaningful column names from the data."""
    # Check if first row contains headers
    first_row = df.iloc[0] if len(df) > 0 else None
    col_name = str(df.columns[idx])
    
    if first_row is not None and str(first_row.iloc[idx]) != 'nan':
        potential_name = str(first_row.iloc[idx])
        if len(potential_name) < 100 and not potential_name.startswith('Unnamed'):
            return potential_name
    return col_name


def analyze_workflows_sheet(df, file_path):
    """Analyze the Workflows sheet in detail."""
    safe_print("\n" + "=" * 100)
    safe_print("CONTENT ANALYSIS: WORKFLOWS SHEET")
    safe_print("=" * 100)
    
    # Read raw - row 0 has headers, row 1 has sub-headers, row 2+ has data
    raw_df = pd.read_excel(file_path, sheet_name="Workflows", header=None)
    
    # Extract column names from row 0 (main headers)
    header_row = raw_df.iloc[0]
    new_col_names = []
    for i, val in enumerate(header_row):
        if pd.notna(val) and str(val).strip():
            new_col_names.append(str(val).strip())
        else:
            # Try row 1 (sub-headers) if row 0 is empty
            if i < len(raw_df.columns) and pd.notna(raw_df.iloc[1, i]):
                new_col_names.append(str(raw_df.iloc[1, i]).strip())
            else:
                new_col_names.append(f"Column_{i}")
    
    # Create clean dataframe: use row 0 as headers, skip row 1 (sub-headers), data starts from row 2
    df_clean = pd.read_excel(file_path, sheet_name="Workflows", header=0)
    df_clean.columns = new_col_names[:len(df_clean.columns)]
    
    # Skip the sub-header row if it's still in the data
    # Check if first row looks like a sub-header (usually has many non-null values but is descriptive text)
    if len(df_clean) > 0:
        first_row_non_null = df_clean.iloc[0].notna().sum()
        # If first row has many non-null values but contains text that looks like headers, drop it
        if first_row_non_null > 5:
            first_val = str(df_clean.iloc[0, 0]) if len(df_clean.columns) > 0 else ""
            # If first row starts with "#" or looks like a header row, keep it; otherwise might be sub-header
            if not first_val.strip().startswith('#') and len(first_val) > 50:
                df_clean = df_clean.iloc[1:].reset_index(drop=True)
    
    safe_print(f"\nDetected {len(df_clean)} workflow entries")
    
    # Try to identify key columns by content analysis
    column_mapping = {}
    for col in df_clean.columns:
        col_str = str(col).lower()
        
        # Identify efficiency ranking column (typically contains 1-5)
        if 'efficien' in col_str or 'improvement' in col_str or 'opportunity' in col_str:
            if 'efficiency_rank' not in column_mapping:  # Take first match
                column_mapping['efficiency_rank'] = col
        # Identify category column
        elif 'categor' in col_str and col_str != 'column_1':
            if 'category' not in column_mapping:
                column_mapping['category'] = col
        # Identify workflow name/process
        elif ('workflow' in col_str and 'process' in col_str) or (col_str == 'workflow process'):
            if 'workflow_name' not in column_mapping:
                column_mapping['workflow_name'] = col
        # Identify hours
        elif 'hour' in col_str:
            if 'hours' not in column_mapping:
                column_mapping['hours'] = col
        # Identify roles
        elif 'role' in col_str and 'performs' in col_str:
            if 'roles' not in column_mapping:
                column_mapping['roles'] = col
        # Identify subsector columns
        elif 'subsector' in col_str or 'infusion' in col_str.lower() or 'specialty' in col_str.lower():
            if 'home infusion' in col_str or 'clean room' in col_str:
                if 'subsector_home' not in column_mapping:
                    column_mapping['subsector_home'] = col
            elif 'specialty infusion' in col_str or 'ambulatory' in col_str:
                if 'subsector_specialty' not in column_mapping:
                    column_mapping['subsector_specialty'] = col
            elif 'light specialty' in col_str:
                if 'subsector_light' not in column_mapping:
                    column_mapping['subsector_light'] = col
            elif 'subsector details' in col_str or 'subsector' in col_str:
                if 'subsector_details' not in column_mapping:
                    column_mapping['subsector_details'] = col
    
    safe_print("\nIdentified Key Columns:")
    for key, col in column_mapping.items():
        safe_print(f"  {key}: {col}")
    
    # Analyze efficiency rankings
    if 'efficiency_rank' in column_mapping:
        rank_col = column_mapping['efficiency_rank']
        safe_print(f"\n{'='*100}")
        safe_print("EFFICIENCY IMPROVEMENT OPPORTUNITY RANKINGS")
        safe_print(f"{'='*100}")
        
        # Extract numeric rankings
        rankings = []
        rank_data = []
        for idx, val in enumerate(df_clean[rank_col]):
            if pd.notna(val):
                # Try to extract number from value
                val_str = str(val)
                # Look for standalone numbers 1-5 (not part of other numbers)
                nums = re.findall(r'\b([1-5])\b(?!\d)', val_str)
                if nums:
                    rank_num = int(nums[0])
                    rankings.append(rank_num)
                    rank_data.append((idx, rank_num, val_str[:100]))
        
        if rankings:
            rank_counts = Counter(rankings)
            safe_print(f"\nRanking Distribution (1=Lowest, 5=Highest Opportunity):")
            for rank in sorted(rank_counts.keys(), reverse=True):
                count = rank_counts[rank]
                safe_print(f"  Rank {rank}: {count} workflow(s)")
            
            # Show top-ranked workflows
            safe_print(f"\nTop Priority Workflows (Rank 5 - Highest Improvement Opportunity):")
            rank_5_items = [(idx, val_str) for idx, rank, val_str in rank_data if rank == 5]
            
            # Get category and workflow name for top-ranked items
            if 'category' in column_mapping and 'workflow_name' in column_mapping:
                cat_col = column_mapping['category']
                wf_col = column_mapping['workflow_name']
                count = 0
                for idx, _ in rank_5_items:
                    try:
                        # Get category - prefer short names
                        cat = ""
                        if cat_col in df_clean.columns:
                            cat_val = df_clean.iloc[idx][cat_col]
                            if pd.notna(cat_val):
                                cat = str(cat_val).strip()
                                # If category is too long, it's probably a description, skip this row
                                if len(cat) > 80:
                                    continue
                        
                        # Get workflow name
                        wf = ""
                        if wf_col in df_clean.columns:
                            wf_val = df_clean.iloc[idx][wf_col]
                            if pd.notna(wf_val):
                                wf = str(wf_val).strip()
                        
                        if cat or wf:
                            safe_print(f"  {count + 1}. Category: {cat if cat else 'N/A'}")
                            if wf:
                                wf_display = wf[:100] + "..." if len(wf) > 100 else wf
                                safe_print(f"     Workflow: {wf_display}")
                            count += 1
                            if count >= 10:  # Limit to 10
                                break
                    except Exception as e:
                        pass
    
    # Analyze categories - look for the actual category column
    # Category seems to be in column 1 based on structure
    cat_col = None
    for col in df_clean.columns:
        col_str = str(col).lower()
        if col_str == 'category':
            cat_col = col
            break
    
    if cat_col and cat_col in df_clean.columns:
        safe_print(f"\n{'='*100}")
        safe_print("WORKFLOW CATEGORIES")
        safe_print(f"{'='*100}")
        
        # Get unique categories, filtering out long descriptions
        category_counts = {}
        for val in df_clean[cat_col].dropna():
            val_str = str(val).strip()
            # Skip very long text (likely descriptions, not category names)
            if len(val_str) < 100:
                category_counts[val_str] = category_counts.get(val_str, 0) + 1
        
        safe_print(f"\nFound {len(category_counts)} distinct categories:")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            safe_print(f"  - {cat}: {count} workflow(s)")
    
    # Analyze hours/workload
    if 'hours' in column_mapping:
        hours_col = column_mapping['hours']
        safe_print(f"\n{'='*100}")
        safe_print("WORKLOAD ANALYSIS (Hours Required)")
        safe_print(f"{'='*100}")
        
        # Extract hours from text
        hours_values = []
        for val in df_clean[hours_col].dropna():
            val_str = str(val)
            # Look for patterns like "X Hours" or "X.X Hours"
            hour_match = re.search(r'(\d+\.?\d*)\s*(?:hours?|hrs?)', val_str, re.IGNORECASE)
            if hour_match:
                hours_values.append(float(hour_match.group(1)))
        
        if hours_values:
            safe_print(f"\nHours Distribution (from {len(hours_values)} entries with hour data):")
            safe_print(f"  Average: {sum(hours_values)/len(hours_values):.2f} hours")
            safe_print(f"  Min: {min(hours_values):.2f} hours")
            safe_print(f"  Max: {max(hours_values):.2f} hours")
    
    # Analyze subsector presence
    subsector_cols = [k for k in column_mapping.keys() if k.startswith('subsector_')]
    if subsector_cols:
        safe_print(f"\n{'='*100}")
        safe_print("SUBSECTOR ANALYSIS")
        safe_print(f"{'='*100}")
        
        for sub_col_key in subsector_cols:
            sub_col = column_mapping[sub_col_key]
            if sub_col in df_clean.columns:
                present_count = df_clean[sub_col].notna().sum()
                y_count = (df_clean[sub_col].astype(str).str.upper() == 'Y').sum()
                safe_print(f"\n{sub_col}:")
                safe_print(f"  Total entries: {present_count}")
                safe_print(f"  Marked 'Y': {y_count}")
    
    # Correlation analysis
    safe_print(f"\n{'='*100}")
    safe_print("CORRELATION ANALYSIS")
    safe_print(f"{'='*100}")
    
    # Correlate efficiency rank with hours
    if 'efficiency_rank' in column_mapping and 'hours' in column_mapping:
        rank_col = column_mapping['efficiency_rank']
        hours_col = column_mapping['hours']
        
        safe_print(f"\nRelationship: Efficiency Rank vs Hours Required")
        # Group by rank and show average hours
        rank_hours = {}
        for idx, rank_val in enumerate(df_clean[rank_col]):
            rank_val_str = str(rank_val)
            rank_num = None
            nums = re.findall(r'\b([1-5])\b', rank_val_str)
            if nums:
                rank_num = int(nums[0])
            
            hours_val = df_clean.iloc[idx][hours_col]
            hours_str = str(hours_val)
            hour_match = re.search(r'(\d+\.?\d*)\s*(?:hours?|hrs?)', hours_str, re.IGNORECASE)
            if rank_num and hour_match:
                if rank_num not in rank_hours:
                    rank_hours[rank_num] = []
                rank_hours[rank_num].append(float(hour_match.group(1)))
        
        if rank_hours:
            for rank in sorted(rank_hours.keys(), reverse=True):
                avg_hours = sum(rank_hours[rank]) / len(rank_hours[rank])
                safe_print(f"  Rank {rank}: Average {avg_hours:.2f} hours ({len(rank_hours[rank])} workflows)")
    
    # Correlate category with efficiency rank (only for short category names)
    if 'category' in column_mapping and 'efficiency_rank' in column_mapping:
        cat_col = column_mapping['category']
        rank_col = column_mapping['efficiency_rank']
        
        safe_print(f"\nRelationship: Category vs Efficiency Rank")
        safe_print("(Only showing categories with concise names)")
        cat_ranks = {}
        for idx, cat_val in enumerate(df_clean[cat_col]):
            if pd.notna(cat_val):
                cat = str(cat_val).strip()
                # Only include categories with short names (likely actual category names, not descriptions)
                if cat and cat != 'nan' and len(cat) < 80:
                    rank_val = df_clean.iloc[idx][rank_col]
                    if pd.notna(rank_val):
                        rank_val_str = str(rank_val)
                        nums = re.findall(r'\b([1-5])\b(?!\d)', rank_val_str)
                        if nums:
                            if cat not in cat_ranks:
                                cat_ranks[cat] = []
                            cat_ranks[cat].append(int(nums[0]))
        
        if cat_ranks:
            # Sort by average rank descending
            sorted_cats = sorted(cat_ranks.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
            for cat, ranks in sorted_cats:
                avg_rank = sum(ranks) / len(ranks)
                max_rank = max(ranks)
                min_rank = min(ranks)
                safe_print(f"  {cat}:")
                safe_print(f"    Average Rank: {avg_rank:.2f}, Range: {min_rank}-{max_rank}, Workflows: {len(ranks)}")


def analyze_categories_sheet(df):
    """Analyze the Categories sheet."""
    safe_print("\n" + "=" * 100)
    safe_print("CONTENT ANALYSIS: CATEGORIES SHEET")
    safe_print("=" * 100)
    
    safe_print("\nThis sheet appears to organize workflows by:")
    if 'Category' in df.columns:
        categories = df['Category'].dropna().unique()
        safe_print(f"\nCategories found: {len(categories)}")
        for cat in categories:
            safe_print(f"  - {cat}")
    
    if 'Workflow Name' in df.columns:
        workflows = df['Workflow Name'].dropna().tolist()
        safe_print(f"\nTotal workflows listed: {len(workflows)}")
    
    if 'Operational Timing' in df.columns:
        timings = df['Operational Timing'].dropna().unique()
        safe_print(f"\nOperational Timing phases: {len(timings)}")
        for timing in timings[:10]:
            safe_print(f"  - {timing}")


def analyze_roles_sheet(df):
    """Analyze the Roles sheet."""
    safe_print("\n" + "=" * 100)
    safe_print("CONTENT ANALYSIS: ROLES SHEET")
    safe_print("=" * 100)
    
    role_col = None
    for col in df.columns:
        if 'role' in str(col).lower():
            role_col = col
            break
    
    if role_col:
        roles = df[role_col].dropna().tolist()
        safe_print(f"\nIdentified {len(roles)} roles in specialty pharmacy:")
        for i, role in enumerate(roles, 1):
            safe_print(f"  {i}. {role}")
    
    # Show cost information if available
    cost_cols = [col for col in df.columns if 'cost' in str(col).lower() or 'salary' in str(col).lower()]
    if cost_cols:
        safe_print(f"\nFinancial columns found: {', '.join(cost_cols)}")


def main():
    """Main analysis function."""
    file_path = "Workflow Team Starting Point Draft.xlsx"
    
    if not Path(file_path).exists():
        safe_print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    safe_print("=" * 100)
    safe_print("EXCEL CONTENT ANALYSIS")
    safe_print("File: Workflow Team Starting Point Draft.xlsx")
    safe_print("=" * 100)
    
    safe_print("\nOVERVIEW:")
    safe_print("This Excel file appears to document workflow processes for a specialty pharmacy")
    safe_print("or infusion care operation. It includes:")
    safe_print("  1. Detailed workflow processes with efficiency rankings")
    safe_print("  2. Categories and operational timing")
    safe_print("  3. Roles and responsibilities")
    safe_print("  4. Analysis of improvement opportunities and automation potential")
    
    # Read each sheet
    excel_file = pd.ExcelFile(file_path)
    
    # Analyze Workflows sheet (most detailed)
    if 'Workflows' in excel_file.sheet_names:
        df_workflows = pd.read_excel(excel_file, sheet_name="Workflows")
        analyze_workflows_sheet(df_workflows, file_path)
    
    # Analyze Categories sheet
    if 'Categories' in excel_file.sheet_names:
        df_categories = pd.read_excel(excel_file, sheet_name="Categories")
        analyze_categories_sheet(df_categories)
    
    # Analyze Roles sheet
    if 'Roles' in excel_file.sheet_names:
        df_roles = pd.read_excel(excel_file, sheet_name="Roles")
        analyze_roles_sheet(df_roles)
    
    safe_print("\n" + "=" * 100)
    safe_print("ANALYSIS COMPLETE")
    safe_print("=" * 100)


if __name__ == "__main__":
    main()

