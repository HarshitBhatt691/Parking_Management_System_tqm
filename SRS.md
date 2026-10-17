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
* **Error Prevention (Poka-Yoke):** Elimination of manual duration calculation and ticket loss disputes through automated timestamping.
* **Customer Focus:** High-satisfaction UI features including live capacity gauges, instant keyboard shortcuts, and dark/light mode toggle.
* **Continuous Improvement (Kaizen):** Built-in Statistical Quality Control (SQC) modules generating Pareto 80/20 analyses and Ishikawa Fishbone root-cause diagrams.

---

## 2. System Architecture Flowchart

+--------------------------------------------------------------+ | User / Gate Operator | +--------------------------------------------------------------+ | v +--------------------------------------------------------------+ | Django Web Presentation Layer | | - Interactive Dashboard (Metrics & Occupancy Progress Bar) | | - Keyboard Shortcut Listener (Alt+N, Alt+D, Alt+T, Alt+H) | | - Dynamic Theme Engine (Light / Dark Mode Persistent State) | | - Visual Reports Portal (Pareto & Fishbone Diagrams) | +--------------------------------------------------------------+ | v +--------------------------------------------------------------+ | Business Logic Layer (Django Core App) | | - forms.py: Input validation and sanitization | | - models.py: Duration & automated fee calculation | | - sqc_tools.py: Matplotlib statistical plotting engine | +--------------------------------------------------------------+ | v +--------------------------------------------------------------+ | Data Persistence Layer (SQLite3) | | - Vehicle Table: Records active & historical sessions | | - Defect Table: Tracks operational failures for SQC | | - ProfileSettings Table: User preferences & tariff configs | +--------------------------------------------------------------+

---

## 3. Critical-to-Quality (CTQ) Tree

Customer Need: Rapid & Frictionless Parking │ ├── Driver Driver Satisfaction │ ├── Low Queue Time (CTQ: Entry processed in < 10 seconds) │ └── Transparent Billing (CTQ: Automated exit receipt calculation) │ └── Operator Efficiency (Q08) ├── Visual Dashboard (CTQ: Real-time available slots progress meter) ├── Ergonomic Interface (CTQ: Keyboard hotkeys & Dark/Light themes) └── Defect Remediation (CTQ: Automated SQC Pareto & Fishbone charts)



---

## 4. Functional Requirements

* **FR-01: Vehicle Registration (Check-in):** Capture vehicle registration number, category, and automatic UTC entry timestamp.
* **FR-02: Automated Checkout & Tariff Engine:** Calculate total duration rounded up to the nearest billable hour and compute tariff against dynamic operator settings.
* **FR-03: Real-Time Space Telemetry:** Display total capacity, current parked vehicles, free slots, and percentage occupancy meter.
* **FR-04: Operator Customization:** Configure lot capacity, billing rates, facility name, and operator profile without editing code.
* **FR-05: Statistical Quality Control Engine:** Generate base64 visual Pareto analysis and Ishikawa diagrams on demand.
