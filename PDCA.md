# BBAT104: TQM Project - PDCA Continuous Improvement Cycle

**Student Name:** Harshit Bhatt  
**Roll Number:** 2410302018 | Branch: CSE  
**Baseline System:** Parking Management System (Digit 8)  
**Assigned Quality Goal:** Q08 - Improve User Satisfaction  

---

## 1. The Plan-Do-Check-Act (PDCA / Deming) Cycle
 +---------------------------------------------+
   |                  1. PLAN                    |
   | - Identify queue bottleneck at gate entry   |
   | - Establish baseline target: < 10s check-in |
   | - Collect failure data across 100 sessions  |
   +---------------------------------------------+
                          |
                          v
   +---------------------------------------------+
   |                   2. DO                     |
   | - Implement Django web interface            |
   | - Add Poka-Yoke automated duration billing  |
   | - Build keyboard hotkeys (Alt+N, Alt+D)     |
   +---------------------------------------------+
                          |
                          v
   +---------------------------------------------+
   |                  3. CHECK                   |
   | - Generate Pareto 80/20 chart from defects  |
   | - Conduct Ishikawa root-cause investigation |
   | - Measure space utilization accuracy        |
   +---------------------------------------------+
                          |
                          v
   +---------------------------------------------+
   |                   4. ACT                    |
   | - Standardize barrier arm maintenance SOP   |
   | - Implement offline fallback for payments   |
   | - Persist operator display preferences      |
   +---------------------------------------------+

---

## 2. Standardized Quality Checksheet (Defect Log)

*Data Sample: 100 Operational Test Runs over 7 Days*

| Defect Category | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday | Total Count | % of Total | Cumulative % | Action Priority |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Barrier Arm Malfunction** | 8 | 6 | 9 | 5 | 7 | 6 | 4 | **45** | 45.0% | 45.0% | **High (Vital 20%)** |
| **Ticket Printer Jam** | 5 | 4 | 6 | 5 | 3 | 4 | 3 | **30** | 30.0% | 75.0% | **High (Vital 20%)** |
| **Payment Gateway Timeout** | 2 | 3 | 1 | 2 | 4 | 2 | 1 | **15** | 15.0% | 90.0% | Moderate |
| **Bay Sensor Read Error** | 1 | 1 | 2 | 0 | 1 | 1 | 1 | **7** | 7.0% | 97.0% | Low |
| **Software Crash / Freeze** | 0 | 1 | 0 | 0 | 1 | 0 | 1 | **3** | 3.0% | 100.0% | Low |
| **Total Logged Defects** | 16 | 15 | 18 | 12 | 16 | 13 | 10 | **100** | 100.0% | - | - |

---

## 3. Corrective and Preventive Actions (CAPA) Log

| Defect / Problem | Root Cause (from Fishbone) | Corrective Action (Immediate) | Preventive Action (Long-Term Kaizen) | Verification Date | Status |
|---|---|---|---|---|---|
| **Barrier Arm Jams** | Debris accumulation & servo motor strain | Cleared debris and lubed mechanical hinge | Automated preventive maintenance schedule every 5,000 cycles | 2026-10-14 | Verified Closed |
| **Ticket Printer Jams** | Thermal paper curl & moisture | Replaced paper roll and cleaned printer head | Paperless digital check-in with on-screen license plate verification | 2026-10-14 | Verified Closed |
| **Operator Fatigue** | Repetitive mouse clicks and eye strain | Added Dark Mode theme switch | Implemented global keyboard shortcuts (<kbd>Alt+N</kbd>, <kbd>Alt+D</kbd>) | 2026-10-14 | Verified Closed |
