# Parking_Management_System_tqm
Parking management system with oprimised quality.

# Core Tqm goal:
Minimize entry queues & maximize space utilization


# BBAT104: Fundamentals of Total Quality Management (TQM)
## Course Project: Smart Parking Management System
**Academic Session:** 2026–27 | **Max Marks:** 70 Raw Marks  
---
### Student & Topic Allotment Details: 

* **Student Name:** Harshit Bhatt
* **Roll Number:** `2410302018`
* **Branch:** Computer Science & Engineering (CSE) (AI ML)
* **Assigned Last Digit:** `8` &rarr; **Parking Management System**
* **Core TQM Baseline Objective:** *Minimize entry queues & maximize space utilization*
* **Assigned Quality Goal:** **Q08 – Improve User Satisfaction**
* **Assigned 5 Target Features:**
  1. *Interactive Dashboard*
  2. *Visual Reports (SQC Tools)*
  3. *Theme Toggle (Dark/Light Mode)*
  4. *Keyboard Shortcuts*
  5. *User Profile & Facility Settings*


## 🛠️ Tech Stack & Dependencies
* **Backend Framework:** Python 3.x, Django 5.x
* **Database & ORM:** SQLite3 (Django ORM with transactions)
* **Frontend Presentation:** HTML5, CSS3, Bootstrap 5.3, JavaScript (LocalStorage persistence)
* **Statistical Quality Control (SQC):** Matplotlib (Headless Agg backend with Base64 URI streaming)
* **Version Control:** Git & GitHub (Structured progressive commit history $\ge 30$ commits)
---
## 🚀 Quick Setup & Installation Guide
1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd Parking_Management_System_tqm

Install project dependencies:

bash
pip install -r requirements.txt


Run database migrations:

bash
python manage.py migrate

  

Seed initial defect data for Pareto analysis:
 
bash
python seed_data.py


Start the local development server:

bash
python manage.py runserver

  
Access the web application at: http://127.0.0.1:8000/


📖 Feature Walkthrough & User Manual

  
1. Interactive Dashboard (/)
  
Live Telemetry Cards: Real-time counters showing Total Capacity, Currently Parked vehicles, Available Spots, and Total Revenue collected.

  
Occupancy Progress Meter: 
Dynamically shifts colors based on occupancy threshold (Green ≤50% ≤ 50%, Yellow > 50% > 50%, Red > 80% > 80%) to alert supervisors of congestion.

  
One-Click Checkout & Billing: Click "Checkout & Bill" on any active vehicle to trigger automated duration calculation and instant tariff deduction.

  

  
2. Statistical Quality Control (SQC) Reports (/reports/)

  
Pareto Analysis (80/20 Rule): Visual bar-line chart categorizing gate operational failures, isolating the vital 20% causes (Barrier Motor Jam & Ticket Printer Jam) driving 80% of queue wait times.

  
Ishikawa (Fishbone) Diagram: Root-cause investigation categorizing queue drivers across People, Process, Software Code, and Infrastructure.

  

  
3. Theme Toggle (Dark & Light Mode):
  
Click the "🌙 Dark Mode / ☀️ Light Mode" toggle in the top-right navbar, or press Alt + T.

  
Uses browser localStorage to preserve your preference across page refreshes.


  
4. Operator Keyboard Shortcuts

Alt + N → Park New Incoming Vehicle
Alt + D → Return to Live Dashboard
Alt + T → Toggle Dark/Light Mode
Alt + H or ? → Display Shortcuts Cheat-Sheet Modal

  

  
5. Profile & Facility Settings (/profile/):

Customize the Operator Name, Facility Title, Hourly Tariff Rate, and Total Lot Capacity dynamically through the web interface without touching database scripts.

  

  

  
🎯 TQM Principles Applied in Architecture

  

  
Customer Focus: Designing an ergonomic interface with fast hotkeys and visual space meters to eliminate customer wait times.

  
Error Prevention (Poka-Yoke): Automated check-in timestamping and formulaic checkout billing eliminates manual calculation errors and billing disputes.

  
Fact-Based Decision Making: Using empirical defect logs to plot Pareto charts that guide maintenance resources toward the highest-impact fixes.

  
Continuous Improvement (Kaizen): Formulating a documented Plan-Do-Check-Act (PDCA) cycle and FMEA risk matrix to proactively reduce RPN scores.

  
