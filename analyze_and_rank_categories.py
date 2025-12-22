#!/usr/bin/env python3
"""
Analyze Categories sheet and assign rankings for cost and improvement opportunity
"""

import pandas as pd
import json
from pathlib import Path

def main():
    file_path = "Workflow Team Starting Point Draft.xlsx"
    
    # Read Categories sheet
    df_cat = pd.read_excel(file_path, sheet_name='Categories', header=0)
    
    # Read Workflows sheet to get cost and improvement data
    df_wf = pd.read_excel(file_path, sheet_name='Workflows', header=0)
    
    # Extract workflows with rankings from Workflows sheet
    wf_ranks = {}
    rows_with_rank = df_wf[df_wf['Efficieny Improvement Opportunity (5=Highest)'].notna()]
    
    for idx, row in rows_with_rank.iterrows():
        desc = str(row.get('Category', ''))
        improvement_rank = row.get('Efficieny Improvement Opportunity (5=Highest)', None)
        hours = str(row.get('Hours Required', ''))
        
        # Try to extract workflow number from description
        wf_num = None
        if 'Workflow 1' in desc or 'Referral Intake' in desc or 'initiation of the patient journey' in desc:
            wf_num = 1
        elif 'Workflow 2' in desc or 'Prior Authorization' in desc or 'PA requirements' in desc:
            wf_num = 2
        elif 'Workflow 3' in desc or 'Transfer Triage' in desc or 'payer lockouts' in desc:
            wf_num = 3
        elif 'Workflow 4' in desc or 'Nursing Coordination' in desc or 'skilled nursing services' in desc:
            wf_num = 4
        elif 'Workflow 5' in desc or 'Patient Onboarding' in desc or 'Initial Pharmacist Therapy' in desc:
            wf_num = 5
        elif 'Workflow 6' in desc or 'Refill Clinical Follow-Up' in desc or 'most automatable workflow' in desc:
            wf_num = 6
        elif 'Workflow 7' in desc or 'Ongoing Clinical Assessment' in desc or 'protocol-driven clinical evaluation' in desc:
            wf_num = 7
        elif 'Workflow 8' in desc or 'Therapy Discontinuation' in desc or 'discontinued' in desc:
            wf_num = 8
        elif 'Workflow 9' in desc or 'Special Programs' in desc or 'REMS participation' in desc:
            wf_num = 9
        elif 'Workflow 10' in desc or 'Prescription Processing' in desc or 'legally validates the prescription' in desc:
            wf_num = 10
        elif 'Workflow 11' in desc or 'Dispensing, Compounding' in desc or 'product picking' in desc:
            wf_num = 11
        elif 'Workflow 12' in desc or 'Procurement' in desc or 'procurement workflow' in desc:
            wf_num = 12
        elif 'Workflow 13' in desc or 'unusable products' in desc or 'Returns' in desc:
            wf_num = 13
        elif 'Workflow 14' in desc or 'Shipping Coordination' in desc or 'pack-out' in desc:
            wf_num = 14
        elif 'Workflow 15' in desc or 'Patient Receipt' in desc or 'Proof of Delivery' in desc or 'POD' in desc:
            wf_num = 15
        elif 'Workflow 16' in desc or 'Pharmacy-benefit claims' in desc or 'NCPDP' in desc:
            wf_num = 16
        elif 'Workflow 17' in desc or 'Medical-benefit billing' in desc or 'HCPCS/J-codes' in desc:
            wf_num = 17
        elif 'Workflow 18' in desc or 'Denials Management' in desc or 'adverse coverage determinations' in desc:
            wf_num = 18
        elif 'Workflow 19' in desc or 'Payment Posting' in desc or 'remittances' in desc:
            wf_num = 19
        elif 'Workflow 20' in desc or 'AR Management' in desc or 'underpaid claims' in desc:
            wf_num = 20
        elif 'Workflow 21' in desc or 'Regulatory' in desc or 'licenses' in desc:
            wf_num = 21
        elif 'Workflow 22' in desc or 'Sterile Compounding' in desc or 'USP' in desc:
            wf_num = 22
        elif 'Workflow 23' in desc or 'Human Resources' in desc or 'Workforce' in desc:
            wf_num = 23
        elif 'Workflow 24' in desc or 'PBM' in desc or 'Network Credentialing' in desc:
            wf_num = 24
        elif 'Workflow 25' in desc or 'Manufacturer Contracting' in desc or 'LDD' in desc:
            wf_num = 25
        elif 'Workflow 26' in desc or 'Vendor Management' in desc:
            wf_num = 26
        elif 'Workflow 27' in desc or 'Accreditation' in desc:
            wf_num = 27
        elif 'Workflow 28' in desc or 'Clinical Oversight' in desc or 'COC' in desc:
            wf_num = 28
        elif 'Workflow 29' in desc or 'Quality Management' in desc or 'QMP' in desc:
            wf_num = 29
        elif 'Workflow 30' in desc or 'Temperature Validation' in desc:
            wf_num = 30
        
        if wf_num and pd.notna(improvement_rank):
            # Extract hours if available
            hour_val = None
            if hours and 'hour' in hours.lower():
                import re
                hour_match = re.search(r'(\d+\.?\d*)\s*(?:hours?|hrs?)', hours, re.IGNORECASE)
                if hour_match:
                    hour_val = float(hour_match.group(1))
            
            wf_ranks[wf_num] = {
                'improvement_rank': int(improvement_rank),
                'hours': hour_val,
                'hours_text': hours
            }
    
    # Now process Categories sheet
    categories = []
    for idx in range(len(df_cat)):
        row = df_cat.iloc[idx]
        
        wf_num = row.iloc[0] if len(row) > 0 else None
        category = row.get('Category', '') if 'Category' in df_cat.columns else ''
        wf_name = row.get('Workflow Name', '') if 'Workflow Name' in df_cat.columns else ''
        timing = row.get('Operational Timing', '') if 'Operational Timing' in df_cat.columns else ''
        
        # Check if wf_num is numeric
        wf_num_int = None
        if pd.notna(wf_num):
            try:
                wf_num_str = str(wf_num).strip()
                if wf_num_str.isdigit():
                    wf_num_int = int(wf_num_str)
            except:
                pass
        
        if wf_num_int:
            # Get rankings from workflows data
            improvement_rank = wf_ranks.get(wf_num_int, {}).get('improvement_rank', None)
            hours = wf_ranks.get(wf_num_int, {}).get('hours', None)
            
            # Assign cost rank based on hours (1=highest cost)
            cost_rank = None
            if hours is not None:
                # Rank by hours (higher hours = higher cost = lower rank number)
                # We'll rank relative to other workflows
                pass
            
            categories.append({
                'workflow_num': wf_num_int,
                'category': str(category) if pd.notna(category) else '',
                'workflow_name': str(wf_name) if pd.notna(wf_name) else '',
                'operational_timing': str(timing) if pd.notna(timing) else '',
                'improvement_rank': improvement_rank,
                'hours': hours,
                'improvement_rank_5scale': improvement_rank
            })
    
    # Calculate cost rankings based on hours (1=highest labor cost)
    # Sort by hours descending and assign ranks
    categories_with_hours = [c for c in categories if c['hours'] is not None]
    categories_with_hours.sort(key=lambda x: x['hours'], reverse=True)
    
    for i, cat in enumerate(categories_with_hours):
        cat['cost_rank'] = i + 1
    
    # For workflows without hours, estimate based on improvement rank and category
    # Higher improvement opportunity often correlates with higher cost
    categories_no_hours = [c for c in categories if c['hours'] is None]
    for cat in categories_no_hours:
        # Estimate cost rank based on improvement rank (inverse relationship)
        if cat['improvement_rank']:
            # Map 5-scale to top 10 scale (rough estimate)
            # Rank 5 (high improvement) = Rank 1-3 (high cost)
            # Rank 4 = Rank 4-5
            # Rank 3 = Rank 6-7
            # Rank 2 = Rank 8-9
            # Rank 1 = Rank 10
            if cat['improvement_rank'] == 5:
                cat['cost_rank'] = 1  # Highest cost estimate
            elif cat['improvement_rank'] == 4:
                cat['cost_rank'] = 3
            elif cat['improvement_rank'] == 3:
                cat['cost_rank'] = 6
            elif cat['improvement_rank'] == 2:
                cat['cost_rank'] = 8
            else:
                cat['cost_rank'] = 10
    
    # Convert improvement ranks from 5-scale to top 10 scale (1=highest opportunity)
    for cat in categories:
        if cat['improvement_rank']:
            # Map 5-scale (5=highest) to top 10 scale (1=highest)
            if cat['improvement_rank'] == 5:
                cat['improvement_rank_top10'] = 1
            elif cat['improvement_rank'] == 4:
                cat['improvement_rank_top10'] = 2
            elif cat['improvement_rank'] == 3:
                cat['improvement_rank_top10'] = 5
            elif cat['improvement_rank'] == 2:
                cat['improvement_rank_top10'] = 8
            else:
                cat['improvement_rank_top10'] = 10
        else:
            cat['improvement_rank_top10'] = None
    
    # Sort by workflow number
    categories.sort(key=lambda x: x['workflow_num'])
    
    # Save
    with open('categories_ranked.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(categories)} workflows")
    print(f"\nTop 10 by Cost Rank:")
    sorted_by_cost = sorted([c for c in categories if c.get('cost_rank')], key=lambda x: x['cost_rank'])
    for cat in sorted_by_cost[:10]:
        print(f"  #{cat['workflow_num']}: {cat['workflow_name'][:50]} - Cost Rank: {cat['cost_rank']}, Hours: {cat.get('hours', 'N/A')}")
    
    print(f"\nTop 10 by Improvement Opportunity:")
    sorted_by_imp = sorted([c for c in categories if c.get('improvement_rank_top10')], key=lambda x: x['improvement_rank_top10'])
    for cat in sorted_by_imp[:10]:
        print(f"  #{cat['workflow_num']}: {cat['workflow_name'][:50]} - Improvement Rank: {cat['improvement_rank_top10']}")

if __name__ == "__main__":
    main()

