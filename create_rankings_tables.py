#!/usr/bin/env python3
"""
Create Excel Sheet with Rankings Tables from Report.md

Generates an Excel file with two tables:
1. Top 10 Workflows by Total Labor Cost (B.1)
2. Top 10 Workflows by Magnitude of Improvement Opportunity (B.2)
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path

# Data from Report.md B.1: Top 10 Workflows by Total Labor Cost
LABOR_COST_DATA = [
    {
        'Rank': 1,
        'Workflow #': 18,
        'Workflow Name': 'Denials Management & Appeals',
        'Hours/Transaction': '1.5 hrs',
        'Annual Frequency': '300-400 cases',
        'Annual Hours': '450-600 hrs',
        'Est. Annual Cost': '$135K-$180K',
        'Rationale': 'Highest per-case cost; complex appeal drafting; can extend 30+ days'
    },
    {
        'Rank': 2,
        'Workflow #': 2,
        'Workflow Name': 'Prior Authorization (PA) Processing',
        'Hours/Transaction': '1.0-5.0 hrs',
        'Annual Frequency': '800-1,000 PAs',
        'Annual Hours': '800-2,500 hrs',
        'Est. Annual Cost': '$120K-$375K',
        'Rationale': 'Extreme variance (15 min to 48+ hrs); documentation-heavy; major bottleneck'
    },
    {
        'Rank': 3,
        'Workflow #': 4,
        'Workflow Name': 'Nursing Coordination & Skilled Visit Scheduling',
        'Hours/Transaction': '1.0 hrs',
        'Annual Frequency': '600-800 visits',
        'Annual Hours': '600-800 hrs',
        'Est. Annual Cost': '$90K-$120K',
        'Rationale': 'High labor burden; 3+ phone calls per visit (Patient, Nurse, Agency)'
    },
    {
        'Rank': 4,
        'Workflow #': 27,
        'Workflow Name': 'Accreditation Maintenance & Continuous Readiness',
        'Hours/Transaction': '20-40 hrs/month',
        'Annual Frequency': '12 months',
        'Annual Hours': '240-480 hrs',
        'Est. Annual Cost': '$72K-$144K',
        'Rationale': 'Continuous compliance; resource-intensive; quarterly cycles'
    },
    {
        'Rank': 5,
        'Workflow #': 28,
        'Workflow Name': 'Clinical Oversight Committee (COC) Operations',
        'Hours/Transaction': '8-12 hrs/quarter',
        'Annual Frequency': '4 quarters',
        'Annual Hours': '32-48 hrs',
        'Est. Annual Cost': '$60K-$90K',
        'Rationale': 'Requires qualified clinical staff; quarterly analysis; high-value time'
    },
    {
        'Rank': 6,
        'Workflow #': 29,
        'Workflow Name': 'Quality Management Program (QMP) & Reporting',
        'Hours/Transaction': '16-24 hrs/quarter',
        'Annual Frequency': '4 quarters',
        'Annual Hours': '64-96 hrs',
        'Est. Annual Cost': '$48K-$72K',
        'Rationale': 'Ongoing monthly data work; quarterly cycles; annual evaluation'
    },
    {
        'Rank': 7,
        'Workflow #': 9,
        'Workflow Name': 'Special Programs & Ancillary Services (REMS)',
        'Hours/Transaction': '0.25-1.0 hrs',
        'Annual Frequency': '400-600 REMS events',
        'Annual Hours': '100-600 hrs',
        'Est. Annual Cost': '$30K-$90K',
        'Rationale': 'PRN-triggered; Moderate-High complexity; compliance-intensive'
    },
    {
        'Rank': 8,
        'Workflow #': 19,
        'Workflow Name': 'Payment Posting & Reconciliation',
        'Hours/Transaction': '0.5-1.0 hrs',
        'Annual Frequency': '200-300 reconciliations',
        'Annual Hours': '100-300 hrs',
        'Est. Annual Cost': '$30K-$60K',
        'Rationale': 'Medical Benefit reconciliation: Moderate-High; dependent on payer rules'
    },
    {
        'Rank': 9,
        'Workflow #': 13,
        'Workflow Name': 'Inventory Management - Returns & Reverse Distribution',
        'Hours/Transaction': '1.0 hrs',
        'Annual Frequency': '50-100 returns',
        'Annual Hours': '50-100 hrs',
        'Est. Annual Cost': '$15K-$30K',
        'Rationale': 'Moderate complexity; higher for controlled substances or large losses'
    },
    {
        'Rank': 10,
        'Workflow #': 12,
        'Workflow Name': 'Inventory Management - Procurement',
        'Hours/Transaction': '0.75 hrs',
        'Annual Frequency': '100-150 orders',
        'Annual Hours': '75-113 hrs',
        'Est. Annual Cost': '$22K-$34K',
        'Rationale': 'Short to Moderate; varies by product and DSCSA requirements'
    }
]

# Data from Report.md B.2: Top 10 Workflows by Improvement Opportunity
IMPROVEMENT_OPPORTUNITY_DATA = [
    {
        'Rank': 1,
        'Workflow #': 18,
        'Workflow Name': 'Denials Management & Appeals',
        'Automation Score': 5.0,
        'Impact Score': 5.0,
        'Frequency Score': 4.0,
        'Composite Score': 4.7,
        'Est. Annual Savings': '$100K-$135K',
        'Rationale': 'Generative AI perfect for LMN drafting; automated categorization; highest cost workflow'
    },
    {
        'Rank': 2,
        'Workflow #': 2,
        'Workflow Name': 'Prior Authorization (PA) Processing',
        'Automation Score': 5.0,
        'Impact Score': 5.0,
        'Frequency Score': 5.0,
        'Composite Score': 5.0,
        'Est. Annual Savings': '$80K-$250K',
        'Rationale': 'Major bottleneck; Generative AI for clinical criteria extraction; RPA for status updates'
    },
    {
        'Rank': 3,
        'Workflow #': 1,
        'Workflow Name': 'Referral Intake, Enrollment & Benefits Verification',
        'Automation Score': 5.0,
        'Impact Score': 4.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.7,
        'Est. Annual Savings': '$60K-$90K',
        'Rationale': '#1 administrative bottleneck; OCR/NLP opportunities; RPA for payer portals'
    },
    {
        'Rank': 4,
        'Workflow #': 6,
        'Workflow Name': 'Refill Clinical Follow-Up',
        'Automation Score': 5.0,
        'Impact Score': 4.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.7,
        'Est. Annual Savings': '$40K-$60K',
        'Rationale': 'Most automatable workflow; 80% labor reduction potential via digital outreach'
    },
    {
        'Rank': 5,
        'Workflow #': 10,
        'Workflow Name': 'Prescription Processing & Order Entry',
        'Automation Score': 5.0,
        'Impact Score': 4.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.7,
        'Est. Annual Savings': '$50K-$75K',
        'Rationale': 'Highly manual; repetitive data entry; OCR and automated procurement triggers'
    },
    {
        'Rank': 6,
        'Workflow #': 15,
        'Workflow Name': 'Patient Receipt & Delivery Confirmation',
        'Automation Score': 5.0,
        'Impact Score': 3.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.3,
        'Est. Annual Savings': '$20K-$30K',
        'Rationale': 'Carrier API integration; automated POD retrieval; fast ROI'
    },
    {
        'Rank': 7,
        'Workflow #': 5,
        'Workflow Name': 'Patient Onboarding & Initial Clinical Assessment',
        'Automation Score': 4.0,
        'Impact Score': 4.0,
        'Frequency Score': 4.0,
        'Composite Score': 4.0,
        'Est. Annual Savings': '$30K-$45K',
        'Rationale': 'AI-generated care plans; digital pre-assessments; EMR integration'
    },
    {
        'Rank': 8,
        'Workflow #': 7,
        'Workflow Name': 'Ongoing Clinical Assessment',
        'Automation Score': 4.0,
        'Impact Score': 3.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.0,
        'Est. Annual Savings': '$25K-$40K',
        'Rationale': 'Automated data aggregation; AI-powered lab trend analysis'
    },
    {
        'Rank': 9,
        'Workflow #': 16,
        'Workflow Name': 'Claims Submission: Pharmacy Benefit',
        'Automation Score': 4.0,
        'Impact Score': 3.0,
        'Frequency Score': 5.0,
        'Composite Score': 4.0,
        'Est. Annual Savings': '$20K-$35K',
        'Rationale': 'Automated rejection prevention; COB processing automation'
    },
    {
        'Rank': 10,
        'Workflow #': 3,
        'Workflow Name': 'Transfer Triage & Payer Lockout Management',
        'Automation Score': 4.0,
        'Impact Score': 3.0,
        'Frequency Score': 3.0,
        'Composite Score': 3.3,
        'Est. Annual Savings': '$15K-$25K',
        'Rationale': 'Automated transfer packet generation; rules-engine routing'
    }
]


def format_table_header(ws, start_row, start_col, num_cols, title, subtitle=None):
    """Format table header with title and column headers."""
    # Title cell
    title_cell = ws.cell(row=start_row, column=start_col)
    title_cell.value = title
    title_cell.font = Font(bold=True, size=14, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.merge_cells(start_row=start_row, start_column=start_col, end_row=start_row, end_column=start_col + num_cols - 1)
    ws.row_dimensions[start_row].height = 30
    
    # Subtitle if provided
    if subtitle:
        subtitle_cell = ws.cell(row=start_row + 1, column=start_col)
        subtitle_cell.value = subtitle
        subtitle_cell.font = Font(italic=True, size=10)
        subtitle_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(start_row=start_row + 1, start_column=start_col, end_row=start_row + 1, end_column=start_col + num_cols - 1)
        ws.row_dimensions[start_row + 1].height = 20
        header_row = start_row + 2
    else:
        header_row = start_row + 1
    
    return header_row


def format_column_headers(ws, header_row, columns):
    """Format column headers."""
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    header_font = Font(bold=True, size=11, color="000000")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='medium')
    )
    
    for col_idx, col_name in enumerate(columns, 1):
        cell = ws.cell(row=header_row, column=col_idx)
        cell.value = col_name
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    
    ws.row_dimensions[header_row].height = 40


def format_data_rows(ws, start_row, data, columns):
    """Format data rows."""
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row_idx, row_data in enumerate(data, start_row):
        for col_idx, col_name in enumerate(columns, 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            value = row_data.get(col_name, '')
            cell.value = value
            
            # Format numeric scores
            if 'Score' in col_name and isinstance(value, (int, float)):
                cell.number_format = '0.0'
            
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            cell.border = border
        
        # Alternate row coloring
        if row_idx % 2 == 0:
            fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
            for col_idx in range(1, len(columns) + 1):
                ws.cell(row=row_idx, column=col_idx).fill = fill
        
        ws.row_dimensions[row_idx].height = 30


def auto_adjust_column_widths(ws, num_cols, start_col=1):
    """Auto-adjust column widths."""
    for col_idx in range(start_col, start_col + num_cols):
        max_length = 0
        column_letter = get_column_letter(col_idx)
        
        for cell in ws[column_letter]:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        
        # Set width with some padding
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width


def create_rankings_excel(output_file="Workflow_Rankings_Tables.xlsx"):
    """Create Excel file with rankings tables."""
    
    # Create DataFrames
    df_labor_cost = pd.DataFrame(LABOR_COST_DATA)
    df_improvement = pd.DataFrame(IMPROVEMENT_OPPORTUNITY_DATA)
    
    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write DataFrames to separate sheets
        df_labor_cost.to_excel(writer, sheet_name='Labor Cost Rankings', index=False)
        df_improvement.to_excel(writer, sheet_name='Improvement Rankings', index=False)
    
    # Load workbook for formatting
    wb = load_workbook(output_file)
    
    # Format Labor Cost Rankings sheet
    ws_labor = wb['Labor Cost Rankings']
    
    # Table 1: Top 10 by Labor Cost
    labor_columns = ['Rank', 'Workflow #', 'Workflow Name', 'Hours/Transaction', 
                     'Annual Frequency', 'Annual Hours', 'Est. Annual Cost', 'Rationale']
    
    header_row = format_table_header(
        ws_labor, 1, 1, len(labor_columns),
        'Top 10 Workflows by Total Labor Cost',
        'Rank 1 = Highest Labor Cost, Rank 10 = Lowest Labor Cost'
    )
    
    # Clear existing data and write formatted data
    ws_labor.delete_rows(header_row, ws_labor.max_row - header_row + 1)
    
    format_column_headers(ws_labor, header_row, labor_columns)
    format_data_rows(ws_labor, header_row + 1, LABOR_COST_DATA, labor_columns)
    auto_adjust_column_widths(ws_labor, len(labor_columns))
    
    # Add note row
    note_row = header_row + len(LABOR_COST_DATA) + 2
    note_cell = ws_labor.cell(row=note_row, column=1)
    note_cell.value = "* Annual Cost assumes weighted average labor rate of $60/hour (mix of pharmacists, specialists, technicians)"
    note_cell.font = Font(italic=True, size=9)
    note_cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws_labor.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=len(labor_columns))
    
    # Format Improvement Rankings sheet
    ws_improvement = wb['Improvement Rankings']
    
    # Table 2: Top 10 by Improvement Opportunity
    improvement_columns = ['Rank', 'Workflow #', 'Workflow Name', 'Automation Score', 
                          'Impact Score', 'Frequency Score', 'Composite Score', 
                          'Est. Annual Savings', 'Rationale']
    
    header_row = format_table_header(
        ws_improvement, 1, 1, len(improvement_columns),
        'Top 10 Workflows by Magnitude of Improvement Opportunity',
        'Rank 1 = Highest Improvement Opportunity, Rank 10 = Lowest Improvement Opportunity'
    )
    
    # Clear existing data and write formatted data
    ws_improvement.delete_rows(header_row, ws_improvement.max_row - header_row + 1)
    
    format_column_headers(ws_improvement, header_row, improvement_columns)
    format_data_rows(ws_improvement, header_row + 1, IMPROVEMENT_OPPORTUNITY_DATA, improvement_columns)
    auto_adjust_column_widths(ws_improvement, len(improvement_columns))
    
    # Add note row
    note_row = header_row + len(IMPROVEMENT_OPPORTUNITY_DATA) + 2
    note_cell = ws_improvement.cell(row=note_row, column=1)
    note_cell.value = "* Annual Savings assumes 50-70% automation efficiency for high-potential workflows"
    note_cell.font = Font(italic=True, size=9)
    note_cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws_improvement.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=len(improvement_columns))
    
    # Save workbook
    wb.save(output_file)
    print(f"[SUCCESS] Excel file created: {output_file}")
    print(f"  - Sheet 1: Labor Cost Rankings ({len(LABOR_COST_DATA)} workflows)")
    print(f"  - Sheet 2: Improvement Rankings ({len(IMPROVEMENT_OPPORTUNITY_DATA)} workflows)")


def main():
    """Main function."""
    output_file = "Workflow_Rankings_Tables.xlsx"
    
    print("="*80)
    print("Creating Excel File with Rankings Tables from Report.md")
    print("="*80)
    print(f"\nOutput file: {output_file}")
    
    try:
        create_rankings_excel(output_file)
        print("\n" + "="*80)
        print("COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

