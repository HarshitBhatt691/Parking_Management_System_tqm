import sys
import pptx
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
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_BLUE = RGBColor(37, 99, 235)      # #2563EB
    C_LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK = RGBColor(30, 41, 59)       # #1E293B
    C_MUTED = RGBColor(100, 116, 139)   # #64748B
    C_GREEN = RGBColor(16, 185, 129)    # #10B981
    C_AMBER = RGBColor(245, 158, 11)    # #F59E0B
    C_RED = RGBColor(239, 68, 68)       # #EF4444
    C_CARD_BG = RGBColor(255, 255, 255)
    C_BORDER = RGBColor(226, 232, 240)  # #E2E8F0

    def add_bg(slide, color=C_LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, dark_mode=False):
        # Category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = RGBColor(96, 165, 250) if dark_mode else C_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE if dark_mode else C_NAVY

    def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Hero Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, C_NAVY)

    # Accent glow top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.2), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_BLUE
    bar.line.fill.background()

    # Category Tag
    tag = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11), Inches(0.4))
    p = tag.text_frame.paragraphs[0]
    p.text = "BBAT104: FUNDAMENTALS OF TOTAL QUALITY MANAGEMENT (TQM) | DIGIT 8 ALLOTMENT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)

    # Main Project Title
    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.8))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "ParkSmart Pro Enterprise"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Commercial Multi-Level Car Parking Automation & EV Fast Charging Management System"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = RGBColor(203, 213, 225)
    p1_sub.space_before = Pt(10)

    # Info Cards at Bottom
    details = [
        ("Presenter & Roll Number", "Harshit Bhatt\nRoll No: 2410302018 (Digit 8)"),
        ("Branch & Academic Target", "CSE [AI & ML]\nQuality Goal: Q08 (User Satisfaction)"),
        ("Key Commercial Features", "5 Stakeholder Portals • 4-Floor Car Bays\n7.2kW EV Hub • Poka-Yoke RTO Engine"),
        ("Institution & Session", "Amrapali University, Haldwani\nAcademic Session: 2026–27"),
    ]
    for idx, (head, val) in enumerate(details):
        x = Inches(0.8 + idx * 2.95)
        add_card(s1, x, Inches(4.3), Inches(2.8), Inches(2.4), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
        tb = s1.shapes.add_textbox(x + Inches(0.15), Inches(4.45), Inches(2.5), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head.upper()
        p_h.font.size = Pt(10)
        p_h.font.bold = True
        p_h.font.color.rgb = RGBColor(96, 165, 250)
        
        p_v = tf.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(13)
        p_v.font.color.rgb = C_WHITE
        p_v.space_before = Pt(8)

    # =========================================================================
    # SLIDE 2: Problem Statement & Industrial Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Industrial Context & Baseline Challenges", "Why Academic Toy Parking Systems Fail in Commercial Operations")

    points_s2 = [
        ("Gate Ingress Bottlenecks", "Manual ticketing, plate handwriting, and payment delays cause 8–15 car queues, spilling onto access highways.", C_RED, "bi-shield-x"),
        ("Flat vs Multi-Floor Vacuum", "Real-world parking facilities span multiple levels (Basement, Ground, Rooftop); single-floor flat models fail completely.", C_AMBER, "bi-layers"),
        ("Unregulated EV Influx", "Electric Vehicles require specialized charging bays with power telemetry and unified parking + energy billing.", C_BLUE, "bi-lightning-charge"),
        ("Human Data Entry Typos", "Operators entering non-existent plates (e.g. 'UK-87') corrupt registries without Poka-Yoke validation rules.", C_NAVY, "bi-exclamation-triangle"),
    ]
    for idx, (head, desc, col, icon) in enumerate(points_s2):
        x = Inches(0.8 + idx * 2.95)
        add_card(s2, x, Inches(1.8), Inches(2.8), Inches(4.8))
        # Top color strip
        strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = col
        strip.line.fill.background()

        tb = s2.shapes.add_textbox(x + Inches(0.2), Inches(2.2), Inches(2.4), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"0{idx+1}. {head}"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_MUTED
        p2.space_before = Pt(14)

    # =========================================================================
    # SLIDE 3: Quality Objectives Aligned with TQM Principles
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Total Quality Management (TQM) Alignment", "Quality Target Q08: Maximizing Usability & Operational Satisfaction")

    tqm_pillars = [
        ("Poka-Yoke Zero Defects", "Shigeo Shingo Principle: Real-time client & server validation strictly blocking non-existent RTO district codes (e.g. UK-87 rejected; UK-04 Haldwani accepted)."),
        ("Role Segregation (ISO 9001)", "Distinct, secure workstations for 5 stakeholders with zero unauthorized privilege crossover; guards cannot access admin consoles."),
        ("Visual Management (Andon)", "Live 4-floor bay occupancy visualizer, capacity heatmaps, animated EV battery charging gauges, and barrier status actuators."),
        ("Deming PDCA Kaizen Cycle", "Plan-Do-Check-Act continuous governance: monitoring ingress clearance (sub-10s gate clearance) and automated daily cap billing (₹250/day max)."),
    ]
    for idx, (title, desc) in enumerate(tqm_pillars):
        y = Inches(1.8 + idx * 1.25)
        add_card(s3, Inches(0.8), y, Inches(11.7), Inches(1.1))
        # Accent bar
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = s3.shapes.add_textbox(Inches(1.2), y + Inches(0.15), Inches(11.1), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_MUTED
        p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: System Architecture & Modern Tech Stack
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Engineering Blueprint", "Full-Stack Enterprise Architecture & Technology Stack")

    stack_cards = [
        ("Backend Framework", "Django 5.x + Python 3.11\n• Strict MVT Architecture\n• Custom @require_role RBAC Decorator\n• RESTful AJAX Validation Endpoints", C_NAVY),
        ("Relational Database", "SQLite3 (ACID Compliant)\n• 7 Relational Models\n• Cascade & Set-Null Constraints\n• Atomic Fee & Session Transactions", C_BLUE),
        ("Poka-Yoke Validation Layer", "rto_validator.py Engine\n• Regex Indian Plate Normalization\n• 14+ State/UT District Range Tables\n• Real-time Debounced Keystroke AJAX", C_GREEN),
        ("Presentation & UX", "Bootstrap 5.3 + Responsive Grid\n• Dynamic Role-Based Navbar\n• Google Plus Jakarta Sans & JetBrains Mono\n• Dual Dark/Light Persistent Theme", C_AMBER),
    ]
    for idx, (head, desc, col) in enumerate(stack_cards):
        x = Inches(0.8 + idx * 2.95)
        add_card(s4, x, Inches(1.8), Inches(2.8), Inches(4.8))
        strip = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = col
        strip.line.fill.background()

        tb = s4.shapes.add_textbox(x + Inches(0.2), Inches(2.1), Inches(2.4), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_DARK
        p2.space_before = Pt(12)

    # =========================================================================
    # SLIDE 5: The 5 Stakeholder Workstations Ecosystem
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Multi-Tenant Operational Ecosystem", "Dedicated Stakeholder Portals with Strict Role Isolation")

    roles = [
        ("👑 Admin / Owner", "/admin-console/", "System Administration", "Staff user accounts, global facility parameters, database health diagnostics, gross revenue audit, and SQLite demo re-seeder.", C_NAVY),
        ("💼 Operations Manager", "/manager/", "Facility & Financial Oversight", "Multi-floor capacity heatmaps, hourly parking tariffs, EV charging kWh pricing, and revenue breakdown analytics.", C_GREEN),
        ("🚗 Gate Operator / Cashier", "/operator/", "Ingress & POS Cashier Terminal", "High-speed check-in (Alt+N) with Poka-Yoke RTO verification, smart bay allocation, checkout billing, and 80mm thermal receipt.", C_BLUE),
        ("🛡️ Security Guard", "/security/", "Gate Barrier Access & Patrol", "Simulated Ingress/Egress boom barrier actuators, live plate scanner lookup, security incident dispatch, and resolution feed.", C_AMBER),
        ("🚙 Customer / Driver", "/customer/", "Public Driver Self-Service", "'Find My Car' locator, bay walking directions, live floor vacancy explorer, real-time EV battery gauge, and e-receipt download.", RGBColor(6, 182, 212)),
    ]
    for idx, (title, url, scope, desc, col) in enumerate(roles):
        x = Inches(0.8 + idx * 2.38)
        add_card(s5, x, Inches(1.8), Inches(2.25), Inches(4.8))
        strip = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.25), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = col
        strip.line.fill.background()

        tb = s5.shapes.add_textbox(x + Inches(0.15), Inches(2.1), Inches(1.95), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

        p_u = tf.add_paragraph()
        p_u.text = url
        p_u.font.size = Pt(10)
        p_u.font.bold = True
        p_u.font.color.rgb = col
        p_u.space_before = Pt(4)

        p_s = tf.add_paragraph()
        p_s.text = scope
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = C_DARK
        p_s.font.bold = True
        p_s.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_MUTED
        p_d.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: Stakeholder 1 — Admin / Owner Console
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Stakeholder Deep-Dive 1 / 5", "👑 Admin / Owner Console — Executive Governance & Health HQ")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s6.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Executive Capabilities & Governance Scope"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s6 = [
        "Global Facility Configuration: Full control over commercial facility name, supervisor assignment, and support email.",
        "Enterprise Staff Directory: High-level view of all registered stakeholder accounts (Admin, Manager, Operator, Guard, Customer) and permissions.",
        "System Health & Telemetry Counters: Live counters for total registered users, active vehicle records, 48 slots, and security logs.",
        "Direct Superuser Admin Link: One-click shortcut into the core Django Superuser Admin portal (/admin/).",
        "Database Maintenance & Demo Seeder: Built-in tool to purge and re-seed clean commercial demo datasets (/api/reset-seed/).",
    ]
    for b in bullets_s6:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(10)

    # Right side Mock / Card
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), C_NAVY, RGBColor(51, 65, 85))
    tb_r = s6.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "ADMIN DIAGNOSTICS & CONTROLS (/admin-console/)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = RGBColor(96, 165, 250)

    admin_metrics = [
        ("Active Staff Users", "6 Accounts Registered (RBAC Isolated)"),
        ("Multi-Floor Bays", "48 Managed Slots across B1, G, F1, F2"),
        ("Vehicle Ledger Count", "45 Active + Historical Parking Records"),
        ("Security Log Entries", "4 Dispatched & Resolved Patrol Reports"),
        ("Security Clearance", "Strictly Protected by @require_role(['admin'])"),
    ]
    for title, val in admin_metrics:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_WHITE
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: Stakeholder 2 — Operations Manager Console
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Stakeholder Deep-Dive 2 / 5", "💼 Operations Manager Console — Financial Analytics & Tariff Control")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s7.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Commercial Oversight & Rate Management"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s7 = [
        "Separated Revenue Accounting: Automatically distinguishes base parking turnover from EV power sales.",
        "Multi-Floor Capacity Heatmaps: Visual progress bars tracking occupancy on B1 (EV), Ground (SUV), F1, and F2 with automatic warning thresholds (>85% switches to red).",
        "Dynamic Tariff & Pricing Control: Inline configuration form to adjust hourly rates (₹30.00/hr), daily max ceiling caps (₹250.00/day), and EV charging rates (₹15.00/kWh).",
        "Recent Exit Cashflow Turnover: Real-time departing vehicle turnover stream with itemized duration and invoice summaries.",
    ]
    for b in bullets_s7:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(10)

    # Right side Financial telemetry cards
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s7.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "FINANCIAL & CAPACITY TELEMETRY (/manager/)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_GREEN

    kpis = [
        ("Gross Facility Revenue", "₹13,440.00 (Aggregated Parking + EV Sales)"),
        ("EV Fast Charging Revenue", "₹2,025.00 (Power Delivered: 135.0 kWh)"),
        ("Active EV Chargers Running", "3 Chargers Active in B1 Fast Hub"),
        ("Current Facility Load", "25% Occupancy (12 / 48 Bays In Use)"),
        ("Access Authorization", "Restricted to Managers & Admin (@require_role)"),
    ]
    for title, val in kpis:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 8: Stakeholder 3 — Gate Operator / Cashier Terminal
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Stakeholder Deep-Dive 3 / 5", "🚗 Gate Operator / Cashier Terminal — Ingress & POS Cashier Station")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "High-Speed Ingress & Checkout Capabilities"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s8 = [
        "Multi-Floor Visual Grid: Tabbed 4-floor bay layout (B1, G, F1, F2) showing vacant (green), occupied (red), and EV active charging bays.",
        "Poka-Yoke Check-In Modal (Alt+N): Sub-second entry modal with real-time keystroke RTO validation and automatic slot routing.",
        "Smart Floor Routing: Arriving EVs are automatically routed to Level B1 EV bays; SUVs to Ground floor; standard cars across F1/F2.",
        "Instant Checkout & Billing: One-click departure checkout computing billed duration, daily cap protection, and EV energy fees.",
        "Thermal 80mm GST Invoice: Generates clean, print-ready POS receipts with barcode and itemized parking + EV power charges.",
    ]
    for b in bullets_s8:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(10)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s8.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "OPERATOR TERMINAL FEATURES (/operator/)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_BLUE

    op_points = [
        ("Sub-10s Gate Ingress", "Hotkey Alt+N opens entry dialog instantly; zero mouse delay"),
        ("Live EV Bay Telemetry", "In-bay battery % progress bar and live power transfer meter"),
        ("Poka-Yoke RTO Protection", "Invalid plates (e.g. UK-87) immediately blocked with error"),
        ("Active Fleet Register", "Searchable tabular registry with instant Exit, Edit, and Void tools"),
        ("Zero Spillover Queues", "Real-time vacancy indicator prevents cars entering full lots"),
    ]
    for title, val in op_points:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: Stakeholder 4 — Security Guard Console
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Stakeholder Deep-Dive 4 / 5", "🛡️ Security Guard Console — Boom Barrier Controls & Gate Patrol")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s9.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Perimeter Security & Incident Management"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s9 = [
        "Remote Boom Barrier Actuators: Manual override switches to Raise/Lower North Ingress and South Egress boom barriers with session state persistence.",
        "ANPR Guard Plate Scanner: Instant plate search verifying if an approaching car is actively registered, its assigned bay, or an unauthorized visitor.",
        "Security Incident Dispatch: Digital incident logging form categorizing issues (Unauthorized Parking, Blocked Lane, Suspicious Car, Barrier Issue).",
        "Live Incident Stream & Resolution: Real-time incident feed with High/Med/Low severity badges and one-click 'Resolve' action.",
        "Strict Role Isolation: Security guards are restricted strictly to /security/ and cannot access Operator, Manager, or Admin consoles.",
    ]
    for b in bullets_s9:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(10)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s9.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "GUARD CONSOLE CAPABILITIES (/security/)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_AMBER

    guard_points = [
        ("North Ingress Barrier", "Session-controlled actuator (OPEN / CLOSED states)"),
        ("South Egress Barrier", "Session-controlled actuator (OPEN / CLOSED states)"),
        ("Plate Authenticity Check", "Verifies state RTO legitimacy even for unregistered visitors"),
        ("Incident Severity Flags", "Categorized severity (High, Medium, Low Priority)"),
        ("Resolution Audit Trail", "Archived incident records with reporting officer handle"),
    ]
    for title, val in guard_points:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 10: Stakeholder 5 — Customer / Driver Portal
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Stakeholder Deep-Dive 5 / 5", "🚙 Customer / Driver Portal — 'Find My Car' & Live EV Telemetry")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s10.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Driver Self-Service & EV Transparency"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s10 = [
        "'Find My Car' Search Engine: Allows motorists to enter their license plate and instantly retrieve their parked vehicle location.",
        "Bay & Floor Directional Signage: Displays allotted bay code (e.g. B1-EV-01) and floor name with pedestrian navigation directions.",
        "Live Parked Duration & Fee Meter: Shows live elapsed time (e.g. 3h 20m) and real-time accrued parking charges.",
        "Animated EV Battery Charging Gauge: Custom visual battery graphic displaying live charging status, battery percentage (e.g. 78%), and energy delivered (kWh).",
        "Multi-Floor Vacancy Explorer: Real-time sensor counters for incoming drivers showing available spots across B1, G, F1, and F2.",
    ]
    for b in bullets_s10:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(10)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s10.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "CUSTOMER SELF-SERVICE (/customer/)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = RGBColor(6, 182, 212)

    cust_points = [
        ("Universal Search", "Flexible input formatting (e.g. 'UK-04-EV-2024' or 'uk04ev2024')"),
        ("Floor Level Guidance", "Directs driver to correct building level before exiting lifts"),
        ("Live EV Telemetry", "Real-time battery percentage bar (35% to 100%) and kWh total"),
        ("Digital POS E-Receipt", "One-click access to download or print tax invoice upon exit"),
        ("Public Guest Access", "Accessible on mobile web without requiring staff sign-in"),
    ]
    for title, val in cust_points:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 11: Entity-Relationship (ER) Diagram & Relational Schema
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Relational Database Blueprint", "Entity-Relationship (ER) Diagram & Schema Architecture")

    # Layout 4 relational cards visualizing the schema
    er_entities = [
        ("FLOOR (Building Level)", "PK: id (AutoField)\n• floor_number (Int, Unique)\n• code (Char, 'B1', 'G', 'F1', 'F2')\n• name (Char, Full Floor Name)\n• total_slots (Int, default 12)\n• is_ev_enabled (Bool)\n\nRel: 1 Floor : N Slots", C_NAVY),
        ("PARKING_SLOT (Bay)", "PK: id (AutoField)\n• slot_number (Char, 'B1-EV-01')\n• FK: floor_id -> Floor.id (CASCADE)\n• slot_type (Standard, SUV, EV Bay)\n• is_occupied (Bool)\n• is_ev_bay (Bool)\n\nRel: 1 Slot : N Vehicles", C_BLUE),
        ("VEHICLE (Session Record)", "PK: id (AutoField)\n• license_plate (Char, RTO Validated)\n• vehicle_type (Sedan, SUV, EV, etc.)\n• FK: slot_id -> Slot.id (SET_NULL)\n• entry_time, exit_time (DateTime)\n• status (Parked, Exited)\n• parking_fee, ev_fee, fee (Decimal)\n\nRel: 1 Vehicle : 1 EV Session", C_GREEN),
        ("EV_CHARGING_SESSION", "PK: id (AutoField)\n• 1:1 FK: vehicle_id -> Vehicle.id\n• FK: slot_id -> Slot.id\n• status (Idle, Charging, Completed)\n• energy_kwh (Decimal)\n• rate_per_kwh (Decimal, ₹15.00)\n• total_cost (Decimal)\n\nRel: 1:1 Extension of Vehicle", RGBColor(6, 182, 212)),
    ]
    for idx, (title, body, col) in enumerate(er_entities):
        x = Inches(0.8 + idx * 2.95)
        add_card(s11, x, Inches(1.8), Inches(2.8), Inches(3.6))
        strip = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(0.12))
        strip.fill.solid()
        strip.fill.fore_color.rgb = col
        strip.line.fill.background()

        tb = s11.shapes.add_textbox(x + Inches(0.15), Inches(2.05), Inches(2.5), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_DARK
        p2.space_before = Pt(8)

    # Bottom summary box for ancillary entities
    add_card(s11, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3))
    tb_b = s11.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.1))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    pb1 = tf_b.paragraphs[0]
    pb1.text = "ANCILLARY & GOVERNANCE MODELS: SECURITY_INCIDENT • PROFILE_SETTINGS • AUTH_USER"
    pb1.font.size = Pt(12)
    pb1.font.bold = True
    pb1.font.color.rgb = C_NAVY

    pb2 = tf_b.add_paragraph()
    pb2.text = "• SecurityIncident: reporter, incident_type, license_plate, severity, timestamp, description, is_resolved\n• ProfileSettings (Singleton): facility_name, operator_name, hourly_rate, daily_max_rate, ev_rate_per_kwh, total_capacity\n• User (auth_user): Django authentication core with RBAC mapping across Admin, Manager, Operator, Guard, Customer"
    pb2.font.size = Pt(11)
    pb2.font.color.rgb = C_MUTED
    pb2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: Poka-Yoke Indian License Plate & RTO Validation Engine
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Mistake-Proofing Engine (Shingo Principle)", "Poka-Yoke RTO License Plate Validation Engine (rto_validator.py)")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Poka-Yoke Multi-Tier Validation Rules"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s12 = [
        "1. Sanitization & Normalization: Automatically strips spaces/hyphens and standardizes input to official format (e.g. uk04ak1234 -> UK-04-AK-1234).",
        "2. State Authority Check: Validates official 2-letter Indian State & UT codes (UK, DL, UP, HR, MH, PB, RJ, KA, MP, GJ, TN, WB, etc.).",
        "3. Strict District Range Enforcement: Verifies official RTO district numbers against registered transport authority boundaries.",
        "4. UK-87 Rejection Example: Uttarakhand (UK) RTO codes strictly run from UK-01 (Almora) to UK-20 (Ranikhet). Entering 'UK-87' is strictly blocked with an educational Poka-Yoke alert!",
        "5. Real-Time AJAX Feedback: Queries /api/validate-plate/ on keystroke to provide instant green/red operator alerts before form submission.",
    ]
    for b in bullets_s12:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(8)

    # Right Side Validation Example Box
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), C_NAVY, RGBColor(51, 65, 85))
    tb_r = s12.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "POKA-YOKE VALIDATION TEST CASES"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = RGBColor(96, 165, 250)

    cases = [
        ("❌ Test Case: UK-87-AK-1234", "STATUS: REJECTED (Zero Defect Guard)\nALERT: Poka-Yoke Error Prevention: 'UK-87' is an invalid RTO registration. Uttarakhand RTO codes strictly range from UK-01 to UK-20 (UK-87 does not exist)."),
        ("✅ Test Case: uk04ak5521", "STATUS: ACCEPTED & NORMALIZED\nOUTPUT: UK-04-AK-5521\nMETADATA: Uttarakhand • Nainital / Haldwani RTO"),
        ("✅ Test Case: dl14cc9999", "STATUS: ACCEPTED (Delhi West Rohini RTO)"),
        ("❌ Test Case: DL-99-CC-9999", "STATUS: REJECTED (Delhi RTO only 01 to 14)"),
    ]
    for title, val in cases:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title}\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_WHITE
        p_m.space_before = Pt(8)

    # =========================================================================
    # SLIDE 13: 4-Level Multi-Floor Car Parking Architecture
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Physical Facility Layout", "4-Level Multi-Floor Car Parking Architecture (48 Bays)")

    floors = [
        ("Level 2 (F2): Covered Rooftop", "12 Bays (F2-01 to F2-12)", "Standard Sedans (F2-01 to F2-06) & Compact City Cars (F2-07 to F2-12). Weather-protected covered rooftop structure.", C_NAVY),
        ("Level 1 (F1): First Floor Deck", "12 Bays (F1-01 to F1-12)", "Dedicated to Standard Sedans & Hatchbacks. Fast vehicle throughput with direct egress ramp access.", C_BLUE),
        ("Ground Floor (G): Ingress Level", "12 Bays (G-01 to G-12)", "Heavy SUV & Premium Bays (G-01 to G-06) + Standard Sedans (G-07 to G-12). Reinforced floor slab for oversized vehicles.", C_AMBER),
        ("Basement (B1): EV Charging Hub", "12 Smart Bays (B1-EV-01 to B1-EV-12)", "100% Dedicated Electric Vehicle (EV) Fast Charging Hub. Equipped with virtual 7.2 kW AC chargers & telemetry.", C_GREEN),
    ]
    for idx, (title, cap, desc, col) in enumerate(floors):
        y = Inches(1.8 + idx * 1.25)
        add_card(s13, Inches(0.8), y, Inches(11.7), Inches(1.1))
        bar = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.15), Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s13.shapes.add_textbox(Inches(1.2), y + Inches(0.12), Inches(11.1), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{title} — {cap}"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_DARK
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 14: EV Smart Fast Charging Infrastructure & Telemetry
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "Clean Energy Infrastructure", "EV Fast Charging Station Telemetry & Combined Billing")

    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s14.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "EV Smart Charging Architecture"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s14 = [
        "12 Dedicated Bays: Basement Level B1 is 100% reserved for Electric Vehicles equipped with virtual 7.2 kW AC fast charging ports.",
        "Automatic EV Routing: Arriving vehicles categorized as EV or checking 'Request EV Bay' are auto-routed to Level B1.",
        "Non-EV Reservation Safeguard: Non-EV cars are programmatically prevented from occupying EV charging bays.",
        "Live State Telemetry: Tracks charging state (Idle -> Actively Charging -> Fully Charged 100%), power consumed (kWh), and battery gauge.",
        "Dynamic Battery Gauge: Visual progress meter simulating battery state from 35% to 100% based on energy delivered.",
    ]
    for b in bullets_s14:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(8)

    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s14.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "COMBINED BILLING MATHEMATICS"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_GREEN

    ev_math = [
        ("Combined Invoice Formula", "Total Invoice = Parking Fee + EV Energy Sales"),
        ("Base Parking Charge", "Hourly Duration × ₹30.00/hr (Subject to ₹250.00/day Max Cap)"),
        ("EV Energy Sales", "Energy Consumed (kWh) × EV Tariff Rate (₹15.00/kWh)"),
        ("Live Simulation Example", "Vehicle UK-04-EV-2024 (Parked 3 Hours, 20.0 kWh Delivered):\n• Parking Charge: 3h × ₹30 = ₹90.00\n• EV Power Charge: 20 kWh × ₹15 = ₹300.00\n• Net Invoice Billed: ₹390.00"),
    ]
    for title, val in ev_math:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 15: Commercial POS Checkout & 80mm Thermal Tax Invoice
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15)
    add_header(s15, "Financial Reconciliation & Receipts", "Commercial POS Checkout & 80mm Thermal Tax Invoice (receipt.html)")

    add_card(s15, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s15.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Point-of-Sale Checkout Capabilities"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s15 = [
        "Automated Duration Timestamping: Computes exact stay duration upon departure without human calculation disputes.",
        "Daily Maximum Ceiling Protection: Capped at ₹250.00/day to eliminate runaway multi-day parking billing disputes.",
        "Itemized Charge Breakdown: Clearly itemizes base parking hours, EV energy kWh, included GST (18%), and net payable.",
        "Print-Optimized Thermal Layout: Built strictly to 80mm POS printer specifications (380px centered) with @media print CSS hiding browser chrome.",
        "Barcode & QR Verification: Encodes invoice serial number and vehicle license plate for automated gate exit scanner clearance.",
    ]
    for b in bullets_s15:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(8)

    # Right side 80mm receipt mock
    add_card(s15, Inches(7.5), Inches(1.8), Inches(4.3), Inches(4.8), C_WHITE, RGBColor(203, 213, 225))
    tb_r = s15.shapes.add_textbox(Inches(7.7), Inches(1.9), Inches(3.9), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    pr = tf_r.paragraphs[0]
    pr.text = "PARKSMART PRO ENTERPRISE"
    pr.alignment = PP_ALIGN.CENTER
    pr.font.size = Pt(13)
    pr.font.bold = True
    pr.font.color.rgb = C_NAVY

    receipt_text = (
        "GSTIN: 05AAACP1234F1Z8 • Gate #1 Egress\n"
        "-----------------------------------------\n"
        "TAX INVOICE: INV-000042\n"
        "Vehicle Plate: UK-04-EV-2024\n"
        "Category: Electric Vehicle (EV)\n"
        "Slot: B1-EV-01 (Basement EV Hub)\n"
        "Duration: 3h 00m (3 hrs billed)\n"
        "-----------------------------------------\n"
        "Parking Fee (3h @ ₹30/h):      ₹90.00\n"
        "EV Energy (20.0 kWh @ ₹15):   ₹300.00\n"
        "Included GST (18%):            ₹59.49\n"
        "=========================================\n"
        "TOTAL PAID:                   ₹390.00\n"
        "Mode: Fastag / Auto UPI Debited\n"
        "-----------------------------------------\n"
        "||| | ||||| || |||| |||||| || | |||| ||\n"
        "Thank you for choosing ParkSmart Pro!"
    )
    pr2 = tf_r.add_paragraph()
    pr2.text = receipt_text
    pr2.font.size = Pt(10)
    pr2.font.name = "Consolas"
    pr2.font.color.rgb = C_DARK
    pr2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 16: Security & Role-Based Access Control (RBAC) Enforcement
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_bg(s16)
    add_header(s16, "Access Governance & Threat Prevention", "Strict Role-Based Access Control (RBAC) & Session Defense")

    add_card(s16, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s16.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Security Vulnerabilities Resolved"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    bullets_s16 = [
        "1. Elimination of Auto-Login Bypass: Clicking stakeholder cards on landing page opens an interactive credential verification modal; password entry is strictly required.",
        "2. Server-Side @require_role Decorator: Protects /admin-console/, /manager/, /operator/, /security/. Unauthorized access triggers 403 Access Denied and bounces user to their home console.",
        "3. Prevention of Cross-Role Escalation: A logged-in Security Guard cannot access Admin Console or Manager Ops (even via URL bar tampering).",
        "4. Context-Aware Dynamic Navbar: Templates render only links authorized for the active user role; unauthenticated visitors see zero internal terminal links.",
        "5. Explicit Role Sign-Out: Session switcher requires authenticating with the destination role's credentials to switch accounts.",
    ]
    for b in bullets_s16:
        p_b = tf_l.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(8)

    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), C_NAVY, RGBColor(51, 65, 85))
    tb_r = s16.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "SECURITY AUDIT VERIFICATION"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = RGBColor(96, 165, 250)

    sec_cases = [
        ("Guard Access to /admin-console/", "STATUS: STRICTLY BLOCKED\nALERT: Access Denied (Security Policy): Your account 'guard' (GUARD role) is not authorized. Required: ADMIN."),
        ("Guard Access to /manager/", "STATUS: STRICTLY BLOCKED (403 Policy)"),
        ("Unauthenticated Access to Terminals", "STATUS: REDIRECTED to / with 'Authentication Required'"),
        ("Admin Supervisory Access", "STATUS: GRANTED full oversight across all workstations"),
    ]
    for title, val in sec_cases:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title}\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_WHITE
        p_m.space_before = Pt(10)

    # =========================================================================
    # SLIDE 17: Live Verification, Test Suite & Commercial Dataset
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_bg(s17)
    add_header(s17, "Quality Assurance & Empirical Validation", "Test Suite Execution & Pre-Seeded Commercial Dataset")

    add_card(s17, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_l = s17.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Automated Unit Test Suite (tests.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    test_bullets = [
        "1. test_poka_yoke_rto_validator: Verifies rejection of UK-87 and normalization of UK-04.",
        "2. test_unauthenticated_workstation_access_blocked: Guarantees unauthenticated access is rejected.",
        "3. test_guard_cannot_access_admin_or_manager: Proves RBAC isolation blocks guard from admin/manager consoles.",
        "4. test_admin_supervisory_access: Verifies admin executive privileges.",
        "5. test_credential_authentication_flow: Verifies password verification and rejection of invalid passwords.",
        "6. test_poka_yoke_check_in_rejection_in_form: Ensures operator form blocks invalid plates.",
        "7. test_valid_check_in_and_smart_slot_allocation: Verifies bay allocation logic.",
        "8. test_ev_fast_charging_and_billing: Verifies EV session & combined fee calculation.",
        "9. test_api_validate_plate: Verifies AJAX keystroke validation endpoint.",
    ]
    for b in test_bullets:
        p_b = tf_l.add_paragraph()
        p_b.text = b
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_DARK
        p_b.space_before = Pt(4)

    p_res = tf_l.add_paragraph()
    p_res.text = "TEST SUITE RESULT: 9 / 9 TESTS PASSED (100% OK)"
    p_res.font.size = Pt(12)
    p_res.font.bold = True
    p_res.font.color.rgb = C_GREEN
    p_res.space_before = Pt(8)

    add_card(s17, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    tb_r = s17.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p_rh = tf_r.paragraphs[0]
    p_rh.text = "PRE-SEEDED COMMERCIAL DATASET (seed_multi_floor.py)"
    p_rh.font.size = Pt(14)
    p_rh.font.bold = True
    p_rh.font.color.rgb = C_BLUE

    db_stats = [
        ("Multi-Floor Layout", "4 Floors (B1, G, F1, F2) with 48 Total Bays"),
        ("Active Parked Fleet", "12 Cars allocated across floors with durations"),
        ("Active EV Sessions", "4 EVs in B1 Smart Hub with telemetry & battery %"),
        ("Historical Departures", "33 Exited records with completed parking & EV fees"),
        ("Security Log Reports", "4 Dispatched & resolved gate patrol logs"),
        ("Stakeholder Users", "admin, manager, operator, guard, customer (all seeded)"),
    ]
    for title, val in db_stats:
        p_m = tf_r.add_paragraph()
        p_m.text = f"{title.upper()}:\n{val}"
        p_m.font.size = Pt(11)
        p_m.font.color.rgb = C_NAVY
        p_m.space_before = Pt(8)

    # =========================================================================
    # SLIDE 18: Conclusion, TQM Defense & Key Achievements
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_bg(s18, C_NAVY)

    # Accent bar
    bar = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.2), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_GREEN
    bar.line.fill.background()

    tag = s18.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11), Inches(0.4))
    p = tag.text_frame.paragraphs[0]
    p.text = "PROJECT DEFENSE CONCLUSION & KEY ACHIEVEMENTS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(52, 211, 153)

    t18 = s18.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.2))
    tf18 = t18.text_frame
    tf18.word_wrap = True
    p1 = tf18.paragraphs[0]
    p1.text = "Commercial Quality & Syllabus Compliance"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    concl_points = [
        ("100% BBAT104 Syllabus Compliance", "Digit 8 allotment strictly implemented; all 5 Q08 Quality Goal features operating at production level."),
        ("Complete Commercial SaaS Transformation", "Eliminated academic toy clutter; delivered enterprise UI matching real platforms (FlashParking, TIBA)."),
        ("5 Dedicated Stakeholder Workstations", "Fully realized operational portals for Admin, Operations Manager, Gate Operator, Security Guard, and Customer."),
        ("Industrial Poka-Yoke RTO Protection", "Hard-rejection of invalid district codes (e.g. UK-87) with real-time keystroke feedback."),
        ("EV Charging Hub & 4-Level Architecture", "Seamless 4-floor car parking with virtual 7.2kW EV fast charging, battery telemetry, and 80mm POS billing."),
        ("Zero Security Bypasses & Strict RBAC", "Complete elimination of auto-login vulnerabilities; strict @require_role enforcement and isolated navbars."),
    ]
    for idx, (head, desc) in enumerate(concl_points):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(3.0 + (idx // 2) * 1.35)
        add_card(s18, x, y, Inches(5.6), Inches(1.15), RGBColor(30, 41, 59), RGBColor(51, 65, 85))
        tb = s18.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), Inches(5.2), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        ph = tf.paragraphs[0]
        ph.text = head
        ph.font.size = Pt(13)
        ph.font.bold = True
        ph.font.color.rgb = RGBColor(96, 165, 250)

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = RGBColor(226, 232, 240)
        pd.space_before = Pt(3)

    out_path = "F:\\TQM\\Parking_Management_System_tqm\\ParkSmart_Pro_Enterprise_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == '__main__':
    create_deck()
