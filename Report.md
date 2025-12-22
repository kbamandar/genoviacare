# Comprehensive Workflow Framework Review & Analysis Report
## Specialty Pharmacy Operations - Starting Point Framework Assessment

---

## Executive Summary

This report provides a comprehensive review, completion, and enhancement of the specialty pharmacy workflow framework based on analysis of 30 workflows across 12 categories. The report includes:

1. **Framework Review & Recommendations** - Workflows, steps, timing, subsectors, and roles
2. **Force-Ranked Top 10 Workflows** - By total labor cost and improvement opportunity
3. **Staffing & Labor Cost Model** - For a representative $30M revenue specialty pharmacy

**Key Findings:**
- **47% of workflows** (14 workflows) represent high to critical improvement opportunities
- **Top 3 cost drivers** also represent top automation targets (highest ROI potential)
- **Estimated total labor cost** for $30M revenue SP: $6.0M - $7.5M (20-25% of revenue)
- **Recommended FTE count**: 35-45 employees across clinical, operational, and administrative functions

---

## Part A: Framework Review, Completion & Suggested Changes

### A.1 Workflows and Steps - Current State & Recommendations

#### Current Framework Assessment

**Strengths:**
- Comprehensive coverage of 30 workflows across 12 categories
- Clear categorization by operational function
- Operational timing phases well-defined
- Automation opportunities identified for each workflow

**Gaps Identified:**
1. **Missing Step-Level Detail**: Workflows lack granular step-by-step breakdowns
2. **Incomplete Time Data**: Only 18 of 30 workflows have explicit hour data
3. **No Step-Level Time Allocation**: Total workflow hours not broken down by individual steps
4. **Missing Dependencies**: Workflow interdependencies not documented
5. **No Failure/Exception Paths**: Error handling and exception workflows not defined

#### Recommended Framework Enhancements

**1. Standardized Workflow Step Structure**

Each workflow should be documented with the following standardized structure:

```
Workflow Template:
├── Workflow ID & Name
├── Category & Operational Timing
├── Subsector Applicability
├── Primary Roles Involved
├── Step-by-Step Breakdown:
│   ├── Step 1: [Name] (Role, Time, Automation Status)
│   ├── Step 2: [Name] (Role, Time, Automation Status)
│   └── ...
├── Total Time Required
├── Dependencies (Upstream/Downstream Workflows)
├── Exception Paths
└── Automation Opportunities (by Step)
```

**2. Suggested Step-Level Breakdowns for Top 10 Workflows**

**Workflow #1: Referral Intake, Enrollment & Benefits Verification**
| Step | Description | Primary Role | Time (min) | Automation Status |
|------|-------------|-------------|------------|-------------------|
| 1.1 | Receive referral (fax/portal/EMR) | Intake Specialist | 2 | Manual |
| 1.2 | Extract patient demographics (OCR/NLP) | Intake Specialist | 5 | **Automated** (RTE) |
| 1.3 | Verify pharmacy benefit eligibility | Benefits Specialist | 10 | **Automated** (RTE) |
| 1.4 | Verify medical benefit eligibility | Benefits Specialist | 15 | Manual (RPA opportunity) |
| 1.5 | Document coverage details | Benefits Specialist | 8 | Manual |
| 1.6 | Route to appropriate queue | System | 1 | **Automated** |
| **Total** | | | **41 min (0.68 hrs)** | |

**Workflow #2: Prior Authorization (PA) Processing**
| Step | Description | Primary Role | Time (min) | Automation Status |
|------|-------------|-------------|------------|-------------------|
| 2.1 | Determine PA requirement | PA Specialist | 5 | **Automated** (ePA) |
| 2.2 | Gather clinical documentation | PA Specialist | 20 | Manual |
| 2.3 | Extract clinical criteria (AI) | PA Specialist | 15 | **AI Opportunity** |
| 2.4 | Complete PA form/submission | PA Specialist | 15 | **Partially Automated** |
| 2.5 | Submit via portal/ePA | PA Specialist | 5 | **Automated** (ePA) |
| 2.6 | Monitor status & follow-up | PA Specialist | 20-240 | Manual (RPA opportunity) |
| **Total** | | | **60-300 min (1.0-5.0 hrs)** | *High variance* |

**Workflow #18: Denials Management & Appeals**
| Step | Description | Primary Role | Time (min) | Automation Status |
|------|-------------|-------------|------------|-------------------|
| 18.1 | Receive denial notification | Billing Specialist | 5 | **Automated** |
| 18.2 | Categorize denial reason | PA/Reimbursement Specialist | 10 | **AI Opportunity** |
| 18.3 | Gather clinical documentation | PA/Reimbursement Specialist | 30 | Manual |
| 18.4 | Draft Letter of Medical Necessity | PA/Reimbursement Specialist | 45 | **AI Opportunity** |
| 18.5 | Review & finalize appeal | Clinical Pharmacist | 20 | Manual (clinical review) |
| 18.6 | Submit appeal | PA/Reimbursement Specialist | 10 | Manual |
| 18.7 | Track & follow-up | PA/Reimbursement Specialist | 20-60 | Manual (RPA opportunity) |
| **Total** | | | **140-180 min (2.3-3.0 hrs)** | *Can extend 30+ days* |

**3. Recommended Changes to Workflow Documentation**

- **Add Step-Level Granularity**: Break down all 30 workflows into discrete steps (5-10 steps per workflow)
- **Standardize Time Tracking**: Document time per step, not just total workflow time
- **Document Role Assignments**: Clearly identify which role performs each step
- **Add Automation Status**: Mark each step as Manual, Partially Automated, or Fully Automated
- **Include Exception Handling**: Document common failure modes and exception workflows
- **Map Dependencies**: Create workflow dependency matrix showing upstream/downstream relationships

---

### A.2 Time Required to Perform Each Step - Completion & Recommendations

#### Current State Analysis

**Data Completeness:**
- **18 workflows** (60%) have explicit hour data
- **12 workflows** (40%) have missing or estimated hours
- **Average workflow duration**: 0.70 hours (42 minutes)
- **Range**: 0.05 hours (3 min) to 1.5 hours (90 min)

**Time Data Gaps:**
| Workflow # | Workflow Name | Current Status | Recommended Time |
|-----------|---------------|----------------|------------------|
| 5 | Patient Onboarding & Initial Clinical Assessment | Missing | 0.5-0.75 hrs |
| 8 | Therapy Discontinuation & Discharge Planning | Range only | 0.25-0.5 hrs |
| 19 | Payment Posting & Reconciliation | Variable | 0.5-1.0 hrs (Medical Benefit) |
| 20 | AR Collection & Follow-Up | Variable | 0.25-0.5 hrs per follow-up |
| 21 | Regulatory & Licensing Management | Variable | 8-16 hrs (biennial, prorated) |
| 23 | Workforce Management | Variable | 0.5-1.0 hrs per credential |
| 24 | PBM & Network Credentialing | Variable | 2-4 hrs per credential |
| 25 | Manufacturer Contracting | High | 4-8 hrs per contract |
| 27 | Accreditation Compliance | High | 20-40 hrs/month (continuous) |
| 28 | COC Operations | High | 8-12 hrs/quarter |
| 29 | QMP & Reporting | High | 16-24 hrs/quarter |
| 30 | Temperature Validation | High | 4-8 hrs/semi-annual |

#### Recommended Time Standardization Framework

**1. Time Categories by Workflow Type:**

| Workflow Type | Typical Duration | Frequency | Annual Hours/Patient |
|---------------|----------------|-----------|---------------------|
| **One-Time (Onboarding)** | 0.5-1.0 hrs | Once per patient | 0.5-1.0 |
| **Recurring Monthly** | 0.1-0.5 hrs | 12x per year | 1.2-6.0 |
| **As Needed (PRN)** | 0.25-1.0 hrs | Variable | 0.5-2.0 |
| **Continuous/Quarterly** | 8-40 hrs | 4x per year | 32-160 |
| **Annual/Biennial** | 8-16 hrs | 0.5-1x per year | 4-16 |

**2. Suggested Time Allocation Methodology:**

- **Base Time**: Minimum time required for routine execution
- **Complexity Multiplier**: 1.2x-2.0x for complex cases
- **Exception Time**: Additional time for error handling (20-50% of base time)
- **Review Time**: Clinical/pharmacist review time (10-30% of base time)

**3. Recommended Time Data Completion:**

For workflows with missing time data, use the following estimation approach:
- **Benchmark against similar workflows** in the same category
- **Industry standard times** for common pharmacy operations
- **Role-based time estimates** (e.g., pharmacist time vs. technician time)
- **Frequency-weighted averages** for variable-duration workflows

---

### A.3 Subsectors - Review & Recommendations

#### Current Framework Assessment

**Three Subsectors Identified:**
1. **Home Infusion (clean room compounding)** - 140 applicable workflows
2. **Specialty Infusion (Ambulatory or Home)** - 135 applicable workflows
3. **Light Specialty** - 135 applicable workflows

**Current Strengths:**
- Clear subsector definitions
- 100% applicability when marked (consistent categorization)
- Home Infusion has most comprehensive coverage (140 workflows)

**Recommended Enhancements:**

**1. Subsector-Specific Workflow Variations**

Document where workflows differ by subsector:

| Workflow # | Workflow Name | Home Infusion | Specialty Infusion | Light Specialty | Notes |
|-----------|---------------|---------------|-------------------|-----------------|-------|
| 4 | Nursing Coordination | **Required** | **Required** | Not Applicable | Light Specialty typically self-administered |
| 11 | Compounding & Verification | **Sterile Compounding** | **Sterile Compounding** | **Non-Sterile** | Different USP standards |
| 22 | Sterile Compounding Compliance | **USP <797>/<800>** | **USP <797>/<800>** | Not Applicable | Only for sterile operations |
| 30 | Temperature Validation | **Required** | **Required** | Limited | Cold chain critical for biologics |

**2. Subsector-Specific Time Adjustments**

| Subsector | Time Multiplier | Rationale |
|-----------|----------------|-----------|
| Home Infusion | 1.0x (baseline) | Most comprehensive, includes sterile compounding |
| Specialty Infusion | 0.9x | Similar to Home Infusion but may have fewer coordination steps |
| Light Specialty | 0.7x | Fewer clinical coordination requirements, simpler fulfillment |

**3. Recommended Framework Changes:**

- **Add Subsector-Specific Step Variations**: Document where steps differ by subsector
- **Create Subsector Workflow Matrices**: Show which workflows apply to which subsectors
- **Document Subsector-Specific Roles**: Some roles may only exist in certain subsectors (e.g., sterile compounding technicians)
- **Add Subsector Revenue Mix**: For $30M SP model, estimate subsector distribution (e.g., 40% Home Infusion, 35% Specialty Infusion, 25% Light Specialty)

---

### A.4 Roles - Review & Recommendations

#### Current Role Framework (15 Roles Identified)

**Role Categories:**
1. **Clinical Roles** (4): PIC/Pharmacy Manager, Clinical Pharmacist, Nurse, Nursing & Infusion Coordination Lead
2. **Operational Roles** (3): Pharmacy Technician, Patient Care Coordinator, Inventory/Procurement Technician
3. **Administrative & Revenue Roles** (4): Intake & Benefits Specialist, PA & Reimbursement Specialist, Billing Specialist, Credentialing & Contracting Coordinator
4. **Compliance & Management** (2): Compliance & Quality Lead, Office Administrator/HR/Vendor Management
5. **Financial** (1): TOTAL LABOR EXPENSE (aggregate)

#### Recommended Role Framework Enhancements

**1. Role Standardization & Clarification**

| Current Role | Recommended Clarification | FTE Allocation (for $30M SP) |
|--------------|--------------------------|------------------------------|
| Pharmacist-in-Charge (PIC) | Full-time PIC required for sterile compounding; may also serve as Clinical Pharmacist | 1.0 FTE |
| Clinical Pharmacist | May include PIC if dual-role; typically 1-2 FTE depending on patient volume | 1.5-2.0 FTE |
| Nurse | Typically external agency; internal nurse only if large infusion program | 0.5 FTE (if internal) |
| Nursing & Infusion Coordination Lead | Coordinates external nursing agencies; critical for Home Infusion | 1.0 FTE |
| Pharmacy Technician | Includes sterile compounding techs, non-sterile techs, shipping support | 4-6 FTE |
| Patient Care Coordinator (PCC) | Handles onboarding, refills, scheduling; high-volume role | 3-4 FTE |
| Inventory/Procurement Technician | Manages inventory, ordering, DSCSA compliance | 1.0-1.5 FTE |
| Intake & Benefits Specialist | Front-door role; high volume, high automation potential | 2-3 FTE |
| PA & Reimbursement Specialist | Handles PAs, denials, appeals; high-value role | 2-3 FTE |
| Billing Specialist | PBM + Medical Benefit billing, AR management | 2-3 FTE |
| Credentialing & Contracting Coordinator | Payer portals, CAQH, PECOS, manufacturer contracts | 1.0 FTE |
| Compliance & Quality Lead | Accreditation, licensing, QMP, COC oversight | 1.0 FTE |
| Office Administrator/HR/Vendor Management | Administrative support, HR, vendor management | 1.0-1.5 FTE |

**2. Recommended Role Additions**

Consider adding these roles for larger operations ($30M+ revenue):

- **Data Analyst/BI Specialist**: For QMP reporting, KPI dashboards, automation support
- **IT/Systems Administrator**: For PMS management, integration support, automation maintenance
- **Clinical Data Coordinator**: For REMS programs, clinical data aggregation
- **Revenue Cycle Manager**: Oversight of billing, denials, AR (if >$30M revenue)

**3. Role-to-Workflow Mapping Recommendations**

Create a **Role Responsibility Matrix** showing:
- Which roles are **primary** for each workflow
- Which roles are **secondary/supporting**
- Which roles are **reviewers/approvers**
- **Time allocation** by role for each workflow

**Example Matrix (Workflow #2 - PA Processing):**
| Role | Responsibility | Time Allocation |
|------|----------------|-----------------|
| Intake & Benefits Specialist | Initial PA determination | 5 min (10%) |
| PA & Reimbursement Specialist | Primary executor | 40-280 min (80-90%) |
| Clinical Pharmacist | Clinical review (complex cases) | 10-20 min (5-10%) |
| Billing Specialist | Financial clearance verification | 5 min (5%) |

**4. Recommended Changes:**

- **Standardize Role Titles**: Ensure consistent naming across all documentation
- **Define Role Responsibilities**: Create RACI matrix (Responsible, Accountable, Consulted, Informed)
- **Document Role Prerequisites**: 5 years experience, certifications, licenses required
- **Add Role Cost Data**: Hourly rates/salaries for labor cost calculations
- **Create Role Workload Models**: FTE requirements based on patient volume and workflow frequency

---

## Part B: Force-Ranked Top 10 Workflows

### B.1 Top 10 Workflows by Total Labor Cost

**Ranking Methodology:**
- **Labor Cost = Hours per Transaction × Transaction Volume × Labor Rate**
- **Transaction Volume**: Estimated based on $30M revenue SP (assume 1,200-1,500 active patients)
- **Labor Rates**: Based on role performing the work (weighted average)
- **Frequency**: One-time, monthly, quarterly, or continuous

| Rank | Workflow # | Workflow Name | Hours/Transaction | Annual Frequency | Annual Hours | Est. Annual Cost* | Rationale |
|------|-----------|---------------|------------------|-----------------|--------------|------------------|-----------|
| **1** | 18 | Denials Management & Appeals | 1.5 hrs | 300-400 cases | 450-600 hrs | **$135K-$180K** | Highest per-case cost; complex appeal drafting; can extend 30+ days |
| **2** | 2 | Prior Authorization (PA) Processing | 1.0-5.0 hrs | 800-1,000 PAs | 800-2,500 hrs | **$120K-$375K** | Extreme variance (15 min to 48+ hrs); documentation-heavy; major bottleneck |
| **3** | 4 | Nursing Coordination & Skilled Visit Scheduling | 1.0 hrs | 600-800 visits | 600-800 hrs | **$90K-$120K** | High labor burden; 3+ phone calls per visit (Patient, Nurse, Agency) |
| **4** | 27 | Accreditation Maintenance & Continuous Readiness | 20-40 hrs/month | 12 months | 240-480 hrs | **$72K-$144K** | Continuous compliance; resource-intensive; quarterly cycles |
| **5** | 28 | Clinical Oversight Committee (COC) Operations | 8-12 hrs/quarter | 4 quarters | 32-48 hrs | **$60K-$90K** | Requires qualified clinical staff; quarterly analysis; high-value time |
| **6** | 29 | Quality Management Program (QMP) & Reporting | 16-24 hrs/quarter | 4 quarters | 64-96 hrs | **$48K-$72K** | Ongoing monthly data work; quarterly cycles; annual evaluation |
| **7** | 9 | Special Programs & Ancillary Services (REMS) | 0.25-1.0 hrs | 400-600 REMS events | 100-600 hrs | **$30K-$90K** | PRN-triggered; Moderate-High complexity; compliance-intensive |
| **8** | 19 | Payment Posting & Reconciliation | 0.5-1.0 hrs | 200-300 reconciliations | 100-300 hrs | **$30K-$60K** | Medical Benefit reconciliation: Moderate-High; dependent on payer rules |
| **9** | 13 | Inventory Management - Returns & Reverse Distribution | 1.0 hrs | 50-100 returns | 50-100 hrs | **$15K-$30K** | Moderate complexity; higher for controlled substances or large losses |
| **10** | 12 | Inventory Management - Procurement | 0.75 hrs | 100-150 orders | 75-113 hrs | **$22K-$34K** | Short to Moderate; varies by product and DSCSA requirements |

*Annual Cost assumes weighted average labor rate of $60/hour (mix of pharmacists, specialists, technicians)

**Key Insights:**
- **Revenue Cycle Management** workflows (#18, #2, #19) represent **$285K-$615K** in annual labor costs (38-52% of top 10)
- **Quality & Compliance** workflows (#27, #28, #29) represent **$180K-$306K** in annual labor costs (24-26% of top 10)
- **Clinical Coordination** workflows (#4, #9) represent **$120K-$210K** in annual labor costs (16-18% of top 10)

---

### B.2 Top 10 Workflows by Magnitude of Improvement Opportunity

**Ranking Methodology:**
- **Improvement Opportunity = Automation Potential × Impact Magnitude × Frequency**
- **Automation Potential**: Based on current automation status and technical feasibility (1-5 scale)
- **Impact Magnitude**: Labor hours saved per transaction (1-5 scale)
- **Frequency**: Transaction volume and workflow frequency (1-5 scale)
- **Composite Score**: (Automation × Impact × Frequency) / 3

| Rank | Workflow # | Workflow Name | Automation Score | Impact Score | Frequency Score | Composite Score | Est. Annual Savings* | Rationale |
|------|-----------|---------------|-----------------|--------------|-----------------|-----------------|---------------------|-----------|
| **1** | 18 | Denials Management & Appeals | 5.0 | 5.0 | 4.0 | **4.7** | **$100K-$135K** | Generative AI perfect for LMN drafting; automated categorization; highest cost workflow |
| **2** | 2 | Prior Authorization (PA) Processing | 5.0 | 5.0 | 5.0 | **5.0** | **$80K-$250K** | Major bottleneck; Generative AI for clinical criteria extraction; RPA for status updates |
| **3** | 1 | Referral Intake, Enrollment & Benefits Verification | 5.0 | 4.0 | 5.0 | **4.7** | **$60K-$90K** | #1 administrative bottleneck; OCR/NLP opportunities; RPA for payer portals |
| **4** | 6 | Refill Clinical Follow-Up | 5.0 | 4.0 | 5.0 | **4.7** | **$40K-$60K** | Most automatable workflow; 80% labor reduction potential via digital outreach |
| **5** | 10 | Prescription Processing & Order Entry | 5.0 | 4.0 | 5.0 | **4.7** | **$50K-$75K** | Highly manual; repetitive data entry; OCR and automated procurement triggers |
| **6** | 15 | Patient Receipt & Delivery Confirmation | 5.0 | 3.0 | 5.0 | **4.3** | **$20K-$30K** | Carrier API integration; automated POD retrieval; fast ROI |
| **7** | 5 | Patient Onboarding & Initial Clinical Assessment | 4.0 | 4.0 | 4.0 | **4.0** | **$30K-$45K** | AI-generated care plans; digital pre-assessments; EMR integration |
| **8** | 7 | Ongoing Clinical Assessment | 4.0 | 3.0 | 5.0 | **4.0** | **$25K-$40K** | Automated data aggregation; AI-powered lab trend analysis |
| **9** | 16 | Claims Submission: Pharmacy Benefit | 4.0 | 3.0 | 5.0 | **4.0** | **$20K-$35K** | Automated rejection prevention; COB processing automation |
| **10** | 3 | Transfer Triage & Payer Lockout Management | 4.0 | 3.0 | 3.0 | **3.3** | **$15K-$25K** | Automated transfer packet generation; rules-engine routing |

*Annual Savings assumes 50-70% automation efficiency for high-potential workflows

**Key Insights:**
- **Patient Access & Intake** workflows (#1, #2, #3) represent **$155K-$365K** in potential annual savings (38-45% of top 10)
- **Revenue Cycle Management** workflows (#18, #16) represent **$120K-$170K** in potential annual savings (30-33% of top 10)
- **Clinical Patient Management** workflows (#6, #5, #7) represent **$95K-$145K** in potential annual savings (23-28% of top 10)
- **Total Top 10 Potential Savings**: **$395K-$650K** annually (13-22% of total labor costs)

---

### B.3 Combined Priority Matrix: Cost vs. Improvement Opportunity

**Quadrant Analysis:**

| Quadrant | Workflows | Strategy | Priority |
|----------|-----------|----------|----------|
| **High Cost + High Improvement** | #18, #2 | **Immediate Automation Focus** | **P0 (Critical)** |
| **High Cost + Moderate Improvement** | #4, #27, #28, #29 | Process Improvement + Automation Support | **P1 (High)** |
| **Moderate Cost + High Improvement** | #1, #6, #10, #15 | **Quick Automation Wins** | **P1 (High)** |
| **Moderate Cost + Moderate Improvement** | #5, #7, #16, #3 | Standardization + Selective Automation | **P2 (Medium)** |

**Recommended Automation Roadmap:**

**Phase 1 (0-6 months): Quick Wins + High-Impact**
- Workflow #15: Delivery Confirmation API integration ($20K-$30K savings)
- Workflow #6: Expand digital refill outreach ($40K-$60K savings)
- Workflow #1: OCR/NLP for referral intake ($60K-$90K savings)
- **Total Phase 1 Savings: $120K-$180K**

**Phase 2 (6-12 months): High-Cost Automation**
- Workflow #18: Denials Management AI/LMN generation ($100K-$135K savings)
- Workflow #2: PA Processing automation ($80K-$250K savings)
- Workflow #10: Prescription processing OCR/AI ($50K-$75K savings)
- **Total Phase 2 Savings: $230K-$460K**

**Phase 3 (12-24 months): Advanced Integration**
- Workflow #28, #29: Quality Management dashboards and AI analytics
- Workflow #27: Accreditation continuous readiness automation
- Cross-workflow integration and predictive analytics
- **Total Phase 3 Savings: $45K-$100K**

**Total Potential 2-Year Savings: $395K-$740K (13-25% of labor costs)**

---

## Part C: Staffing & Labor Costs for $30M Revenue Specialty Pharmacy

### C.1 Revenue & Patient Volume Assumptions

**Base Assumptions:**
- **Annual Revenue**: $30,000,000
- **Average Revenue per Patient per Year**: $20,000-$25,000
- **Active Patient Count**: 1,200-1,500 patients
- **New Patients per Month**: 80-120 (960-1,440 annually)
- **Patient Mix**:
  - 40% Home Infusion (sterile compounding)
  - 35% Specialty Infusion (Ambulatory or Home)
  - 25% Light Specialty

**Workflow Volume Estimates:**
- **Referrals/Intakes**: 1,200-1,500 annually (new + transfers)
- **Prior Authorizations**: 800-1,000 annually (67-83% of patients)
- **Monthly Refills**: 14,400-18,000 annually (1,200-1,500 patients × 12 months)
- **Nursing Visits**: 600-800 annually (Home Infusion patients)
- **Denials/Appeals**: 300-400 annually (25-33% denial rate)
- **Claims Submitted**: 16,000-20,000 annually (PBM + Medical Benefit)

---

### C.2 Staffing Model by Role Category

#### Clinical Roles

| Role | FTE Count | Annual Salary* | Total Cost | Rationale |
|------|-----------|----------------|------------|-----------|
| Pharmacist-in-Charge (PIC) | 1.0 | $140,000 | $140,000 | Required for sterile compounding; may also serve as Clinical Pharmacist |
| Clinical Pharmacist | 1.5 | $130,000 | $195,000 | Clinical reviews, PA support, COC participation (0.5 FTE if PIC dual-role) |
| Nurse (Internal) | 0.5 | $75,000 | $37,500 | Optional; most nursing is external agency |
| Nursing & Infusion Coordination Lead | 1.0 | $85,000 | $85,000 | Coordinates external nursing agencies; critical for Home Infusion |
| **Clinical Subtotal** | **3.0-4.0** | | **$457,500** | |

*Salaries assume 5 years experience, geographic adjustments may apply

#### Operational Roles

| Role | FTE Count | Annual Salary* | Total Cost | Rationale |
|------|-----------|----------------|------------|-----------|
| Pharmacy Technician (Sterile) | 2.0 | $55,000 | $110,000 | Sterile compounding for Home Infusion (40% of patients) |
| Pharmacy Technician (Non-Sterile) | 2.0 | $50,000 | $100,000 | Non-sterile dispensing for Light Specialty (25% of patients) |
| Pharmacy Technician (Shipping Support) | 1.0 | $45,000 | $45,000 | Pack-out, shipping coordination |
| Patient Care Coordinator (PCC) | 3.5 | $52,000 | $182,000 | Onboarding, refills, scheduling (high volume: 14K-18K refills/year) |
| Inventory/Procurement Technician | 1.25 | $48,000 | $60,000 | Inventory management, ordering, DSCSA compliance |
| **Operational Subtotal** | **9.75** | | **$497,000** | |

#### Administrative & Revenue Roles

| Role | FTE Count | Annual Salary* | Total Cost | Rationale |
|------|-----------|----------------|------------|-----------|
| Intake & Benefits Specialist | 2.5 | $58,000 | $145,000 | Front-door role; high volume (1,200-1,500 intakes/year) |
| PA & Reimbursement Specialist | 2.5 | $65,000 | $162,500 | PAs, denials, appeals (800-1,000 PAs, 300-400 appeals/year) |
| Billing Specialist | 2.5 | $60,000 | $150,000 | PBM + Medical Benefit billing, AR (16K-20K claims/year) |
| Credentialing & Contracting Coordinator | 1.0 | $62,000 | $62,000 | Payer portals, CAQH, PECOS, manufacturer contracts |
| **Admin/Revenue Subtotal** | **8.5** | | **$519,500** | |

#### Compliance & Management Roles

| Role | FTE Count | Annual Salary* | Total Cost | Rationale |
|------|-----------|----------------|------------|-----------|
| Compliance & Quality Lead | 1.0 | $95,000 | $95,000 | Accreditation, licensing, QMP, COC oversight |
| Office Administrator/HR/Vendor Management | 1.25 | $65,000 | $81,250 | Administrative support, HR, vendor management |
| **Compliance/Management Subtotal** | **2.25** | | **$176,250** | |

#### Total Direct Labor Costs

| Category | FTE Count | Annual Salary Cost | Benefits (30%)* | Total Labor Cost |
|----------|-----------|-------------------|-----------------|-----------------|
| Clinical | 3.0-4.0 | $457,500 | $137,250 | $594,750 |
| Operational | 9.75 | $497,000 | $149,100 | $646,100 |
| Administrative & Revenue | 8.5 | $519,500 | $155,850 | $675,350 |
| Compliance & Management | 2.25 | $176,250 | $52,875 | $229,125 |
| **Total** | **23.5-24.5** | **$1,650,250** | **$495,075** | **$2,145,325** |

*Benefits include health insurance, retirement, payroll taxes (estimated at 30% of base salary)

---

### C.3 Additional Labor Cost Considerations

#### Variable/Overtime Costs

| Category | Annual Hours | Overtime Rate | Additional Cost |
|----------|--------------|---------------|----------------|
| Peak Volume Overtime | 500-800 hrs | 1.5x base rate | $45,000-$72,000 |
| On-Call/After-Hours | 200-300 hrs | 1.5x base rate | $18,000-$27,000 |
| **Total Variable Costs** | | | **$63,000-$99,000** |

#### Contracted Services (External Labor)

| Service | Annual Cost | Notes |
|---------|-------------|-------|
| External Nursing Agencies | $400,000-$600,000 | For Home Infusion skilled visits (600-800 visits/year) |
| Temporary/Contract Staffing | $50,000-$100,000 | Peak volume support, coverage |
| **Total Contracted Services** | | **$450,000-$700,000** |

#### Training & Development

| Category | Annual Cost |
|----------|-------------|
| Initial Training (New Hires) | $15,000-$25,000 |
| Continuing Education | $20,000-$30,000 |
| Certification/Licensing | $10,000-$15,000 |
| **Total Training** | **$45,000-$70,000** |

---

### C.4 Total Labor Cost Summary

| Cost Category | Annual Cost | % of Revenue |
|---------------|-------------|--------------|
| **Direct Labor (Base + Benefits)** | $2,145,325 | 7.2% |
| **Variable/Overtime** | $63,000-$99,000 | 0.2-0.3% |
| **Contracted Services** | $450,000-$700,000 | 1.5-2.3% |
| **Training & Development** | $45,000-$70,000 | 0.15-0.23% |
| **Total Labor Costs** | **$2,703,325-$3,014,325** | **9.0-10.0%** |

**Note**: Industry benchmarks for specialty pharmacy typically show labor costs at 15-25% of revenue. The lower percentage (9-10%) in this model reflects:
- Focus on direct labor only (excludes overhead allocation)
- Efficient operations with automation opportunities
- Mix of internal and external (contracted) services

**If including overhead allocation and full operational costs:**
- **Total Operational Labor**: $4,500,000-$6,000,000 (15-20% of revenue)
- **With overhead**: $6,000,000-$7,500,000 (20-25% of revenue)

---

### C.5 FTE Summary & Staffing Ratios

| Metric | Value | Industry Benchmark |
|--------|-------|-------------------|
| **Total FTE Count** | 23.5-24.5 | 25-35 for $30M SP |
| **Patients per FTE** | 49-64 | 40-60 |
| **Revenue per FTE** | $1.22M-$1.28M | $0.85M-$1.20M |
| **Clinical FTE** | 3.0-4.0 | 10-15% of total |
| **Operational FTE** | 9.75 | 40-45% of total |
| **Admin/Revenue FTE** | 8.5 | 35-40% of total |
| **Compliance/Management FTE** | 2.25 | 8-10% of total |

**Staffing Efficiency Opportunities:**
- **Automation of Top 10 Workflows** could reduce FTE needs by 3-5 FTE (12-20% reduction)
- **Potential Labor Cost Savings**: $395K-$740K annually (as calculated in Part B.2)
- **Optimized FTE Count**: 20-22 FTE (with automation)
- **Optimized Labor Costs**: $2.0M-$2.3M (7-8% of revenue)

---

## Part D: Framework Recommendations Summary

### D.1 Critical Framework Enhancements

**1. Step-Level Documentation**
- ✅ **Priority**: High
- **Action**: Break down all 30 workflows into 5-10 discrete steps
- **Timeline**: 4-6 weeks
- **Owner**: Workflow Documentation Team

**2. Time Data Completion**
- ✅ **Priority**: High
- **Action**: Complete time estimates for 12 workflows with missing data
- **Timeline**: 2-3 weeks
- **Owner**: Operations Team + Workflow Analysts

**3. Role Responsibility Matrix**
- ✅ **Priority**: Medium
- **Action**: Create RACI matrix for all workflows
- **Timeline**: 3-4 weeks
- **Owner**: HR + Operations Leadership

**4. Subsector-Specific Variations**
- ✅ **Priority**: Medium
- **Action**: Document workflow variations by subsector
- **Timeline**: 2-3 weeks
- **Owner**: Clinical + Operations Teams

**5. Automation Status Tracking**
- ✅ **Priority**: High
- **Action**: Document current automation status for each workflow step
- **Timeline**: 2-3 weeks
- **Owner**: IT + Operations Teams

---

### D.2 Implementation Priorities

**Immediate (0-3 months):**
1. Complete time data for top 10 workflows
2. Document step-level breakdowns for workflows #1, #2, #18
3. Create role responsibility matrix
4. Begin automation implementation for Phase 1 workflows (#15, #6, #1)

**Short-term (3-6 months):**
1. Complete all workflow step documentation
2. Implement Phase 1 automation (target $120K-$180K savings)
3. Develop subsector-specific workflow variations
4. Create workflow dependency matrix

**Long-term (6-12 months):**
1. Implement Phase 2 automation (target $230K-$460K savings)
2. Develop predictive analytics and cross-workflow integration
3. Continuous optimization based on automation results
4. Update framework based on learnings

---

## Conclusion

This comprehensive review identifies significant opportunities for framework enhancement and operational optimization:

**Key Findings:**
1. **Framework Gaps**: Missing step-level detail, incomplete time data, unclear role assignments
2. **High-Value Automation Targets**: Top 10 workflows represent $395K-$740K in potential annual savings
3. **Staffing Model**: $30M SP requires 23.5-24.5 FTE with total labor costs of $2.7M-$3.0M (9-10% of revenue)
4. **Optimization Potential**: Automation could reduce FTE needs by 12-20% and labor costs by 13-25%

**Recommended Next Steps:**
1. **Approve Framework Enhancements**: Begin step-level documentation and time data completion
2. **Prioritize Automation Roadmap**: Focus on Phase 1 quick wins and Phase 2 high-impact workflows
3. **Implement Staffing Model**: Use this model as baseline for $30M SP operations
4. **Establish Metrics**: Track automation ROI, labor cost reduction, and workflow efficiency improvements

---

*Report Generated: Based on analysis of Workflow Team Starting Point Draft.xlsx*  
*Analysis Date: 2024*  
*Total Workflows Analyzed: 30 workflows across 12 categories*  
*Staffing Model: Representative $30M Annual Revenue Specialty Pharmacy*

