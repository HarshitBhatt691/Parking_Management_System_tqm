# BBAT104: Software Requirements Specification (SRS)
## Parking Management System (TQM Project)

**Student Name:** Harshit Bhatt  
**Roll Number:** 2410302018 | Branch: CSE  
**Baseline System:** Parking Management System (Digit 8)  
**Assigned Quality Goal:** Q08 - Improve User Satisfaction  

---

## 1. Project Overview & Scope
The ParkSmart TQM Parking Management System is designed to eliminate common gate bottlenecks, minimize vehicular queue waiting times, and maximize facility space utilization through automated duration tracking and live telemetry.

### Core TQM Scope:
* **Error Prevention (Poka-Yoke):** Elimination of manual duration calculation and ticket loss disputes through automated timestamping and formulaic tariff generation.
* **Customer Focus:** High-satisfaction UI features including live capacity gauges, 2D parking bay visualizer, instant keyboard shortcuts, and dark/light mode toggle.
* **Continuous Improvement (Kaizen):** Built-in Statistical Quality Control (SQC) modules generating Pareto 80/20 analyses and Ishikawa Fishbone root-cause diagrams.

---

## 2. System Architecture Flowchart

```
+--------------------------------------------------------------------------+
|                          User / Gate Operator                            |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                      Django Web Presentation Layer                       |
|  - Interactive Dashboard (Live Metrics, 2D Bay Map, Occupancy Progress)  |
|  - Keyboard Shortcut Listener (Alt+N, Alt+D, Alt+Y, Alt+T, Alt+H)        |
|  - Dynamic Theme Engine (Light / Dark Mode Persistent LocalStorage)      |
|  - Visual Reports Portal (Pareto & Fishbone Base64 Stream)               |
|  - Complete CRUD Suite (Add, View, Edit, History, Bill & Delete)         |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                     Business Logic Layer (Django Core App)               |
|  - forms.py: Strict input validation and sanitization (Poka-Yoke)        |
|  - models.py: Duration tracking, fee formulas, and daily tariff caps     |
|  - views.py: CRUD controllers, filter aggregations, error handling       |
|  - sqc_tools.py: Matplotlib statistical SQC engine (80/20 Pareto)        |
+--------------------------------------------------------------------------+
                                     |
                                     v
+--------------------------------------------------------------------------+
|                       Data Persistence Layer (SQLite3)                   |
|  - Vehicle Table: Records active & historical vehicle sessions           |
|  - Defect Table: Tracks operational failure frequencies for SQC          |
|  - ProfileSettings Table: User preferences & tariff configurations       |
+--------------------------------------------------------------------------+
```

---

## 3. Critical-to-Quality (CTQ) Tree

```
Customer Need: Rapid, Transparent & Frictionless Parking
  │
  ├── Driver / Customer Satisfaction
  │     ├── Low Queue Time (CTQ: Entry processed in < 10 seconds)
  │     └── Transparent Billing (CTQ: Automated duration-based fee with daily cap)
  │
  └── Operator Efficiency & Ergonomics (Q08)
        ├── Visual Dashboard (CTQ: Real-time 2D bay occupancy telemetry)
        ├── Ergonomic Interface (CTQ: Keyboard hotkeys & Dark/Light themes)
        ├── Full Audit Control (CTQ: Complete CRUD operations: Add, Edit, Void)
        └── Defect Remediation (CTQ: Dynamic Pareto 80/20 & Fishbone analytics)
```

---

## 4. Functional Requirements (Full CRUD & Q08)

* **FR-01: Vehicle Registration (Create - C):** Capture vehicle registration number, category, and automatic UTC entry timestamp.
* **FR-02: Real-Time Space Telemetry (Read - R):** Display total capacity, current parked vehicles, free slots, 2D bay status, and percentage occupancy meter.
* **FR-03: Vehicle Detail Modification (Update - U):** Allow gate operators to edit license plate numbers or vehicle categories to rectify entry typos.
* **FR-04: Automated Checkout & Tariff Engine (Update - U):** Calculate total duration rounded to billable hours, apply hourly rate with daily maximum cap, and generate receipt.
* **FR-05: Record Cancellation & Voiding (Delete - D):** Permanently remove mistaken entries or cancelled tickets with confirmation safeguards.
* **FR-06: Historical Audit Log (Read - R):** Complete searchable registry of all active and exited vehicles with duration, tariff, and timestamp filters.
* **FR-07: Operator & Facility Customization:** Configure lot capacity, billing rates, facility name, and operator profile dynamically.
* **FR-08: Statistical Quality Control Engine:** Generate on-demand base64 visual Pareto analysis and Ishikawa diagrams for process auditing.
