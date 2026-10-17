# BBAT104: TQM Project - Risk Audit & FMEA Matrix

**Student Name:** Harshit Bhatt  
**Roll Number:** 2410302018  
**Baseline System:** Parking Management System (Digit 8)  
**Assigned Quality Goal:** Q08 - Improve User Satisfaction  

---

## 1. SIPOC Process Flowchart (System Overview)

| Component | Description |
|---|---|
| **Suppliers (S)** | Motorists, Campus Visitors, Sensor Hardware Vendors, Payment Gateways |
| **Inputs (I)** | License Plate Number, Vehicle Classification, Entry Timestamp, Cash/Card |
| **Process (P)** | Automatic Plate Entry -> Slot Allocation -> Duration Timestamping -> Tariff Billing -> Barrier Release |
| **Outputs (O)** | Time-stamped Digital Ticket, Assigned Spot, Final Invoice/Receipt, Occupancy Analytics |
| **Customers (C)** | Drivers, Parking Operators, Campus Security, Audit Administrators |

---

## 2. Failure Mode and Effects Analysis (FMEA) Matrix

*Rating Scale: 1 (Lowest Risk) to 10 (Highest Severity / Frequency / Detection Difficulty)*  
*$\text{RPN} = \text{Severity (S)} \times \text{Occurrence (O)} \times \text{Detection (D)}$*

| ID | Process Step | Potential Failure Mode | Potential Effect of Failure | S | Potential Causes | O | Current Controls | D | RPN | Recommended Action (Mitigation) |
|---|---|---|---|---|---|---|---|---|---|---|
| **FM-01** | Vehicle Entry | Automated Barrier Arm Jam | Severe entry queue bottleneck; traffic backspill | 8 | Mechanical motor failure / debris | 4 | Visual alert on operator console | 5 | **160** | Install Poka-Yoke manual release lever & periodic servo maintenance |
| **FM-02** | Ticket Check-in | Ticket Printer Hardware Jam | Motorist entry delay; unrecorded vehicles | 6 | Paper spool exhausted; thermal head dirty | 5 | Out-of-paper warning prompt | 4 | **120** | Switch to digital screen QR code tickets & paperless logging |
| **FM-03** | Checkout & Billing | Payment Gateway / Network Timeout | Motorist trapped at exit lane; queue buildup | 7 | Intermittent internet loss / API timeout | 4 | Automatic failover retry | 4 | **112** | Implement offline cash checkout fallback mode in Django |
| **FM-04** | Slot Allocation | Ultrasonic Bay Sensor False Reading | Inaccurate available slot counter on UI | 4 | Sensor misalignment or lens dust | 5 | Periodic database sync | 3 | **60** | Calibrate sensors weekly and provide operator manual slot override |
| **FM-05** | Software System | Database Lock / Crash | Total halt of entry & exit operations | 9 | Unoptimized concurrent write queries | 2 | Automated SQLite transaction rollback | 3 | **54** | Add database indexing and background automated backups |

---

## 3. Critical-to-Quality (CTQ) Parameters
* **CTQ-1: Mean Check-in Wait Time:** $\le 10$ seconds per incoming vehicle.
* **CTQ-2: Space Utilization Accuracy:** $100\%$ consistency between dashboard counters and actual occupancy.
* **CTQ-3: Checkout Duration:** $\le 15$ seconds for fee calculation and receipt generation.
* **CTQ-4: System Availability:** $\ge 99.5\%$ operational uptime during peak traffic hours.
