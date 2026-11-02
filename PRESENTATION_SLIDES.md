# BBAT104: Fundamentals of Total Quality Management (TQM)
## Course Project Presentation: Smart Parking Management System
**Topic Allotment:** Digit 8 &rarr; Parking Management System  
**Core TQM Goal:** Minimize entry queues & maximize space utilization  
**Assigned Quality Goal:** Q08 &rarr; Improve User Satisfaction  
**Student Name:** Harshit Bhatt | **Roll No:** 2410302018 | **Branch:** CSE  
**Institution:** Amrapali University, Haldwani, Uttarakhand  

---

# 📑 Slide-by-Slide Presentation Content (Ready for MS PowerPoint)

---

## 🖥️ SLIDE 1: Title Slide
* **Slide Title:** ParkSmart TQM: Enterprise Parking Management System
* **Subtitle:** An Integrated Quality Audit, Space Optimization & Full CRUD Platform (BBAT104)
* **Presenter Information:**
  * **👤 Presenter:** Harshit Bhatt
  * **Roll Number:** 2410302018 | Branch: Computer Science & Engineering (CSE)
  * **Academic Session:** 2026–27 | Max Assessment: 70 Raw Marks
  * **Institution:** Amrapali University, Haldwani, Uttarakhand
  * **Baseline Allotment:** Digit 8 &rarr; Parking Management System
  * **Quality Target:** Q08 &rarr; Improve User Satisfaction

---

## 🖥️ SLIDE 2: Problem Statement & Operational Baseline
* **Slide Title:** Problem Statement & Baseline Operational Challenges

* **1. Entry Gate Queuing Bottlenecks (Traffic Flow Baseline):**
  * **Operational Issue:** Peak-hour ingress generates queues exceeding 8–12 vehicles, spilling onto campus access roads.
  * **Root Cause:** Manual handwriting on paper receipts, manual token issuance, and verification latency (45–60s per car).
  * **Baseline Solution:** Sub-second digital check-in with automated UTC timestamping & hotkey execution (<kbd>Alt+N</kbd>).

* **2. Blind Space Utilization & Bay Searching (Capacity Baseline):**
  * **Operational Issue:** Drivers spend 5–10 minutes circling the facility seeking vacant slots, causing gridlock and fuel waste.
  * **Root Cause:** Absence of real-time bay telemetry; gate supervisors have zero live visibility into physical lot occupancy.
  * **Baseline Solution:** 2D Interactive Parking Bay Visualizer (`P-01` to `P-24`) + live color-shifting capacity telemetry.

* **3. Tariff Disputes & Discrepancies (Financial Baseline):**
  * **Operational Issue:** Cashier calculation disputes, lost paper token arguments, and uncontrolled multi-day fee accumulation.
  * **Root Cause:** Subjective manual duration guessing without automated timekeeping or daily billing ceilings.
  * **Baseline Solution:** Poka-Yoke formulaic duration billing with transparent breakdowns and daily maximum tariff caps.

---

## 🖥️ SLIDE 3: Quality Objectives Aligned with TQM Principles
* **Slide Title:** Quality Objectives Aligned with Core TQM Principles

* **Objective 1: Sub-10s Gate Ingress (Customer Focus & Ergonomics):**
  * Accelerate gate clearance via hotkey-driven check-in (<kbd>Alt+N</kbd>), achieving sub-10 second check-in to eliminate queues.

* **Objective 2: 100% Space Telemetry Accuracy (Fact-Based Management):**
  * Real-time synchronization between physical slots and digital counters (Total, Occupied, Vacant) via 2D visual bay mapping.

* **Objective 3: Zero Billing Discrepancies (Poka-Yoke Error Proofing):**
  * Server-side automated duration timestamping with formulaic billing and daily rate caps to prevent human calculation errors.

* **Objective 4: High Ergonomic Usability & Fatigue Reduction (Q08 Focus):**
  * Full-viewport enterprise SaaS interface with persistent Dark/Light theming (<kbd>Alt+T</kbd>) and global keyboard shortcuts.

* **Objective 5: Continuous Kaizen Quality Governance (ISO 9001 & SQC):**
  * Automated 80/20 Pareto defect analytics, Ishikawa root-cause categorization, and an append-only historical audit trail.

---

## 🖥️ SLIDE 4: Operational Scope & Workstation Personas
* **Slide Title:** Operational Scope & Workstation Personas

* **👑 Facility Supervisor / Admin (Console HQ):**
  * Terminal: Supervisor Master Console
  * Configure facility branding, total capacity limits, hourly rates, and daily tariff caps (`/profile/`).
  * Access the complete master parking history and audit registry (`/history/`) with date and status filters.
  * Monitor live gross revenue and review Statistical Quality Control (SQC) audit reports.

* **🚗 Gate Entry Operator (Ingress Kiosk):**
  * Terminal: Entry Gate Barrier #1
  * 1-Click / Hotkey (<kbd>Alt+N</kbd>) vehicle registration (license plate + classification).
  * Real-time visual verification of allocated parking bays on the 2D bay map before barrier release.
  * Automated capacity safeguard alerts when the facility reaches 100% full capacity.

* **💳 Cashier & Exit Operator (Egress Terminal):**
  * Terminal: Exit Toll Booth
  * 1-Click checkout & automated duration tariff calculation.
  * Transparent bill receipt generation with exact duration breakdown (e.g. `2h 15m`).
  * Full CRUD control: modify entry typos (Update) or void mistaken entries (Delete).

* **📊 Quality Auditor / TQM Inspector (Audit Station):**
  * Terminal: SQC Analytics Portal
  * Generate dynamic 80/20 Pareto charts isolating the vital few failure modes.
  * Inspect Ishikawa Fishbone root-cause diagrams across People, Process, Software & Infrastructure.
  * Track Plan-Do-Check-Act (PDCA) Kaizen logs and FMEA RPN scores.

---

## 🖥️ SLIDE 5: Modular Architecture & System Blueprint
* **Slide Title:** Modular Architecture & System Blueprint

* **📁 Clean Enterprise Modular Layout:**
  ```text
  Parking_Management_System_tqm/
  ├── core_parking_system_app1/
  │   ├── models.py       # Relational persistence (Vehicle, Defect, ProfileSettings)
  │   ├── views.py        # Full CRUD controllers & telemetry logic
  │   ├── forms.py        # Poka-Yoke validation & sanitization forms
  │   ├── urls.py         # RESTful app URL routing table
  │   ├── admin.py        # Enterprise Django admin registry
  │   └── sqc_tools.py    # Headless Matplotlib Base64 SQC engine
  ├── main_parking_system_proj/
  │   ├── settings.py     # Central configuration & security
  │   └── urls.py         # Root URL dispatcher
  ├── templates/          # Clean, distraction-free Bootstrap 5.3 UI templates
  ├── seed_data.py        # TQM defect sample dataset
  ├── populate_vehicles.py# 43-vehicle realistic test dataset
  └── manage.py           # Django execution CLI
  ```

* **⭐ The Core Architectural Principle:**
  * *"Presentation never directly alters database state: UI Template &rarr; Form Validation &rarr; View Controller &rarr; SQLite ACID Commit."*
  * Protects relational database tables from invalid user input, enforces business logic, and guarantees atomic commits.

---

## 🖥️ SLIDE 6: Software Requirements Specification (SRS) — IEEE 830
* **Slide Title:** Software Requirements Specification (SRS) — IEEE 830 Standard

* **📋 Core Functional Requirements (FR-01 to FR-08):**
  * **FR-01 (Vehicle Registration - Create):** Capture plate, classification, and UTC entry timestamp.
  * **FR-02 (Live Telemetry - Read):** Stream live capacity, occupied count, available spots, and revenue.
  * **FR-03 (2D Bay Visualizer - Read):** Map active cars to physical bays (`P-01` to `P-24`).
  * **FR-04 (Detail Modification - Update):** Enable operators to edit license plate typos or vehicle classes.
  * **FR-05 (Automated Tariff Billing - Update):** Formulaic duration-based fee calculation with daily cap.
  * **FR-06 (Record Cancellation - Delete):** Permanently void accidental entries with confirmation alerts.
  * **FR-07 (Facility Customization):** Modify tariff rate, capacity limit, and operator metadata dynamically.
  * **FR-08 (SQC Visual Analytics):** Generate dynamic base64 Pareto and Fishbone diagrams on demand.

* **⚡ Non-Functional Requirements (NFR-01 to NFR-04):**
  * **NFR-01 (Performance & Latency):** Sub-20ms page render response; instant client-side table search.
  * **NFR-02 (ACID Reliability):** SQLite3 WAL mode ensuring atomic commits during concurrent checkouts.
  * **NFR-03 (Ergonomic UX):** Distraction-free SaaS design, persistent dark/light theming, and full keyboard navigation.
  * **NFR-04 (Traceability):** Complete historical audit logging of every parked and departed vehicle.

---

## 🖥️ SLIDE 7: Modules and Features Overview
* **Slide Title:** Comprehensive Modules & Functional Capabilities

* **🅿️ Live Command Center Dashboard (`/`):**
  * 4 KPI cards (Total Capacity, Occupied, Vacant, Gross Revenue), color-shifting occupancy bar, and active vehicle list.
* **🗺️ 2D Interactive Parking Bay Visualizer:**
  * 24 interactive parking bays dynamically showing vacant (soft green) vs. occupied (soft red) with hover vehicle details.
* **📝 Full CRUD Operations Portal:**
  * Create (Check-in), Read (Live list), Update (Edit details & Checkout bill), and Delete (Void mistaken entries).
* **📋 Complete Parking History & Audit Log (`/history/`):**
  * Searchable master historical registry with filter pills (`All`, `Parked`, `Exited`), duration tags, and export layout.
* **📊 SQC Visual Reports Portal (`/reports/`):**
  * Dynamic Matplotlib Pareto 80/20 analysis chart and Ishikawa Fishbone root-cause diagram.
* **⚙️ Facility & Profile Settings (`/profile/`):**
  * Real-time configuration of operator credentials, facility branding, hourly rates, and capacity limits.

---

## 🖥️ SLIDE 8: Core Features Aligned with TQM Principles & Quality Goals
* **Slide Title:** Core Features Aligned with TQM Principles (Q08 Focus)

| Implemented Core Feature | Aligned TQM Quality Goal & Principle | Quality Pioneer / Standard |
| :--- | :--- | :--- |
| **Poka-Yoke Duration & Tariff Engine** | Zero Billing Discrepancies & Dispute Prevention | Shigeo Shingo (Poka-Yoke Error Proofing) |
| **Interactive Dashboard & 2D Bay Map** | Space Utilization Maximization & Queue Reduction | Kaizen Continuous Flow Optimization |
| **Pareto 80/20 Defect Analysis** | Fact-Based Decision Making (Vital Few Causes) | Joseph Juran (Pareto Principle) |
| **Ishikawa Fishbone Root-Cause Diagram** | Systematic Defect Cause Categorization | Kaoru Ishikawa (Cause & Effect Analysis) |
| **Keyboard Hotkeys (<kbd>Alt+N</kbd>, <kbd>Alt+D</kbd>, <kbd>Alt+Y</kbd>)** | Operator Ergonomics & Ingress Queue Minimization | Customer & User Satisfaction (Q08) |
| **Persistent Dark / Light Mode Switch** | Visual Comfort & Operator Fatigue Reduction | Usability & Ergonomics Standard (Q08) |
| **Full CRUD Suite with Void Safeguards** | Process Robustness & Data Integrity | Philip Crosby (Zero Defects Standard) |
| **FMEA Matrix & PDCA Continuous Cycle** | Risk Mitigation & Structured Iterative Kaizen | W. Edwards Deming (PDCA Cycle) |

---

## 🖥️ SLIDE 9: Database Architecture & Relational Data Dictionary
* **Slide Title:** Database Design & Relational Data Dictionary

* **Table 1: `Vehicle` (Master Vehicle Registry):**
  * `id`: Integer Primary Key (Auto-increment)
  * `license_plate`: CharField(20) &rarr; Vehicle registration number
  * `vehicle_type`: CharField(50) &rarr; Classification (Sedan, SUV, Hatchback, EV, Bike)
  * `entry_time`: DateTimeField &rarr; Automatic UTC check-in timestamp
  * `exit_time`: DateTimeField (Nullable) &rarr; Checkout timestamp
  * `status`: CharField(20) &rarr; `['Parked', 'Exited']`
  * `fee`: DecimalField(10, 2) &rarr; Final computed duration tariff

* **Table 2: `Defect` (TQM Quality Defect Log):**
  * `id`: Integer Primary Key
  * `defect_type`: CharField(100) &rarr; Bottleneck name (Barrier Jam, Printer Jam, etc.)
  * `frequency`: IntegerField &rarr; Total observed defect occurrences (Checksheet data)

* **Table 3: `ProfileSettings` (Facility Settings):**
  * `id`: Integer Primary Key
  * `operator_name`: CharField(100) &rarr; Supervisor identity
  * `facility_name`: CharField(150) &rarr; Parking lot brand name
  * `hourly_rate`: DecimalField(6, 2) &rarr; Hourly billing rate (₹30.00)
  * `total_capacity`: IntegerField &rarr; Total bays available (50 bays)
  * `contact_email`: EmailField &rarr; Supervisor contact

---

## 🖥️ SLIDE 10: CRUD Operations Implementation Across All Entities
* **Slide Title:** Comprehensive CRUD Implementation Matrix

| Entity / Model | Create (C) | Read (R) | Update (U) | Delete (D) |
| :--- | :---: | :---: | :---: | :---: |
| **Active Vehicles** | `/add/` Form Entry | Live Table & 2D Bay Map | `/edit/<id>/` Plate/Type Edit | `/delete/<id>/` Cancel/Void |
| **Completed Sessions** | Auto-created on Entry | History Log (`/history/`) | `/exit/<id>/` Tariff Billing | `/delete/<id>/` Purge Entry |
| **Facility Profile** | Initial Auto Seed | `/profile/` & Dashboard Header | `/profile/` Form Submission | Admin Reset to Default |
| **SQC Defect Logs** | `seed_data.py` Script | `/reports/` Pareto Analysis | Frequency Increment Engine | Django Admin Purge |
| **Django Admin Portal** | Full Admin Creation | Master Search & Filter Grid | Full Field Update Forms | Batch Record Deletion |

---

## 🖥️ SLIDE 11: Enterprise UI & UX Design Highlights (Q08)
* **Slide Title:** Production-Grade UI Design & Ergonomic Highlights

* **1. Modern Distraction-Free Enterprise Interface:**
  * Clean, production-ready typography using Google Font **Plus Jakarta Sans**.
  * Uncluttered full-viewport layout without student footers or intrusive banners.
  * Live pulsing `🟢 Gate #1 Active` badge and real-time digital clock in header.

* **2. 2D Interactive Parking Bay Visualizer:**
  * 24 interactive slot badges (`P-01` to `P-24`).
  * Instant visual occupancy status: Vacant (soft green) vs. Occupied (soft red with car plate tooltip).

* **3. Dual Persistent Theme Engine (Dark & Light Mode):**
  * Engineered for day/night gate lighting conditions.
  * Instant 1-click toggle (<kbd>Alt+T</kbd>) stored persistently in browser `localStorage`.

* **4. Operator Productivity Hotkeys:**
  * <kbd>Alt+N</kbd> (Park Car), <kbd>Alt+D</kbd> (Dashboard), <kbd>Alt+Y</kbd> (History), <kbd>Alt+T</kbd> (Theme), <kbd>Alt+H</kbd> / <kbd>?</kbd> (Shortcut Modal).

---

## 🖥️ SLIDE 12: Main System Workflow: End-to-End Ingress to Egress
* **Slide Title:** Main System Workflow: End-to-End Vehicle Lifecycle

* **Stage 1: Gate Approach & Arrival:**
  * Motorist reaches Gate #1; operator hits <kbd>Alt+N</kbd>.
  * Operator enters plate number and selects category.

* **Stage 2: Validation & Poka-Yoke Check-in:**
  * Django validates input; records server-side UTC timestamp.
  * System allocates next vacant bay; updates visual map (`P-01` to `P-24`).
  * Barrier gate opens; elapsed queue time $\le 10$ seconds.

* **Stage 3: Live Bay Tracking & Telemetry:**
  * Dashboard counter increments; utilization percentage shifts.
  * Vehicle duration timer updates continuously (`15m`, `1h 20m`, etc.).

* **Stage 4: Egress Checkout & Automated Billing:**
  * Motorist arrives at exit; cashier clicks **"Bill & Exit"**.
  * System computes exact duration; calculates fee with daily cap protection.
  * Receipt generated showing duration and tariff; status set to `Exited`.

* **Stage 5: Audit Log & SQC Defect Tracking:**
  * Departure archived into `/history/`.
  * Any gate barrier or printer delays logged to `Defect` table for Pareto auditing.

---

## 🖥️ SLIDE 13: TQM Quality Analytics: Pareto (80/20) & Fishbone
* **Slide Title:** Statistical Quality Control (SQC): Pareto & Fishbone Analysis

* **📈 Pareto Analysis (80/20 Rule) — Operational Bottlenecks:**
  * **1. Barrier Motor Malfunction (45%):** Mechanical arm stalls causing lane blockage.
  * **2. Ticket Printer Jam (30%):** Paper spool tear causing entry halt.
  * **3. Payment Gateway Timeout (15%):** Network drops during exit card swipe.
  * **4. Bay Sensor False Read (7%):** Ultrasonic dust obstruction.
  * **5. Software Freeze / Crash (3%):** Database locking under load.
  * **⭐ TQM Vital Few Conclusion:** Resolving the top 2 failure modes (Barrier & Printer) eliminates **75% of all parking delays**!

* **🐟 Ishikawa (Fishbone) Root-Cause Decomposition:**
  * **People:** Untrained gate staff, slow cash handling, misreading plates.
  * **Process:** Manual receipt verification, lack of lane signage, unorganized cash reconciliation.
  * **Software Code:** Unindexed queries, missing shortcut hotkeys, lack of automated fee formulas.
  * **Infrastructure:** Barrier servo strain, thermal printer roller wear, sensor alignment drift.

---

## 🖥️ SLIDE 14: TQM Quality Governance: FMEA Risk & Deming PDCA Cycle
* **Slide Title:** Quality Governance: FMEA Risk Audit & PDCA Kaizen Cycle

* **⚠️ Failure Mode and Effects Analysis (FMEA Matrix):**
  * *Formula: $\text{RPN} = \text{Severity (S)} \times \text{Occurrence (O)} \times \text{Detection (D)}$*
  * **Barrier Arm Jam:** $S=8, O=4, D=5 \rightarrow \mathbf{RPN\ 160}$ &rarr; *Action: Weekly servo lubrication & manual lever.*
  * **Ticket Printer Jam:** $S=6, O=5, D=4 \rightarrow \mathbf{RPN\ 120}$ &rarr; *Action: Paperless on-screen plate check-in.*
  * **Payment Gateway Drop:** $S=7, O=4, D=4 \rightarrow \mathbf{RPN\ 112}$ &rarr; *Action: Offline emergency cash fallback mode.*
  * **Bay Sensor Misread:** $S=4, O=5, D=3 \rightarrow \mathbf{RPN\ 60}$ &rarr; *Action: Weekly lens calibration & supervisor override.*
  * **Database Concurrency Lock:** $S=9, O=2, D=3 \rightarrow \mathbf{RPN\ 54}$ &rarr; *Action: SQLite WAL mode & atomic transactions.*

* **🔁 Deming PDCA Kaizen Cycle:**
  * **PLAN:** Identify peak-hour entry bottlenecks ($\ge 45\text{s}$ queue time) via checksheets.
  * **DO:** Deploy ParkSmart Django web app with keyboard hotkeys & automated duration billing.
  * **CHECK:** Generate monthly Pareto charts and monitor check-in times ($\le 10\text{s}$ achieved).
  * **ACT:** Standardize digital check-in across all university gates as standard operating procedure (SOP).

---

## 🖥️ SLIDE 15: Working Application Setup, Verification & Test Dataset
* **Slide Title:** System Launch, Verification & Realistic Dataset

* **🚀 Launch Commands:**
  * `pip install -r requirements.txt` &rarr; Installs Django, Matplotlib, Pandas
  * `python manage.py migrate` &rarr; Applies SQLite3 schema migrations
  * `python seed_data.py` &rarr; Seeds initial Pareto SQC defect matrix
  * `python populate_vehicles.py` &rarr; Generates realistic 43-vehicle lot data
  * `python manage.py runserver` &rarr; Launches web server at `http://127.0.0.1:8000/`

* **📊 Live Verification Telemetry:**
  * **Total Vehicles in Registry:** 43 Vehicles
  * **Currently Parked (Active Bays):** 13 Vehicles (Bays P-01 to P-13 occupied)
  * **Checked-out Turnover:** 30 Departed vehicles with duration-based billing history
  * **System Health:** 0 Django check errors; 100% clean test execution

---

## 🖥️ SLIDE 16: Live Demonstration Walkthrough (Viva Execution Guide)
* **Slide Title:** Live Demonstration Walkthrough (5-Phase Defense)

* **Phase 1: Ingress Check-in & Poka-Yoke (<kbd>Alt+N</kbd>):**
  * Press <kbd>Alt+N</kbd>; enter test car (e.g. `UK-04-AB-9999`); click Register.
  * Point out sub-second response, automatic UTC timestamp, and bay assignment on 2D map.

* **Phase 2: Live Command Center & Telemetry:**
  * Show the 4 KPI cards, color-shifting occupancy bar, and search filter in action.
  * Toggle **Dark Mode** (<kbd>Alt+T</kbd>) to demonstrate persistent dual theming.

* **Phase 3: Full CRUD Demonstration (Update & Delete):**
  * Click **Edit (Pencil)** on any active car &rarr; fix a typo and save.
  * Click **Delete (Trash)** on a test car &rarr; verify confirmation prompt and voiding.

* **Phase 4: Egress Checkout & Transparent Billing:**
  * Click **"Bill & Exit"** on any car &rarr; show automated duration calculation and daily tariff cap.
  * Navigate to **"History & Logs"** (<kbd>Alt+Y</kbd>) &rarr; demonstrate master audit trail and status filters.

* **Phase 5: SQC Visual Reports & Defense:**
  * Open **"SQC Reports"** &rarr; present the dynamic Matplotlib **80/20 Pareto Chart** and **Ishikawa Fishbone Diagram** to defend TQM quality compliance.

---

## 🖥️ SLIDE 17: Conclusion & Thank You
* **Slide Title:** Conclusion & Oral Viva Defense
* **Key Achievements:**
  * 100% compliance with BBAT104 syllabus (Digit 8: Parking Management System).
  * All 5 Q08 Quality Goal features implemented and functioning seamlessly.
  * Comprehensive CRUD suite backed by SQLite ACID transactions and Django Admin.
  * 38+ meaningful Git commits with structured documentation (`SRS.md`, `FMEA.md`, `PDCA.md`).
* **Questions & Discussion:**
  * *"Thank you! Open for Viva Defense and Questions."*
  * Student: **Harshit Bhatt** (Roll No: `2410302018`)
