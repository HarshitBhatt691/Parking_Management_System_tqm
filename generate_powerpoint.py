import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Enterprise Palette
    C_NAVY = RGBColor(15, 23, 42)       # #0f172a
    C_BLUE = RGBColor(37, 99, 235)      # #2563eb
    C_LIGHT_BLUE = RGBColor(239, 246, 255) # #eff6ff
    C_GREEN = RGBColor(16, 185, 129)    # #10b981
    C_AMBER = RGBColor(245, 158, 11)    # #f59e0b
    C_DARK_GRAY = RGBColor(30, 41, 59)  # #1e293b
    C_MUTED = RGBColor(100, 116, 139)   # #64748b
    C_LIGHT_BG = RGBColor(248, 250, 252)# #f8fafc
    C_WHITE = RGBColor(255, 255, 255)
    C_BORDER = RGBColor(226, 232, 240)  # #e2e8f0

    def add_header(slide, title_text, category_tag="PARKSMART PRO ENTERPRISE"):
        # Header strip
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_NAVY
        top_bar.line.color.rgb = C_NAVY

        # Accent border line
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_BLUE
        accent.line.color.rgb = C_BLUE

        # Tag text
        tx = top_bar.text_frame
        tx.word_wrap = True
        tx.margin_left = Inches(0.8)
        tx.margin_top = Inches(0.12)
        
        p0 = tx.paragraphs[0]
        p0.text = category_tag.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_AMBER

        p1 = tx.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.35))
        ftx = footer_box.text_frame
        ftx.margin_left = ftx.margin_top = ftx.margin_right = ftx.margin_bottom = 0
        fp = ftx.paragraphs[0]
        fp.text = "ParkSmart Pro Enterprise | Harshit Bhatt (2410302018) | BBAT104 Course Project Defense"
        fp.font.size = Pt(9)
        fp.font.color.rgb = C_MUTED

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.color.rgb = C_NAVY

    # Hero card
    hero = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.933), Inches(5.1))
    hero.fill.solid()
    hero.fill.fore_color.rgb = RGBColor(24, 34, 58)
    hero.line.color.rgb = RGBColor(45, 60, 95)
    hero.line.width = Pt(1.5)

    htx = hero.text_frame
    htx.word_wrap = True
    htx.margin_left = Inches(0.8)
    htx.margin_right = Inches(0.8)
    htx.margin_top = Inches(0.6)

    hp0 = htx.paragraphs[0]
    hp0.text = "🅿️ ENTERPRISE TQM SOFTWARE DEFENSE"
    hp0.font.size = Pt(12)
    hp0.font.bold = True
    hp0.font.color.rgb = C_AMBER

    hp1 = htx.add_paragraph()
    hp1.text = "ParkSmart Pro Enterprise"
    hp1.font.size = Pt(36)
    hp1.font.bold = True
    hp1.font.color.rgb = C_WHITE
    hp1.space_before = Pt(8)

    hp2 = htx.add_paragraph()
    hp2.text = "Multi-Level Car Parking Automation, EV Fast Charging Telemetry & Poka-Yoke RTO Engine"
    hp2.font.size = Pt(16)
    hp2.font.color.rgb = RGBColor(186, 215, 255)
    hp2.space_before = Pt(6)

    hp3 = htx.add_paragraph()
    hp3.text = "Course: BBAT104 - Fundamentals of Total Quality Management (TQM) | Quality Goal: Q08"
    hp3.font.size = Pt(13)
    hp3.font.color.rgb = C_MUTED
    hp3.space_before = Pt(16)

    # Presenter Details box
    pbox = slide1.shapes.add_textbox(Inches(2.0), Inches(4.3), Inches(9.333), Inches(1.6))
    ptx = pbox.text_frame
    ptx.word_wrap = True

    pp1 = ptx.paragraphs[0]
    pp1.text = "👤 Student Presenter: Harshit Bhatt   •   Roll No: 2410302018   •   Branch: Computer Science & Engineering"
    pp1.font.size = Pt(13)
    pp1.font.bold = True
    pp1.font.color.rgb = C_WHITE

    pp2 = ptx.add_paragraph()
    pp2.text = "🏛️ Institution: Amrapali University, Haldwani (Uttarakhand)   •   Allotment: Digit 8 (Parking Management)"
    pp2.font.size = Pt(12)
    pp2.font.color.rgb = C_MUTED
    pp2.space_before = Pt(4)

    pp3 = ptx.add_paragraph()
    pp3.text = "🔒 Security Architecture: 5 Stakeholder Workstations with Role-Based Access Control (RBAC)"
    pp3.font.size = Pt(12)
    pp3.font.color.rgb = C_GREEN
    pp3.space_before = Pt(4)

    # Helper function for 2-column or 3-column card layouts
    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_BLUE, bg_color=C_WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1)

        # Accent top bar
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.color.rgb = accent_color

        tx = card.text_frame
        tx.word_wrap = True
        tx.margin_left = Inches(0.25)
        tx.margin_right = Inches(0.25)
        tx.margin_top = Inches(0.2)

        tp = tx.paragraphs[0]
        tp.text = title
        tp.font.size = Pt(14)
        tp.font.bold = True
        tp.font.color.rgb = C_DARK_GRAY

        for b in body_bullets:
            bp = tx.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(11)
            bp.font.color.rgb = C_DARK_GRAY
            bp.space_before = Pt(5)

        return card

    # ==========================================
    # SLIDE 2: THE 5 STAKEHOLDERS (REQUESTED SLIDE)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Stakeholder Ecosystem: 5 Dedicated Workstations", "USER PERSONAS & ROLE SEPARATION")

    # 5 Cards across the slide
    card_w = Inches(2.25)
    card_h = Inches(5.4)
    gap = Inches(0.18)
    start_x = Inches(0.7)
    card_y = Inches(1.4)

    # 1. Admin
    add_card(slide2, start_x, card_y, card_w, card_h, "👑 Admin / Owner", [
        "Scope: Executive governance & system integrity.",
        "Console: /admin-console/",
        "User account management & staff permissions.",
        "Gross financial auditing & turnover reconciliation.",
        "System diagnostics, database health, & demo re-seeding.",
        "Global facility config & contact parameters."
    ], C_NAVY)

    # 2. Manager
    add_card(slide2, start_x + (card_w + gap), card_y, card_w, card_h, "💼 Operations Mgr", [
        "Scope: Daily capacity & commercial tariffs.",
        "Console: /manager/",
        "Multi-floor capacity heatmaps (B1, G, F1, F2).",
        "Hourly parking rate & daily max cap control.",
        "EV fast charging tariff setting (₹15/kWh).",
        "Fleet turnover streams & revenue breakdowns."
    ], C_GREEN)

    # 3. Operator
    add_card(slide2, start_x + (card_w + gap)*2, card_y, card_w, card_h, "🚗 Gate Operator", [
        "Scope: Vehicle check-in & cashier billing.",
        "Console: /operator/",
        "High-speed ingress entry (<10s) with Alt+N.",
        "Interactive 4-floor bay status map.",
        "Smart auto-allocation (EV->B1, SUV->G).",
        "Checkout fee calculation & 80mm POS invoice printing."
    ], C_BLUE)

    # 4. Guard
    add_card(slide2, start_x + (card_w + gap)*3, card_y, card_w, card_h, "🛡️ Security Guard", [
        "Scope: Perimeter access & gate barrier control.",
        "Console: /security/",
        "Boom barrier actuators (Ingress/Egress overrides).",
        "ANPR camera plate lookup against lot database.",
        "Visitor & suspicious car identification.",
        "Real-time security incident logging & dispatch."
    ], C_AMBER)

    # 5. Customer
    add_card(slide2, start_x + (card_w + gap)*4, card_y, card_w, card_h, "🚙 Customer / Driver", [
        "Scope: Self-service vehicle finding & telemetry.",
        "Portal: /customer/",
        "'Find My Car' instant license plate locator.",
        "Allotted floor, bay number & walking directions.",
        "Live EV battery charge % gauge & kWh delivered.",
        "Floor vacancy explorer for arriving motorists."
    ], RGBColor(6, 182, 212))

    # ==========================================
    # SLIDE 3: SECURITY & ROLE-BASED ACCESS CONTROL (RBAC)
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Enterprise Security Architecture: Strict RBAC Enforcement", "ACCESS CONTROL & AUTHENTICATION")

    c_w2 = Inches(5.7)
    c_h2 = Inches(5.4)
    add_card(slide3, Inches(0.8), Inches(1.4), c_w2, c_h2, "🔒 Server-Side Role Enforcement (@require_role)", [
        "Zero Hardcoded Bypass: Eliminated all unauthenticated 1-click bypasses.",
        "Cryptographic Authentication: Every stakeholder must authenticate through Django's PBKDF2 credential verification.",
        "Strict 403 Policy Interception: If a Security Guard attempts to open /admin-console/ or /manager/, the server halts execution immediately.",
        "Immediate Safe Redirection: Unauthorized attempts flash an alert and bounce the user back to their authorized home console.",
        "Administrative Supervisory Access: Admins maintain executive oversight across all operational consoles."
    ], C_BLUE)

    add_card(slide3, Inches(6.8), Inches(1.4), c_w2, c_h2, "🌐 Dynamic UI & Navbar Isolation", [
        "Context-Aware Navigation: Global context processor (auth_role_context) filters links based on authenticated user.",
        "Zero Cross-Role Leakage: Guards only see Security Gate links. Operators only see Operator Terminal. Public visitors see zero internal workstations.",
        "Interactive Role Modal (#stakeholderAuthModal): Clicking any card opens a dynamic modal pre-filling username with demo password prompts.",
        "Explicit Sign-Out Protocol: Active session pill in navbar shows current user handle with one-click sign-out to switch roles.",
        "Protected REST Endpoints: Plate validation and incident resolution endpoints verify session authenticity."
    ], C_NAVY)

    # ==========================================
    # SLIDE 4: POKA-YOKE RTO LICENSE PLATE ENGINE
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Poka-Yoke RTO Anti-Error Engine (Zero-Defect Quality)", "MISTAKE-PROOFING IN PRACTICE")

    add_card(slide4, Inches(0.8), Inches(1.4), c_w2, c_h2, "🛡️ Industrial Poka-Yoke Engineering", [
        "TQM Principle: Prevent human error at the source before defect propagation.",
        "Syntax Pattern Matching: Regex enforces standard Indian plate format (State + District + Series + Number).",
        "State Code Registry: Validates 14+ Indian States & UTs (UK, DL, UP, HR, MH, PB, RJ, KA, etc.).",
        "Strict RTO District Boundary Limits: Validates realistic transport office numbers per state.",
        "Automatic Capitalization & Normalization: Automatically transforms messy inputs ('uk04ak5521') into official standards ('UK-04-AK-5521')."
    ], C_AMBER)

    add_card(slide4, Inches(6.8), Inches(1.4), c_w2, c_h2, "🚫 The 'UK-87' Defect Rejection Case Study", [
        "The Defect: Operators entering invalid district numbers (e.g. 'UK-87-AK-1234').",
        "Physical Reality: Uttarakhand transport authority only has 20 districts (UK-01 Almora to UK-20 Ranikhet). UK-87 does not exist!",
        "Real-Time AJAX Interception: Debounced listener queries /api/validate-plate/ on keystroke in the check-in modal.",
        "Instant Educational Alert: Displays: 'Poka-Yoke Error Prevention: UK-87 is invalid. Uttarakhand RTO district codes strictly range from UK-01 to UK-20.'",
        "Multi-Tier Guard: Blocked both at client modal and at backend Django form clean() validation."
    ], C_GREEN)

    # ==========================================
    # SLIDE 5: MULTI-FLOOR CAR PARKING ARCHITECTURE
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Multi-Floor Car Parking Architecture (48 Bays)", "PHYSICAL FACILITY MODELLING")

    c_w4 = Inches(2.75)
    c_h4 = Inches(5.4)
    g4 = Inches(0.2)
    s4_x = Inches(0.8)

    add_card(slide5, s4_x, Inches(1.4), c_w4, c_h4, "⚡ Level B1: EV Hub", [
        "Basement Level B1",
        "12 Bays: B1-EV-01 to B1-EV-12",
        "Dedicated EV Smart Bays",
        "Equipped with 7.2 kW AC fast charging infrastructure.",
        "Real-time kWh energy telemetry.",
        "Non-EV vehicles programmatically blocked."
    ], C_GREEN)

    add_card(slide5, s4_x + (c_w4+g4), Inches(1.4), c_w4, c_h4, "🚗 Ground Floor (G)", [
        "Ground Ingress Level",
        "12 Bays: G-01 to G-12",
        "G-01 to G-06: Heavy SUV & Premium Bays.",
        "G-07 to G-12: Standard Sedans.",
        "Direct egress access to reduce turning circle congestion.",
        "Reinforced floor rating."
    ], C_BLUE)

    add_card(slide5, s4_x + (c_w4+g4)*2, Inches(1.4), c_w4, c_h4, "🚙 Level 1 (F1)", [
        "First Floor Level",
        "12 Bays: F1-01 to F1-12",
        "Standard Sedans & Hatchbacks.",
        "Optimized lane dimensions for rapid diagonal parking.",
        "Automated bay routing from gate entry.",
        "Clear level signage."
    ], C_NAVY)

    add_card(slide5, s4_x + (c_w4+g4)*3, Inches(1.4), c_w4, c_h4, "🛞 Level 2 (F2)", [
        "Covered Rooftop Level",
        "12 Bays: F2-01 to F2-12",
        "F2-01 to F2-06: Standard Sedans.",
        "F2-07 to F2-12: Compact City Cars.",
        "Overspill buffer level.",
        "Weatherproof canopy structure."
    ], C_MUTED)

    # ==========================================
    # SLIDE 6: EV CHARGING TELEMETRY & POS BILLING
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "EV Charging Infrastructure & Unified POS Billing", "CLEAN ENERGY INTEGRATION & BILLING")

    add_card(slide6, Inches(0.8), Inches(1.4), c_w2, c_h2, "⚡ Live EV Charging Telemetry", [
        "Virtual Smart Charger Hub: 7.2 kW AC charging protocol.",
        "Real-Time Telemetry: Tracks energy consumed (kWh), charging state (Idle, Charging, Completed).",
        "Dynamic Battery Gauge: Visual animated battery UI showing 35% -> 100% based on energy transferred.",
        "Driver Remote View: Customers track battery progress on smartphones via /customer/.",
        "Smart Tariff Config: Configurable per-kWh rate (default ₹15.00/kWh) in Manager Console."
    ], C_GREEN)

    add_card(slide6, Inches(6.8), Inches(1.4), c_w2, c_h2, "🧾 Unified POS Thermal Billing (receipt.html)", [
        "Dual Fee Composition: Total Bill = Base Parking Fee + EV Energy Charge.",
        "Daily Max Rate Protection: Automatic ₹250/day ceiling cap to prevent astronomical runaway bills.",
        "Authentic 80mm POS Thermal Receipt: Styled to mimic commercial EPSON/Star Micronics thermal printers (380px width).",
        "GST Compliance: Itemized parking charge, EV energy, and 18% included GST breakdown with facility GSTIN.",
        "Print Optimization: Dedicated @media print stylesheet stripping browser chrome for instant receipt printing."
    ], C_BLUE)

    # ==========================================
    # SLIDE 7: DATABASE SCHEMA & DATA MODELS
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Relational Database Schema & Data Models", "BACKEND ARCHITECTURE (DJANGO ORM)")

    c_w3 = Inches(3.7)
    c_h3 = Inches(5.4)
    g3 = Inches(0.3)
    s3_x = Inches(0.8)

    add_card(slide7, s3_x, Inches(1.4), c_w3, c_h3, "Floor & ParkingSlot", [
        "Floor Model:",
        "- floor_number (Int, -1 to 2)",
        "- code ('B1', 'G', 'F1', 'F2')",
        "- name, total_slots, is_ev_enabled",
        "- Properties: occupied_count, available_count, occupancy_pct",
        "ParkingSlot Model:",
        "- slot_number ('B1-EV-01', 'G-04')",
        "- floor (FK -> Floor)",
        "- slot_type, is_occupied, is_ev_bay"
    ], C_NAVY)

    add_card(slide7, s3_x + (c_w3+g3), Inches(1.4), c_w3, c_h3, "Vehicle & EV Session", [
        "Vehicle Model:",
        "- license_plate (RTO validated)",
        "- vehicle_type (Sedan, SUV, EV...)",
        "- slot (FK -> ParkingSlot)",
        "- entry_time, exit_time, status",
        "- parking_fee, ev_fee, fee (total)",
        "EVChargingSession Model:",
        "- vehicle (1-to-1 -> Vehicle)",
        "- slot (FK -> ParkingSlot)",
        "- status, energy_kwh, rate_per_kwh"
    ], C_BLUE)

    add_card(slide7, s3_x + (c_w3+g3)*2, Inches(1.4), c_w3, c_h3, "Incident & ProfileConfig", [
        "SecurityIncident Model:",
        "- reporter (Guard Name)",
        "- incident_type, license_plate",
        "- severity (Low, Med, High)",
        "- description, is_resolved, timestamp",
        "ProfileSettings Model:",
        "- facility_name, operator_name",
        "- hourly_rate, daily_max_rate",
        "- ev_rate_per_kwh, total_capacity"
    ], C_AMBER)

    # ==========================================
    # SLIDE 8: TQM ALIGNMENT & DEFENSE CRITERIA
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "TQM Principles & Academic Defense Alignment", "HOW THIS FULFILLS BBAT104 QUALITY GOALS")

    add_card(slide8, Inches(0.8), Inches(1.4), c_w2, c_h2, "🎯 Core Allotment & Quality Goal Q08", [
        "Digit 8 Allotment: Parking Management System.",
        "Baseline Objective: Minimize entry queues & maximize space utilization.",
        "Quality Goal Q08: Improve User Satisfaction & Usability.",
        "Zero Academic Toy Elements: Eliminated artificial SQC charts from the active app, replaced with real-world commercial analytics.",
        "Sub-10s Gate Ingress: Ergonomic keyboard shortcuts (Alt+N) and instant slot allotment clear queues rapidly.",
        "Ergonomic Dark/Light Theming: High-contrast themes reduce operator eye fatigue during 24/7 night shifts."
    ], C_BLUE)

    add_card(slide8, Inches(6.8), Inches(1.4), c_w2, c_h2, "🏆 Core TQM Philosophies Demonstrated", [
        "Poka-Yoke (Mistake-Proofing): Hard-rejection of non-existent RTO registrations (UK-87) prevents data corruption.",
        "Visual Management (Andon): Real-time green/red bay visualizer and floor heatmaps provide instant visual operational status.",
        "Fact-Based Decision Making: Operations Manager monitors exact revenue splits (parking vs EV energy) and floor capacity metrics.",
        "Continuous Improvement (Kaizen): Shifted from a student assignment prototype to a deployable enterprise platform.",
        "Customer Focus: Drivers locate cars instantly and view real-time battery percentages on mobile devices."
    ], C_GREEN)

    # ==========================================
    # SLIDE 9: VERIFICATION, TESTING & LIVE DEMO
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "System Verification & Live Demonstration Script", "PROOF OF PRODUCTION QUALITY")

    add_card(slide9, Inches(0.8), Inches(1.4), c_w2, c_h2, "✅ Automated Test Suite (9/9 Passing)", [
        "1. Poka-Yoke Validator: UK-87 rejected, UK-04 accepted.",
        "2. Unauthenticated Access Block: Internal consoles redirect.",
        "3. Guard RBAC Isolation: Guard strictly blocked from Admin/Manager.",
        "4. Admin Supervisory Access: Admin retains full system oversight.",
        "5. Credential Verification: Password validation checks authentication.",
        "6. Check-In Form Validation: Rejects invalid plates at form layer.",
        "7. Smart Bay Allocation: Auto-assigns optimal floor bays.",
        "8. EV Telemetry & Billing: Verifies dual fee calculation.",
        "9. Real-Time AJAX API: Instant keystroke plate validation."
    ], C_GREEN)

    add_card(slide9, Inches(6.8), Inches(1.4), c_w2, c_h2, "🎬 Step-by-Step Defense Walkthrough", [
        "Step 1: Open http://127.0.0.1:8000/ -> Show Auth Launchpad & 5 Persona Tiles.",
        "Step 2: Click 'Sign In as Operator' -> Authenticate with operator / operator123.",
        "Step 3: Press Alt+N -> Enter UK-87-AK-1234 -> Show immediate red Poka-Yoke alert! Change to UK-04-AK-5521 -> Show green valid badge.",
        "Step 4: Check out UK-04-EV-2024 -> Show 80mm thermal receipt with parking + EV power charge.",
        "Step 5: Sign out -> Sign in as Guard (guard / guard123) -> Try to open /admin-console/ in URL bar -> Show immediate 403 Access Denied block!",
        "Step 6: Show Customer Portal -> Search UK-04-EV-2024 -> Show live animated battery gauge."
    ], C_BLUE)

    # Save presentation
    output_path = r"F:\TQM\Parking_Management_System_tqm\ParkSmart_Pro_Enterprise_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    create_deck()
