# BBAT104: Fundamentals of Total Quality Management (TQM)
## Course Project: Smart Parking Management System
**Academic Session:** 2026–27 | **Max Marks:** 70 Raw Marks  

---

### 👨‍💻 Student & Topic Allotment Details
* **Student Name:** Harshit Bhatt
* **Roll Number:** `2410302018`
* **Branch:** Computer Science & Engineering (CSE)
* **Assigned Last Digit:** `8` &rarr; **Parking Management System**
* **Core TQM Baseline Objective:** *Minimize entry queues & maximize space utilization*
* **Assigned Quality Goal:** **Q08 – Improve User Satisfaction**
* **Assigned 5 Target Features:**
  1. *Interactive Dashboard*
  2. *Visual Reports (SQC Tools)*
  3. *Theme Toggle (Dark/Light Mode)*
  4. *Keyboard Shortcuts*
  5. *User Profile & Facility Settings*

---

## 🛠️ Tech Stack & Dependencies
* **Backend Framework:** Python 3.x, Django 5.x
* **Database & ORM:** SQLite3 (Django ORM with transactions & admin registry)
* **Frontend Presentation:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, JavaScript (LocalStorage persistence)
* **Statistical Quality Control (SQC):** Matplotlib (Headless Agg backend with Base64 URI streaming)
* **Version Control:** Git & GitHub (Progressive commit history with 36+ commits)

---

## 🚀 Quick Setup & Installation Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HarshitBhatt691/Parking_Management_System_tqm.git
   cd Parking_Management_System_tqm
   ```

2. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Seed initial TQM defect data (for Pareto SQC):**
   ```bash
   python seed_data.py
   ```

5. **Populate realistic demo vehicle dataset (35-40 vehicles):**
   ```bash
   python populate_vehicles.py
   ```

6. **Start the local development server:**
   ```bash
   python manage.py runserver
   ```
   *Access the web application at: `http://127.0.0.1:8000/`*  
   *Django Admin Portal: `http://127.0.0.1:8000/admin/`*

---

## 📖 Complete CRUD & Feature Walkthrough

### 1. Full CRUD Suite (Create, Read, Update, Delete)
* **Create (C) &rarr; `/add/`:** Register incoming vehicles with automatic UTC entry timestamping.
* **Read (R) &rarr; `/` and `/history/`:** Real-time capacity gauges, 2D parking lot visualizer map (Bays P-01 to P-24), and complete historical audit logs with status filters (`All`, `Parked`, `Exited`).
* **Update (U) &rarr; `/edit/<id>/`:** Modify vehicle details (fix typos in license plate or vehicle type) with duration recalculation.
* **Update & Bill (U) &rarr; `/exit/<id>/`:** Automate departure timestamping, compute parking duration, and calculate tariff using hourly rate with daily maximum cap.
* **Delete (D) &rarr; `/delete/<id>/`:** Cancel mistaken entries or void tickets with confirmation safety prompts.
* **Admin CRUD &rarr; `/admin/`:** Administrative data management with list filters, search fields, and batch operations.

### 2. Interactive Dashboard (`/`)
* **Live Telemetry Cards:** Real-time counters showing Total Capacity, Currently Parked vehicles, Available Spots, and Total Revenue collected.
* **2D Parking Bay Visualizer:** 24 interactive parking slots dynamically showing vacant (green) vs. occupied (red) states.
* **Space Utilization Meter:** Dynamically shifts colors based on occupancy threshold (Green $\le 50\%$, Yellow $> 50\%$, Red $> 80\%$) to alert supervisors of congestion.
* **Live Client-side Search:** Instant search filter matching plate numbers or vehicle classifications as you type.

### 3. Statistical Quality Control (SQC) Reports (`/reports/`)
* **Pareto Analysis (80/20 Rule):** Visual bar-line chart categorizing gate operational failures, isolating the vital 20% causes (Barrier Motor Jam & Ticket Printer Jam) driving 80% of queue wait times.
* **Ishikawa (Fishbone) Diagram:** Root-cause investigation categorizing queue drivers across **People, Process, Software Code, and Infrastructure**.

### 4. Theme Toggle (Dark & Light Mode)
* Click the **"🌙 Dark Mode / ☀️ Light Mode"** toggle in the top-right navbar, or press <kbd>Alt</kbd> + <kbd>T</kbd>.
* Uses browser `localStorage` to preserve your preference across page refreshes.

### 5. Operator Keyboard Shortcuts
* <kbd>Alt</kbd> + <kbd>N</kbd> &rarr; Park New Incoming Vehicle (Create)
* <kbd>Alt</kbd> + <kbd>D</kbd> &rarr; Return to Live Dashboard (Read)
* <kbd>Alt</kbd> + <kbd>Y</kbd> &rarr; View Complete History & Logs (Read All)
* <kbd>Alt</kbd> + <kbd>T</kbd> &rarr; Toggle Dark/Light Mode
* <kbd>Alt</kbd> + <kbd>H</kbd> or <kbd>?</kbd> &rarr; Display Shortcuts Cheat-Sheet Modal

### 6. Profile & Facility Settings (`/profile/`)
* Customize the **Operator Name**, **Facility Title**, **Hourly Tariff Rate**, and **Total Lot Capacity** dynamically through the web interface without touching database scripts.

---

## 🎯 TQM Principles Applied in Architecture
1. **Customer Focus:** Designing an ergonomic interface with fast hotkeys and visual space meters to eliminate customer wait times.
2. **Error Prevention (Poka-Yoke):** Automated check-in timestamping and formulaic checkout billing eliminates manual calculation errors and billing disputes.
3. **Fact-Based Decision Making:** Using empirical defect logs to plot Pareto charts that guide maintenance resources toward the highest-impact fixes.
4. **Continuous Improvement (Kaizen):** Formulating a documented Plan-Do-Check-Act (PDCA) cycle and FMEA risk matrix to proactively reduce RPN scores.

---

## 🎓 Oral Viva Defense Cheat-Sheet
* **Q: Why was the Pareto chart selected?**
  * *A:* To apply the 80/20 rule, determining that fixing barrier arm jams and printer jams resolves $75\%-80\%$ of all parking queue bottlenecks.
* **Q: How does this project apply Poka-Yoke?**
  * *A:* Check-in timestamps and checkout tariffs are calculated automatically by the server using duration formulas, preventing human calculation errors or lost ticket guessing.
* **Q: What is the highest RPN in your FMEA matrix?**
  * *A:* Automated Barrier Arm Jam ($\text{RPN} = 160$), which is mitigated by installing a manual release mechanism and scheduling weekly servo maintenance.
* **Q: What CRUD operations are supported?**
  * *A:* All four operations are supported: **Create** (vehicle check-in), **Read** (dashboard & complete history logs), **Update** (license plate editing and duration checkout billing), and **Delete** (voiding mistaken entries).
