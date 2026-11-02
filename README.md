# ParkSmart Pro Enterprise
## Commercial Multi-Level Car Parking Automation & EV Fast Charging Management System

[![Django 5.x](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap 5.3](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

---

### 🏢 System Overview
**ParkSmart Pro** is a ready-to-use, production-grade commercial multi-level car parking automation and EV charging platform designed for multi-stakeholder facility operations. Built with industrial **Poka-Yoke (Mistake-Proofing)** principles, the system prevents invalid data entry, coordinates real-time multi-floor slot routing, manages 7.2 kW EV smart charging telemetry, and produces itemized GST POS thermal invoices.

---

## 👥 1. Dedicated Stakeholder Workstations

The platform boots directly onto an interactive **Auth & Persona Launchpad (`/`)** with 1-click evaluation access and role credentials:

| Stakeholder / Persona | Operational Scope | Dedicated Route | Default Credentials |
| :--- | :--- | :--- | :--- |
| **👑 Admin / Owner** | System audit, user accounts, database diagnostics, gross revenue audit | `/admin-console/` & `/admin/` | `admin` / `admin123` |
| **💼 Operations Manager** | Multi-floor capacity heatmaps, hourly tariffs, EV kWh pricing, financial analytics | `/manager/` | `manager` / `manager123` |
| **🚗 Gate Operator / Cashier** | High-speed vehicle check-in with Poka-Yoke RTO verification, bay allotment, POS checkout | `/operator/` | `operator` / `operator123` |
| **🛡️ Security Guard** | Boom barrier override (Ingress/Egress), live plate scanner lookup, security dispatch | `/security/` | `guard` / `guard123` |
| **🚙 Customer / Driver** | "Find My Car" locator, live floor vacancy explorer, real-time EV battery gauge, e-receipt | `/customer/` | Public / `customer` |

---

## 🏗️ 2. Multi-Floor Car Parking Architecture

The facility features 48 dedicated car parking bays organized across 4 physical building levels with real-time sensor simulation:

* **⚡ Level B1: Basement Fast Charging Hub (12 Bays: `B1-EV-01` to `B1-EV-12`)**
  * Reserved exclusively for Electric Vehicles (EV).
  * Equipped with virtual 7.2 kW AC smart chargers, battery percentage monitoring, and power telemetry.
* **🚗 Level G: Ground Floor (12 Bays: `G-01` to `G-12`)**
  * Bays `G-01` to `G-06`: Heavy SUV & Premium Vehicles.
  * Bays `G-07` to `G-12`: Standard Sedans.
* **🚙 Level F1: First Floor (12 Bays: `F1-01` to `F1-12`)**
  * Standard Sedans and City Cars.
* **🛞 Level F2: Second Floor Covered Rooftop (12 Bays: `F2-01` to `F2-12`)**
  * Standard and Compact Cars (`F2-07` to `F2-12`).

---

## 🛡️ 3. Poka-Yoke Indian License Plate & RTO Validation Engine

The gate check-in terminal is protected by an industrial **Poka-Yoke (Mistake-Proofing)** validation engine (`rto_validator.py`):

1. **State Registration Check:** Validates official Indian state codes (`UK`, `DL`, `UP`, `HR`, `MH`, `PB`, `RJ`, `KA`, etc.).
2. **State-Specific RTO District Boundary Check:**
   * **Uttarakhand (`UK`):** Strictly enforces district codes from `01` to `20` (`UK-01` Almora &rarr; `UK-20` Ranikhet).
   * **Rejection Example:** Entering **`UK-87-XXXX`** is immediately blocked with the error message:  
     `"Poka-Yoke Error Prevention: 'UK-87' is an invalid RTO registration. Uttarakhand RTO district codes strictly range from UK-01 to UK-20 (UK-87 does not exist)."`
   * **Acceptance Example:** Entering **`uk04ak5521`** is instantly verified as Uttarakhand (Nainital / Haldwani RTO) and normalized to `UK-04-AK-5521`.
3. **Real-Time AJAX Feedback:** The operator check-in modal validates input on keystroke via `/api/validate-plate/`.

---

## ⚡ 4. EV Fast Charging Telemetry & Combined Billing

1. **Smart Bay Assignment:** Vehicles flagged as EV or requesting charging are automatically allocated to Level B1 EV bays.
2. **Active Telemetry:** Tracks energy delivered (kWh), charging status (`Charging` &rarr; `Completed`), and visual battery percentage gauge (35% &rarr; 100%).
3. **Unified Checkout Invoice:**
   $$\text{Total Invoice} = \text{Parking Fee (Hours } \times \text{ ₹30/hr, Max ₹250/day)} + \text{EV Power (kWh } \times \text{ ₹15/kWh)}$$
4. **Thermal POS Receipt:** Generates printable 80mm GST receipt with itemized charges and barcode.

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

3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Seed commercial multi-floor layout, active fleet, and stakeholder accounts:**
   ```bash
   python seed_multi_floor.py
   ```

5. **Run test suite:**
   ```bash
   python manage.py test
   ```

6. **Start the production dev server:**
   ```bash
   python manage.py runserver
   ```
   * Access Launchpad: `http://127.0.0.1:8000/`
   * Django Superuser Admin: `http://127.0.0.1:8000/admin/`

---

## ⌨️ Operator Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| <kbd>Alt</kbd> + <kbd>N</kbd> | Open Fast Vehicle Check-In Modal |
| <kbd>Alt</kbd> + <kbd>D</kbd> | Operator Terminal |
| <kbd>Alt</kbd> + <kbd>Y</kbd> | Parking Logs & History |
| <kbd>Alt</kbd> + <kbd>C</kbd> | Customer Self-Service Portal |
| <kbd>Alt</kbd> + <kbd>T</kbd> | Toggle Light / Dark Mode |
| <kbd>Alt</kbd> + <kbd>H</kbd> or <kbd>?</kbd> | Open Hotkeys Help Modal |
