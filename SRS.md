# ParkSmart Pro Enterprise: Software Requirements Specification (SRS)
## Commercial Multi-Level Car Parking Automation & EV Fast Charging Management System
**Document Standard:** IEEE 830-1998 Compliant  
**Academic Session:** 2026–27 | **Course:** BBAT104: Fundamentals of Total Quality Management (TQM)  
**Topic Allotment:** Digit 8 &rarr; Parking Management System  
**Assigned Quality Goal:** Q08 &rarr; Improve User Satisfaction  
**Student Name:** Harshit Bhatt | **Roll No:** 2410302018 | **Branch:** CSE [AI & ML]  
**Institution:** Amrapali University, Haldwani, Uttarakhand  

---

## 1. Introduction & Project Scope

### 1.1 Purpose
This Software Requirements Specification (SRS) describes the complete commercial architecture, functional requirements, non-functional requirements, data models, and security access controls for **ParkSmart Pro Enterprise**. The platform is designed for commercial multi-level car parking facilities and electric vehicle (EV) charging hubs, eliminating queue bottlenecks, automating bay allocation, and enforcing zero-defect data integrity.

### 1.2 Total Quality Management (TQM) Alignment
* **Poka-Yoke (Mistake-Proofing - Shigeo Shingo):** Enforces strict Indian transport authority (RTO) validation rules at the gate, blocking invalid state codes and non-existent district numbers (e.g. `UK-87`) before data reaches the database.
* **Customer Focus & User Satisfaction (Q08):** Eliminates driver circling times through multi-level vacancy telemetry, a self-service "Find My Car" locator, live EV battery charge tracking, and transparent daily fee caps.
* **Andon Visual Management:** Real-time visual representation of 48 physical bays across 4 floors (`B1`, `G`, `F1`, `F2`), capacity heatmaps, animated EV charging telemetry, and remote boom barrier status.
* **Role-Based Process Integrity (RBAC):** Complete operational segregation ensuring that security guards, cashiers, operations managers, and drivers interact only with authorized workstation functions.

---

## 2. Overall System Description & Architecture

```
+---------------------------------------------------------------------------------------------------+
|                            ParkSmart Pro Central Authentication Gateway                           |
|                                       Role Launchpad (/)                                          |
+---------------------------------------------------------------------------------------------------+
                                                  |
                     +----------------------------+----------------------------+
                     |                            |                            |
                     v                            v                            v
       +----------------------------+ +----------------------------+ +----------------------------+
       |   👑 Admin / Owner         | |   💼 Operations Manager    | |   🚗 Gate Operator / Cashier|
       |   Endpoint: /admin-console/| |   Endpoint: /manager/      | |   Endpoint: /operator/     |
       |   - Staff Account Admin    | |   - Multi-Floor Analytics  | |   - 4-Floor Bay Grid Map   |
       |   - DB Health Diagnostics  | |   - Tariff & EV Rates Form | |   - Poka-Yoke Ingress Modal|
       |   - Master Audit Trail     | |   - EV Power Sales Metrics | |   - Instant POS Checkout   |
       |   - Demo Re-Seed Engine    | |   - Recent Turnover Stream | |   - 80mm Thermal Receipt   |
       +----------------------------+ +----------------------------+ +----------------------------+
                     |                            |
                     v                            v
       +----------------------------+ +----------------------------+
       |   🛡️ Security Guard        | |   🚙 Customer / Driver     |
       |   Endpoint: /security/     | |   Endpoint: /customer/     |
       |   - Boom Barrier Actuators | |   - "Find My Car" Locator  |
       |   - Plate Scanner Lookup   | |   - Floor Vacancy Explorer |
       |   - Incident Dispatch Log  | |   - Live EV Battery Gauge  |
       |   - Security Feed & Resolve| |   - Digital POS E-Receipt  |
       +----------------------------+ +----------------------------+
```

### 2.1 Multi-Floor Car Facility Architecture
The facility models a 4-level covered car parking garage containing **48 dedicated car bays**:
1. **Level B1 (Basement EV Fast Charging Hub — 12 Bays: `B1-EV-01` to `B1-EV-12`):**
   * Equipped with Mode 3 / Type 2 AC fast chargers (7.2 kW charging speed).
   * Reserved strictly for Electric Vehicles (EV); standard ICE vehicles are blocked from allocation.
2. **Ground Floor G (Ingress Level — 12 Bays: `G-01` to `G-12`):**
   * Bays `G-01` to `G-06`: Heavy SUV & Luxury bays with reinforced dimensional clearance.
   * Bays `G-07` to `G-12`: Standard Sedans.
3. **Level 1 F1 (First Floor — 12 Bays: `F1-01` to `F1-12`):**
   * Standard passenger cars, sedans, and family vehicles.
4. **Level 2 F2 (Covered Rooftop — 12 Bays: `F2-01` to `F2-12`):**
   * Bays `F2-01` to `F2-06`: Standard Sedans.
   * Bays `F2-07` to `F2-12`: Compact City Hatchbacks.

---

## 3. Specific Functional Requirements (FR-01 to FR-08)

### FR-01: Multi-Stakeholder Authentication & Role-Based Workstations
* **Description:** The system shall authenticate users via password verification across 5 distinct roles: Admin, Operations Manager, Gate Operator, Security Guard, and Customer.
* **Security Rule:** Unauthenticated requests or cross-role URL tampering (e.g. Guard accessing `/admin-console/`) shall be intercepted with an `Access Denied (403)` policy alert and redirected to the user's home workstation.
* **Dynamic Navigation:** The global navigation shell (`base.html`) shall render links strictly authorized for the active authenticated role.

### FR-02: Poka-Yoke Indian License Plate & RTO Validation Engine
* **Description:** The gate check-in interface shall validate license plates against official Indian transport authority registration syntax: `^[A-Z]{2}\d{1,2}[A-Z]{0,3}\d{1,4}$`.
* **District Boundary Rule:** State codes (`UK`, `DL`, `UP`, `HR`, `MH`, etc.) shall be verified against their active RTO district ranges.
* **Rejection Case:** Any entry with an invalid district code (e.g. `UK-87-XXXX`, since Uttarakhand RTO districts strictly range from `UK-01` to `UK-20`) shall be hard-rejected with educational feedback.
* **Real-Time Keystroke Feedback:** The check-in modal shall provide instantaneous AJAX verification (`/api/validate-plate/`) as the operator types.

### FR-03: Multi-Floor Smart Bay Allocation
* **Description:** The system shall maintain real-time occupancy state (`Vacant` vs. `Occupied`) across 48 physical bays on Floors `B1`, `G`, `F1`, and `F2`.
* **Smart Routing:** Auto-allocation shall assign Electric Vehicles to Level B1 EV bays, SUVs to Ground floor bays, and standard passenger cars across Levels F1 and F2.

### FR-04: Integrated EV Fast Charging Telemetry & Battery Gauges
* **Description:** The system shall simulate active 7.2 kW EV fast charging sessions for vehicles parked in Level B1 bays.
* **Telemetry Fields:** Energy delivered in kilowatt-hours (kWh), charging state (`Charging` vs. `Completed`), and visual battery percentage gauge ($35\% \rightarrow 100\%$).
* **Customer Access:** Drivers shall be able to track live battery percentage and power consumed in real time via `/customer/`.

### FR-05: Real-Time Security Perimeter & Barrier Actuators
* **Description:** The Security Guard Console (`/security/`) shall provide remote boom barrier actuators for North Ingress and South Egress lanes with visual state badges (`OPEN` vs. `CLOSED`).
* **Plate Scanner Lookup:** Security personnel shall be able to query license plates on demand to distinguish between authorized parked cars and unregistered visitor vehicles.
* **Incident Dispatch:** The workstation shall provide structured incident logging (Unauthorized parking, blocked lane, barrier issue) with severity classification and 1-click resolution actions.

### FR-06: Unified Duration Billing & 80mm POS Thermal Receipting
* **Description:** Upon vehicle checkout, the system shall compute:
  $$\text{Total Invoice} = \text{Parking Fee (Hours } \times \text{ ₹30/hr, Max ₹250/day)} + \text{EV Power (kWh } \times \text{ ₹15/kWh)}$$
* **Thermal Receipt:** The system shall generate a standard 80mm thermal POS invoice displaying GSTIN registration, vehicle plate, category, duration breakdown, energy line item, taxes, and barcode.

### FR-07: Commercial Facility Tariff & Capacity Governance
* **Description:** Operations Managers and Admins shall have live form controls to adjust hourly parking tariffs, 24-hour ceiling caps, EV electricity rates, and facility operating names without system downtime.

### FR-08: Master Transaction Ledger & Historical Audit Trail
* **Description:** The system shall maintain a permanent, searchable audit ledger (`/history/`) recording all active and departed vehicle sessions with status filters, duration tags, and re-printable receipts.

---

## 4. Non-Functional Requirements (NFR-01 to NFR-05)

* **NFR-01 (Performance & Sub-10s Gate Ingress):** The check-in form and AJAX validation API shall return responses in $< 50\text{ms}$, enabling sub-10 second vehicle ingress.
* **NFR-02 (ACID Transaction Integrity):** The SQLite3 database shall utilize Write-Ahead Logging (WAL) mode ensuring atomic commits and preventing data loss during concurrent checkout transactions.
* **NFR-03 (Role-Based Access Security):** Workstation views shall be secured with server-side RBAC decorators preventing privilege escalation and horizontal role traversal.
* **NFR-04 (Ergonomic Usability & Fatigue Reduction - Q08):** The user interface shall provide persistent Light and Dark themes stored in browser `LocalStorage` and global hotkey navigation (<kbd>Alt+N</kbd>, <kbd>Alt+D</kbd>, <kbd>Alt+Y</kbd>, <kbd>Alt+C</kbd>, <kbd>Alt+T</kbd>).
* **NFR-05 (Mobile Responsiveness):** The Customer Self-Service Portal (`/customer/`) shall be fully responsive across mobile, tablet, and desktop viewports.

---

## 5. Relational Data Dictionary

| Model / Table | Primary Key | Key Attributes & Foreign Keys | Description |
| :--- | :--- | :--- | :--- |
| **`Floor`** | `id` (int) | `floor_number`, `code`, `name`, `total_slots`, `is_ev_enabled` | Building levels (`B1`, `G`, `F1`, `F2`). |
| **`ParkingSlot`** | `id` (int) | `slot_number`, `floor_id` (FK), `slot_type`, `is_occupied`, `is_ev_bay` | 48 physical bays organized by level. |
| **`Vehicle`** | `id` (int) | `license_plate`, `vehicle_type`, `slot_id` (FK), `entry_time`, `exit_time`, `status`, `parking_fee`, `ev_charging_fee`, `fee` | Active and historical vehicle sessions. |
| **`EVChargingSession`** | `id` (int) | `vehicle_id` (1-to-1 FK), `slot_id` (FK), `status`, `energy_kwh`, `rate_per_kwh`, `total_cost` | Real-time smart charger power telemetry. |
| **`SecurityIncident`** | `id` (int) | `reporter`, `incident_type`, `license_plate`, `severity`, `timestamp`, `description`, `is_resolved` | Guard incident logs and resolution status. |
| **`ProfileSettings`** | `id` (int) | `facility_name`, `operator_name`, `hourly_rate`, `daily_max_rate`, `ev_rate_per_kwh`, `total_capacity` | Singleton facility commercial tariffs. |
| **`User`** | `id` (int) | `username`, `password`, `is_staff`, `is_superuser` | Django standard authentication user model. |
