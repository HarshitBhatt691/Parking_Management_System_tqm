import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Corporate Enterprise
    NAVY = RGBColor(15, 23, 42)        # Slate 900
    BLUE = RGBColor(37, 99, 235)       # Primary Blue
    WHITE = RGBColor(255, 255, 255)
    DARK_TEXT = RGBColor(30, 41, 59)   # Slate 800
    MUTED_TEXT = RGBColor(100, 116, 139) # Slate 500
    CARD_BG = RGBColor(248, 250, 252)  # Slate 50
    BORDER_COL = RGBColor(226, 232, 240)
    GREEN = RGBColor(16, 185, 129)     # Emerald
    WARNING = RGBColor(217, 119, 6)    # Amber
    RED = RGBColor(220, 38, 38)        # Crimson

    def add_header(slide, title_text, category_text="PARKSMART PRO ENTERPRISE"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COL):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🅿️ PARKSMART PRO ENTERPRISE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Commercial Multi-Level Car Parking Automation & EV Fast Charging Management System"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Production Architecture with Multi-Stakeholder Workstations, Poka-Yoke RTO Engine & Zero-Defect Governance"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_after = Pt(32)

    # Info card inside title
    add_card(s1, Inches(1.0), Inches(4.5), Inches(11.3), Inches(1.8), bg_color=RGBColor(30, 41, 59), border_color=BLUE)
    info_tb = s1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.9), Inches(1.6))
    itf = info_tb.text_frame
    itf.word_wrap = True

    ip1 = itf.paragraphs[0]
    ip1.text = "Presenter: Harshit Bhatt  |  Roll No: 2410302018  |  Branch: Computer Science & Engineering (CSE)"
    ip1.font.size = Pt(14)
    ip1.font.bold = True
    ip1.font.color.rgb = WHITE
    ip1.space_after = Pt(6)

    ip2 = itf.add_paragraph()
    ip2.text = "Course: BBAT104: Fundamentals of Total Quality Management (TQM)  |  Assigned Digit: 8 (Parking Management)"
    ip2.font.size = Pt(13)
    ip2.font.color.rgb = RGBColor(203, 213, 225)
    ip2.space_after = Pt(4)

    ip3 = itf.add_paragraph()
    ip3.text = "Quality Goal: Q08 - Improve User Satisfaction & Error Proofing  |  Institution: Amrapali University, Haldwani"
    ip3.font.size = Pt(13)
    ip3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Executive Vision & Industrial Transformation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Industrial Transformation: From Toy Prototype to Production SaaS")

    # Left Card: Traditional College Toy Project
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), bg_color=RGBColor(254, 242, 242), border_color=RED)
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    p = tf2_l.paragraphs[0]
    p.text = "❌ Rejected Prototype Pitfalls (Academic Toys)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RED
    p.space_after = Pt(12)

    flaws = [
        ("Static Retrospective SQC Charts", "Displays academic Pareto/Fishbone diagrams on live gate screens where cashiers need fast checkout tools."),
        ("Flat Single-Floor Slots", "Naive 20-slot flat lot disconnected from real multi-level commercial infrastructure."),
        ("Zero Role Isolation", "Single flat login where any guard or cashier can access executive administrative controls."),
        ("No Electric Vehicle Telemetry", "Lacks support for modern EV charging, power consumption tracking, and energy billing."),
        ("Vulnerable Data Entry", "Accepts fake license plates like 'UK-87' without validating real transport authority districts.")
    ]
    for h, b in flaws:
        p = tf2_l.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # Right Card: ParkSmart Pro Enterprise Solution
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), bg_color=RGBColor(240, 253, 244), border_color=GREEN)
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True
    p = tf2_r.paragraphs[0]
    p.text = "✅ ParkSmart Pro Enterprise Architecture"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(12)

    features = [
        ("Multi-Stakeholder Workstations", "5 distinct portals tailored specifically for Admin, Manager, Operator, Guard, and Customer."),
        ("4-Level Multi-Floor Infrastructure", "48 dedicated bays organized across Basement B1, Ground, F1, and Covered Rooftop F2."),
        ("Strict Role-Based Access Control (RBAC)", "Server-side @require_role protection with zero unauthorized cross-portal leakage."),
        ("7.2 kW EV Smart Charging Hub", "Real-time energy tracking (kWh), live battery progress gauge, and combined checkout billing."),
        ("Poka-Yoke Indian RTO Engine", "Keystroke AJAX validation that strictly rejects non-existent RTOs (e.g. UK-87 rejected).")
    ]
    for h, b in features:
        p = tf2_r.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Dedicated Stakeholder Architecture (USER REQUESTED DEDICATED SLIDE)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Comprehensive Stakeholder Architecture: 5 Specialized Workstations")

    stakeholders = [
        ("👑 Admin / Owner", "/admin-console/", "Complete Facility Governance", "User staff accounts, system diagnostics, gross revenue audits, database backups & re-seeding.", NAVY),
        ("💼 Operations Manager", "/manager/", "Commercial Operations & Tariffs", "Multi-floor capacity heatmaps, hourly parking tariffs, EV charging kWh pricing, and revenue analytics.", GREEN),
        ("🚗 Gate Operator / Cashier", "/operator/", "Fast Ingress & POS Checkout", "Sub-5s check-in with Alt+N, Poka-Yoke RTO verification, smart bay allocation, and POS thermal receipts.", BLUE),
        ("🛡️ Security Guard", "/security/", "Access Control & Patrol Dispatch", "Remote boom barrier overrides (Ingress/Egress), live plate scanner lookup, and security incident dispatch.", WARNING),
        ("🚙 Customer / Driver", "/customer/", "Driver Self-Service Station", "'Find My Car' bay locator, live floor vacancy explorer, real-time EV battery progress gauge, and e-receipts.", RGBColor(8, 145, 178))
    ]

    card_width = Inches(2.26)
    gap = Inches(0.18)
    start_left = Inches(0.8)

    for i, (role, route, scope, desc, color) in enumerate(stakeholders):
        l = start_left + i * (card_width + gap)
        add_card(s3, l, Inches(1.6), card_width, Inches(5.2), bg_color=CARD_BG, border_color=color)

        tb = s3.shapes.add_textbox(l + Inches(0.12), Inches(1.75), card_width - Inches(0.24), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = role
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = route
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = MUTED_TEXT
        p.space_after = Pt(10)

        p = tf.add_paragraph()
        p.text = "Scope:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT

        p = tf.add_paragraph()
        p.text = scope
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(10)

        p = tf.add_paragraph()
        p.text = "Operational Tools:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_TEXT

    # =========================================================================
    # SLIDE 4: Strict Role-Based Access Control (RBAC) & Security Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Strict Role-Based Access Control (RBAC) & Authentication Security")

    # 3 Horizontal Cards
    card_h_width = Inches(3.64)
    c_gap = Inches(0.38)

    # Card 1: The Vulnerability & Solution
    add_card(s4, Inches(0.8), Inches(1.6), card_h_width, Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(0.95), Inches(1.75), card_h_width - Inches(0.3), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🛡️ 1. Why Role Isolation Matters"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(10)

    points1 = [
        "Elimination of Auth Bypasses: In casual setups, any guard can view sensitive revenue figures.",
        "Zero-Trust Policy: Every URL endpoint is protected by a server-side @require_role decorator.",
        "Guards Locked to Patrol: If a Security Guard attempts to open /admin-console/ or /manager/, the request is intercepted.",
        "Immediate 403 Response: Guard is shown 'Access Denied: Required Role: ADMIN' and bounced back to /security/."
    ]
    for pt in points1:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # Card 2: Interactive Modal Auth
    add_card(s4, Inches(0.8) + card_h_width + c_gap, Inches(1.6), card_h_width, Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(0.95) + card_h_width + c_gap, Inches(1.75), card_h_width - Inches(0.3), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🔐 2. Modal Credential Verification"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(10)

    points2 = [
        "Card-Triggered Auth: Clicking any stakeholder card on the landing page opens an authentication modal.",
        "Role Pre-Configuration: Modal dynamically adapts to selected role (Admin, Manager, Operator, Guard).",
        "Mandatory Password Entry: Users must provide the verified password (e.g. admin123, guard123).",
        "Safe Demo Validation: Demo keys are displayed cleanly for evaluator transparency without compromising security."
    ]
    for pt in points2:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # Card 3: Context-Aware Dynamic Navbar
    add_card(s4, Inches(0.8) + 2 * (card_h_width + c_gap), Inches(1.6), card_h_width, Inches(5.2))
    tb = s4.shapes.add_textbox(Inches(0.95) + 2 * (card_h_width + c_gap), Inches(1.75), card_h_width - Inches(0.3), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧭 3. Context-Aware Navbar"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(10)

    points3 = [
        "Dynamic Template Processors: auth_role_context determines active user permissions globally.",
        "Unauthenticated Visitors: See zero internal workstation links (Driver portal only).",
        "Guard Navbar Isolation: Displays ONLY Security Gate Console & Plate Lookup.",
        "Explicit Sign-Out Action: Switching roles requires formal sign-out and re-authentication with target credentials."
    ]
    for pt in points3:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: Multi-Floor Car Parking Architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Multi-Floor Car Parking Architecture: 4-Level Physical Facility (48 Bays)")

    floors = [
        ("Level 2 (F2) - Covered Rooftop Deck", "12 Dedicated Bays: F2-01 to F2-12", "Standard Sedans (F2-01 to F2-06) & Compact City Cars (F2-07 to F2-12)", RGBColor(100, 116, 139)),
        ("Level 1 (F1) - Mid-Level Car Deck", "12 Dedicated Bays: F1-01 to F1-12", "Standard City Sedans, Compacts & Family Hatchbacks", BLUE),
        ("Ground Floor (G) - Primary Ingress Deck", "12 Dedicated Bays: G-01 to G-12", "Heavy SUV & Premium Bays (G-01 to G-06) + Standard Sedans (G-07 to G-12)", NAVY),
        ("Basement (B1) - EV Fast Charging Hub", "12 Dedicated Smart Bays: B1-EV-01 to B1-EV-12", "100% Dedicated to Electric Vehicles equipped with 7.2 kW AC Smart Chargers", GREEN)
    ]

    for i, (name, bays, vehicles, color) in enumerate(floors):
        top_y = Inches(1.6) + i * Inches(1.3)
        add_card(s5, Inches(0.8), top_y, Inches(11.73), Inches(1.15), bg_color=CARD_BG, border_color=color)

        tb = s5.shapes.add_textbox(Inches(1.0), top_y + Inches(0.08), Inches(11.3), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = f"Allocation: {bays}   |   Vehicle Suitability: {vehicles}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6: EV Charging Infrastructure & Unified Billing
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Electric Vehicle (EV) Fast Charging Infrastructure & Combined Billing")

    # Left: EV Telemetry & Features
    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚡ 7.2 kW EV Smart Charging Hub"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(12)

    ev_pts = [
        "Basement B1 EV Fast Bays: 12 dedicated bays equipped with virtual AC chargers.",
        "Real-Time Charging Telemetry: Real-time state machine ('Idle' -> 'Charging' -> 'Completed').",
        "Energy Metering (kWh): Formulaic consumption tracking based on charging duration.",
        "Animated Visual Battery Gauge: Real-time UI progress bar indicating 35% to 100% full.",
        "Non-EV Protection: Poka-Yoke rule blocks combustion vehicles from taking EV bays."
    ]
    for pt in ev_pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # Right: Formula & Thermal POS Receipt
    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧾 Unified Checkout & POS Thermal Invoice"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(12)

    bill_pts = [
        "Unified Billing Formula: Total Invoice = Parking Fee + EV Energy Charge",
        "Parking Fee Calculation: (Days * Daily Cap [₹250]) + min(Daily Cap, Hours * ₹30/hr)",
        "EV Energy Sales: kWh Delivered * EV Tariff Rate (default ₹15/kWh)",
        "Commercial 80mm Thermal Receipt: Formatted for POS thermal printers with GSTIN, duration breakdown, and simulated barcode.",
        "Driver E-Receipt Download: Accessible directly on driver smartphones via the customer portal."
    ]
    for pt in bill_pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: Poka-Yoke Indian RTO Validation Engine
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Industrial Poka-Yoke (Mistake-Proofing): Indian RTO Engine")

    # Left: Concept & Engine
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🛡️ Poka-Yoke Quality Principle"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(12)

    poka_pts = [
        "Core TQM Definition: 'Mistake-Proofing' mechanisms designed to make human error physically impossible.",
        "Problem: Gate operators frequently mistype license plates, corrupting audit logs and causing lost tickets.",
        "3-Tier Verification Engine (rto_validator.py):",
        "  1. Syntax Regex Parsing: Validates standard Indian plate structure.",
        "  2. State Code Verification: Recognizes official Indian state codes (UK, DL, UP, HR, MH, etc.).",
        "  3. District Boundary Enforcement: Validates district limits per state authority."
    ]
    for pt in poka_pts:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(6)

    # Right: Real-World Case Study (UK-87 vs UK-04)
    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 Real-World Case Study: UK-87 Rejection"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    cases = [
        ("❌ Invalid Plate (UK-87-AK-1234)", "Uttarakhand only has 20 registered RTO districts (UK-01 Almora to UK-20 Ranikhet). UK-87 is non-existent. The system immediately rejects entry with a Poka-Yoke error alert.", RED),
        ("✅ Valid Plate (uk04ak5521)", "Recognized as Uttarakhand (Nainital / Haldwani RTO). System accepts plate and normalizes formatting to UK-04-AK-5521.", GREEN),
        ("⚡ Real-Time Keystroke AJAX Feedback", "Operator receives instant visual confirmation via /api/validate-plate/ as they type into the check-in modal.", BLUE)
    ]
    for title, desc, col in cases:
        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT
        p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: Gate Operator Workstation & Ingress Flow
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Gate Operator Workstation: High-Speed Vehicle Ingress & Checkout")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🚗 Gate Operator / Cashier Workflow & Ergonomics"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(14)

    op_points = [
        ("Sub-5 Second Ingress (Alt+N)", "Operators open the check-in modal instantly via global keyboard hotkey without touching the mouse, minimizing vehicle queues during rush hour."),
        ("Interactive Multi-Floor Bay Map", "Live color-shifting bay visualizer tabbed across B1, Ground, F1, and F2 with real-time sensor occupancy (Green = Vacant, Red = Occupied, Cyan = EV Charging)."),
        ("Smart Automatic Slot Routing", "Automatic floor and bay assignment routing heavy SUVs to Ground floor and electric vehicles directly to Basement B1 EV bays."),
        ("Active Parked Fleet Register", "Comprehensive data table with vehicle license plate, category, assigned bay & floor, entry timestamp, parked duration, and EV battery telemetry."),
        ("Instant POS Billing & Egress Checkout", "1-Click checkout executing formulaic billing, releasing the bay, updating the multi-floor sensor state, and generating the printable 80mm GST receipt.")
    ]
    for h, b in op_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 9: Driver Customer Self-Service Portal
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Driver Self-Service Portal: 'Find My Car' & Live EV Battery Gauge")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🚙 Customer Driver Self-Service (/customer/)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(8, 145, 178)
    p.space_after = Pt(14)

    cust_points = [
        ("Mobile-Friendly 'Find My Car' Search", "Drivers type their license plate into a responsive search bar on their smartphones upon returning to the facility."),
        ("Wayfinding & Bay Directions", "System returns exact floor location and assigned bay code (e.g. 'Basement Level B1, Bay B1-EV-01') with pedestrian navigation instructions."),
        ("Live EV Battery Charging Telemetry", "Custom animated CSS battery gauge displays real-time charging status, current battery percentage (e.g. 78% Charged), and kWh power delivered."),
        ("Public Multi-Floor Vacancy Explorer", "Arriving drivers can inspect live vacancies across all 4 building levels before pulling up to the ingress barrier."),
        ("Downloadable Digital Tax Invoice", "Drivers can view, download, or reprint their digital tax invoice directly from their mobile devices.")
    ]
    for h, b in cust_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 10: Security Guard Console & Perimeter Control
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Security Guard Console: Remote Barriers & Incident Dispatch")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🛡️ Security Guard Station & Perimeter Oversight (/security/)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WARNING
    p.space_after = Pt(14)

    sec_points = [
        ("Remote Boom Barrier Actuators", "Software override toggles for North Ingress and South Egress boom barriers (Raised/Lowered states with session persistence)."),
        ("Guard License Plate Scanner Lookup", "Security guards can verify any arriving plate against the active lot database to distinguish authorized parked cars from unregistered visitors."),
        ("RTO Authority Verification", "Visitor plates undergo instant RTO verification to identify counterfeit or non-existent vehicle plates at the security checkpoint."),
        ("Incident Logging & Dispatch Form", "Standardized reporting form for security incidents (Unauthorized parking, blocked lanes, barrier sensor delays) with severity levels (Low, Medium, High)."),
        ("Live Security Incident Feed", "Real-time incident audit stream with one-click resolution dispatch for on-duty patrol guards.")
    ]
    for h, b in sec_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: Operations Manager & Executive Analytics
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Operations Manager Console: Tariffs & Commercial Analytics")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "💼 Operations Manager & Financial Analytics (/manager/)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(14)

    mgr_points = [
        ("Revenue Stream Separation", "Real-time auditing separating base parking revenue from EV fast charging power sales."),
        ("Multi-Floor Capacity Heatmaps", "Live utilization progress bars across Basement B1, Ground, F1, and F2 with chromatic warnings (>85% capacity highlighted in red)."),
        ("Dynamic Tariff & Pricing Controls", "Inline configuration form allowing managers to adjust hourly parking rates (₹30/hr), daily ceiling caps (₹250/day), and EV power tariffs (₹15/kWh)."),
        ("Turnover Audit Stream", "Real-time log of departing vehicles, billed durations, and collected fees for cashflow auditing."),
        ("Facility Operational Configuration", "Facility operating name, supervisor in-charge, and customer support contact email settings.")
    ]
    for h, b in mgr_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: Admin / Owner Console & Facility Diagnostics
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Admin / Owner Console: System Governance & Data Integrity")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "👑 System Administrator & Executive Governance (/admin-console/)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    adm_points = [
        ("System Diagnostics & Health Metrics", "Live diagnostic counters tracking active staff users, 48 multi-floor bays, vehicle ledger records, and security logs."),
        ("Enterprise Staff Credentials Directory", "Comprehensive registry of registered users, roles, staff/superuser flags, and direct workstation launch buttons."),
        ("1-Click Demo Re-Seed Engine (/api/reset-seed/)", "Integrated administrative tool that re-seeds realistic multi-floor cars, EV charging sessions, and security logs for flawless demonstrations."),
        ("Direct Django Superuser Bridge", "Direct access to the underlying Django Admin ORM portal (/admin/) for database maintenance."),
        ("Full Superuser Authority", "Administrative privileges granting supervisory access across all 5 operational workstations.")
    ]
    for h, b in adm_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 13: Mapping to Total Quality Management (TQM) Principles
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Rigorous Alignment with Core TQM Principles")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "📐 TQM Principles Embedded in Operational Code"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(14)

    tqm_mappings = [
        ("Poka-Yoke (Mistake-Proofing)", "Zero-defect entry: Invalid RTO codes (e.g. UK-87) and non-EV cars attempting to book EV bays are programmatically blocked at source."),
        ("Visual Management (Andon)", "Real-time color-coded multi-floor bay visualizer, live EV battery percentage gauges, barrier state indicators, and occupancy threshold heatmaps."),
        ("Just-In-Time (JIT) Flow", "Sub-5 second hotkey check-in (Alt+N) and automated bay allocation eliminate gate queue bottlenecks during peak ingress."),
        ("Continuous Improvement (Kaizen)", "Iterative architectural evolution from a toy student script to an enterprise multi-stakeholder operations platform."),
        ("Customer Satisfaction Focus (Q08)", "Transparent duration billing, daily maximum price ceilings, driver self-service car locator, and thermal POS receipts.")
    ]
    for h, b in tqm_mappings:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 14: Technology Stack & Architectural Robustness
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Enterprise Technology Stack & Architectural Robustness")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "💻 Technical Architecture & Production Standards"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    tech_points = [
        ("Backend Framework", "Python 3.11 with Django 5.x following the MVC/MVT architectural pattern with clean separation of concerns."),
        ("Relational Database", "SQLite3 with relational foreign keys (Floor -> ParkingSlot -> Vehicle -> EVChargingSession) and ACID compliance."),
        ("Zero External Frontend Bloat", "Bootstrap 5.3 + Bootstrap Icons + Custom CSS3 animations (Fast rendering, zero node_modules or build-step overhead)."),
        ("Ergonomics & Accessibility", "Persistent Dark/Light theme toggle (Alt+T) stored in LocalStorage, plus operator keyboard shortcuts (Alt+N, Alt+D, Alt+Y, Alt+C, Alt+H)."),
        ("Version Control Discipline", "Progressive Git history with 40+ clean descriptive commits documenting the architectural evolution.")
    ]
    for h, b in tech_points:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 15: Verification & Automated Test Suite Results
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Verification: Automated Test Suite (100% Pass Rate)")

    add_card(s15, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s15.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🧪 9 Automated Unit Test Cases (core_parking_system_app1/tests.py)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(14)

    tests = [
        ("test_poka_yoke_rto_validator", "Verifies strict rejection of UK-87 and normalization of UK-04."),
        ("test_unauthenticated_workstation_access_blocked", "Verifies all internal terminals require authentication."),
        ("test_guard_cannot_access_admin_or_manager", "Proves a Guard account is strictly blocked from Admin/Manager portals with a 403 alert."),
        ("test_admin_supervisory_access", "Verifies Admin executive privileges across all facility terminals."),
        ("test_credential_authentication_flow", "Verifies password verification (wrong password rejected, valid password logged in)."),
        ("test_poka_yoke_check_in_rejection_in_form", "Verifies operator check-in form blocks invalid RTO plates."),
        ("test_valid_check_in_and_smart_slot_allocation", "Verifies automatic bay allocation across floors."),
        ("test_ev_fast_charging_and_billing", "Verifies EV charging sessions and combined checkout billing math."),
        ("test_api_validate_plate", "Verifies real-time keystroke AJAX validation endpoint.")
    ]
    for name, desc in tests:
        p = tf.add_paragraph()
        p.text = f"• {name}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        p.space_after = Pt(5)

    p = tf.add_paragraph()
    p.text = "Execution Result: Ran 9 tests in 7.194s — OK (0 Failures, 0 Errors)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GREEN

    # =========================================================================
    # SLIDE 16: Live Demonstration Roadmap (For Professor)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "5-Minute Live Demonstration Roadmap")

    add_card(s16, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s16.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🎯 Step-by-Step Demonstration Flow for Professor Evaluation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(14)

    steps = [
        ("Step 1: Landing Page (/)", "Demonstrate the 5 stakeholder cards and the authentication modal requiring passwords."),
        ("Step 2: Security Guard Isolation (/security/)", "Log in as guard (guard123). Show barrier overrides. Try navigating to /admin-console/ in the URL bar -> show immediate 403 Access Denied alert!"),
        ("Step 3: Operator Poka-Yoke Check-In (/operator/)", "Log in as operator (operator123). Press Alt+N. Type UK-87-AK-1234 -> observe instant red Poka-Yoke rejection! Type UK-04-AK-5521 -> observe green acceptance & auto-allocation!"),
        ("Step 4: EV Charging & Unified Billing", "Check in an EV -> allocated to Basement B1 EV bay. Click 'Checkout' on active EV -> show itemized 80mm thermal receipt combining parking fee + EV power charge."),
        ("Step 5: Customer Portal (/customer/)", "Search UK-04-EV-2024 -> observe live animated battery charging gauge and bay wayfinding directions."),
        ("Step 6: Manager Console (/manager/)", "Inspect multi-floor capacity heatmaps and adjust facility tariff rates live.")
    ]
    for h, b in steps:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b
        run.font.bold = False
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 17: Anticipated Viva / Defense Q&A
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Anticipated Viva / Defense Questions & Answers")

    add_card(s17, Inches(0.8), Inches(1.6), Inches(11.73), Inches(5.2))
    tb = s17.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🎓 Bulletproof Defense Answers for Critical Evaluation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    qa = [
        ("Q: Why did you remove traditional Pareto and Fishbone charts from the web app?",
         "A: Pareto charts are retrospective historical audit tools, not real-time facility operations software. Commercial platforms (like FlashParking or TIBA) do not display academic charts to gate cashiers. Instead, we applied TQM proactively through Poka-Yoke error prevention, real-time visual Andon controls, and multi-tenant security."),
        ("Q: What is Poka-Yoke, and where is it implemented in your code?",
         "A: Poka-Yoke is mistake-proofing to achieve zero defects. It is implemented in rto_validator.py. It inspects Indian state registration boundaries. For example, Uttarakhand only has 20 official RTO districts (UK-01 to UK-20). If an operator enters UK-87, the system rejects it at both keystroke AJAX and form validation layers, preventing corrupted data from entering the database."),
        ("Q: How do you prevent a Security Guard from accessing the Admin or Manager workstation?",
         "A: We implemented Role-Based Access Control (RBAC) at two layers. At the backend, our custom @require_role decorator intercepts unauthorized requests, issues a 403 security warning, and redirects the user to their authorized home workstation. At the UI layer, our context processor dynamically filters navbar links so that cross-role terminals are not even rendered in the Guard's browser."),
        ("Q: How does the EV charging integration affect billing?",
         "A: Level B1 has 12 dedicated EV smart charging bays. When an EV checks out, the system combines the base parking fee (calculated with hourly rates and a daily maximum cap of ₹250) with the energy consumed (kWh delivered multiplied by the ₹15/kWh tariff), producing an itemized 80mm thermal POS tax invoice.")
    ]
    for q, a in qa:
        p = tf.add_paragraph()
        p.text = q
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = BLUE
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.size = Pt(10)
        p2.font.color.rgb = DARK_TEXT
        p2.space_after = Pt(6)

    output_path = "F:/TQM/Parking_Management_System_tqm/ParkSmart_Pro_Enterprise_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    create_deck()
