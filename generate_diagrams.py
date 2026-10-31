"""
Diagram Generator for Student Expense Tracker and Analyzer Project Report.
Generates high-resolution academic diagrams matching Shivaji University / BCA requirements:
1. System Architecture Diagram (3-Tier Layered Architecture)
2. DFD Level 0 Context Diagram
3. DFD Level 1 Process Flow Diagram
4. UML Use Case Diagram
5. UML Class Diagram
6. UML Sequence Diagram
7. Database Entity-Relationship (ER) Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("assets/diagrams", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'


def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 96, "Student Expense Tracker and Analyzer — 3-Tier Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')

    # Tier 1: Presentation Layer
    p_rect = patches.FancyBboxPatch((5, 68), 90, 22, boxstyle="round,pad=1.5", 
                                    edgecolor='#2563EB', facecolor='#F0F7FF', linewidth=2)
    ax.add_patch(p_rect)
    ax.text(8, 86, "Presentation Layer (Streamlit Web Interface - Port 8501)", 
            fontsize=11, fontweight='bold', color='#1E40AF')
    
    # Sub-boxes in Presentation Layer
    components = [
        ("Dashboard View", "KPI Metrics & Charts\nBudget Warning Alerts"),
        ("Transaction Portal", "CRUD Data Table\nSearch & Dynamic Filters"),
        ("Budget Manager", "Category Monthly Limits\nUtilization Progress Bars"),
        ("Analytics & Reports", "12-Month Trends\nStatement CSV Export")
    ]
    for i, (title, desc) in enumerate(components):
        bx = 8 + i * 21.5
        box = patches.FancyBboxPatch((bx, 71), 20, 12, boxstyle="square,pad=0.5", 
                                    edgecolor='#93C5FD', facecolor='#FFFFFF', linewidth=1.2)
        ax.add_patch(box)
        ax.text(bx + 10, 79, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#1E293B')
        ax.text(bx + 10, 74.5, desc, ha='center', va='center', fontsize=7.5, color='#475569')

    # Arrow 1
    ax.annotate('', xy=(50, 61), xytext=(50, 68),
                arrowprops=dict(arrowstyle="<->", color='#3B82F6', lw=2.5))
    ax.text(52, 64.5, "HTTP REST API Communication (JSON Payloads)", fontsize=9, fontweight='bold', color='#1E40AF')

    # Tier 2: Application / API Layer
    a_rect = patches.FancyBboxPatch((5, 36), 90, 22, boxstyle="round,pad=1.5", 
                                    edgecolor='#059669', facecolor='#F0FDF4', linewidth=2)
    ax.add_patch(a_rect)
    ax.text(8, 54, "Application & Service Layer (Flask REST API Engine - Port 5000)", 
            fontsize=11, fontweight='bold', color='#065F46')

    api_components = [
        ("REST API Routes", "/api/transactions\n/api/categories\n/api/budgets, /api/analytics"),
        ("Transaction Service", "Payload Validation\nDate & Type Checks\nCRUD Business Logic"),
        ("Budget Service", "Monthly Expense Aggregation\nThreshold Alert Logic\nDuplicate Rejection"),
        ("Analytics Service", "Net Balance Calculation\nMonthly Trends & MoM\nCSV Export Generator")
    ]
    for i, (title, desc) in enumerate(api_components):
        bx = 8 + i * 21.5
        box = patches.FancyBboxPatch((bx, 39), 20, 12, boxstyle="square,pad=0.5", 
                                    edgecolor='#86EFAC', facecolor='#FFFFFF', linewidth=1.2)
        ax.add_patch(box)
        ax.text(bx + 10, 47, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#1E293B')
        ax.text(bx + 10, 42.5, desc, ha='center', va='center', fontsize=7.5, color='#475569')

    # Arrow 2
    ax.annotate('', xy=(50, 29), xytext=(50, 36),
                arrowprops=dict(arrowstyle="<->", color='#10B981', lw=2.5))
    ax.text(52, 32.5, "SQLAlchemy ORM / PyMySQL Driver (Parameterized SQL)", fontsize=9, fontweight='bold', color='#065F46')

    # Tier 3: Database Persistence Layer
    d_rect = patches.FancyBboxPatch((5, 6), 90, 20, boxstyle="round,pad=1.5", 
                                    edgecolor='#D97706', facecolor='#FFFBEB', linewidth=2)
    ax.add_patch(d_rect)
    ax.text(8, 22, "Data Persistence Layer (MySQL Relational Database Engine - Port 3306)", 
            fontsize=11, fontweight='bold', color='#92400E')

    db_tables = [
        ("users", "id, username, email\nfull_name, currency"),
        ("categories", "id, name, type\ndescription, is_default"),
        ("transactions", "id, user_id, category_id\ntype, amount, date, method"),
        ("budgets", "id, category_id, month\nyear, amount, timestamps")
    ]
    for i, (title, desc) in enumerate(db_tables):
        bx = 8 + i * 21.5
        box = patches.FancyBboxPatch((bx, 9), 20, 10, boxstyle="square,pad=0.5", 
                                    edgecolor='#FDE68A', facecolor='#FFFFFF', linewidth=1.2)
        ax.add_patch(box)
        ax.text(bx + 10, 16, f"Table: {title}", ha='center', va='center', fontsize=9, fontweight='bold', color='#1E293B')
        ax.text(bx + 10, 12, desc, ha='center', va='center', fontsize=7.5, color='#475569')

    plt.tight_layout()
    plt.savefig("assets/diagrams/architecture_diagram.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_dfd_level0():
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 94, "Data Flow Diagram (DFD) — Level 0 Context Diagram", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    # External Entity: Student User
    user_box = patches.FancyBboxPatch((6, 38), 24, 24, boxstyle="square,pad=0.5", 
                                      edgecolor='#2563EB', facecolor='#EFF6FF', linewidth=2)
    ax.add_patch(user_box)
    ax.text(18, 50, "STUDENT USER\n(College Student)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Central Process: 0.0 System
    proc_circle = patches.Circle((50, 50), 16, edgecolor='#059669', facecolor='#ECFDF5', linewidth=2.5)
    ax.add_patch(proc_circle)
    ax.text(50, 52, "0.0\nStudent Expense\nTracker & Analyzer\nSystem", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#065F46')

    # External Entity: Administrator / Faculty
    admin_box = patches.FancyBboxPatch((70, 38), 24, 24, boxstyle="square,pad=0.5", 
                                       edgecolor='#7C3AED', facecolor='#F5F3FF', linewidth=2)
    ax.add_patch(admin_box)
    ax.text(82, 50, "EVALUATOR /\nFACULTY GUIDE", ha='center', va='center', fontsize=10, fontweight='bold')

    # Flows User -> Process
    ax.annotate('', xy=(34, 55), xytext=(30, 55), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))
    ax.text(32, 58, "Income / Expense Records,\nMonthly Budgets, Queries", ha='center', fontsize=8, color='#1E40AF')

    # Flows Process -> User
    ax.annotate('', xy=(30, 45), xytext=(34, 45), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5))
    ax.text(32, 41, "Financial Dashboard, Alerts,\nReports & Analytics", ha='center', fontsize=8, color='#065F46')

    # Flows Process -> Admin
    ax.annotate('', xy=(70, 52), xytext=(66, 52), arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=1.5))
    ax.text(68, 56, "Academic CSV Reports,\nBudget Utilization Ledger", ha='center', fontsize=8, color='#5B21B6')

    plt.tight_layout()
    plt.savefig("assets/diagrams/dfd_level0.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_dfd_level1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "Data Flow Diagram (DFD) — Level 1 Detailed Process Flow", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    # Processes
    procs = [
        ("1.0", "Record\nTransactions", (20, 72)),
        ("2.0", "Manage\nCategories", (20, 38)),
        ("3.0", "Set Monthly\nBudgets", (50, 72)),
        ("4.0", "Compute Budget\nAlerts", (50, 38)),
        ("5.0", "Financial\nAnalytics", (80, 72)),
        ("6.0", "Report\nExport", (80, 38)),
    ]
    for num, label, (x, y) in procs:
        c = patches.Circle((x, y), 8.5, edgecolor='#2563EB', facecolor='#EFF6FF', linewidth=1.8)
        ax.add_patch(c)
        ax.text(x, y + 1.5, num, ha='center', va='center', fontsize=8, fontweight='bold', color='#1E40AF')
        ax.text(x, y - 2, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

    # Data Stores
    stores = [
        ("D1: transactions", (35, 12)),
        ("D2: categories", (10, 12)),
        ("D3: budgets", (65, 12)),
    ]
    for name, (x, y) in stores:
        # Open ended rectangle for DFD store
        line1 = patches.Rectangle((x, y), 20, 7, fill=False, edgecolor='#059669', linewidth=1.5)
        ax.add_patch(line1)
        ax.text(x + 10, y + 3.5, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46')

    # Arrows connecting to stores
    ax.annotate('', xy=(38, 20), xytext=(22, 63), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))
    ax.annotate('', xy=(15, 20), xytext=(20, 29), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))
    ax.annotate('', xy=(68, 20), xytext=(52, 63), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.2))
    ax.annotate('', xy=(50, 47), xytext=(50, 63), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.2))
    ax.annotate('', xy=(78, 47), xytext=(78, 63), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.2))

    plt.tight_layout()
    plt.savefig("assets/diagrams/dfd_level1.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "UML Use Case Diagram — Student Expense Tracker and Analyzer", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    # Boundary box
    bound = patches.FancyBboxPatch((28, 5), 68, 87, boxstyle="square,pad=0.5", 
                                   edgecolor='#64748B', facecolor='#F8FAFC', linewidth=1.5)
    ax.add_patch(bound)
    ax.text(62, 89, "Student Expense Tracker System Boundary", ha='center', fontsize=10, fontweight='bold', color='#475569')

    # Actor: Student
    ax.text(12, 58, "👤\nCollege Student\n(Primary Actor)", ha='center', va='center', fontsize=10, fontweight='bold', color='#1E293B')

    # Use Cases (Ellipses)
    use_cases = [
        ("View Financial Dashboard & KPIs", 80),
        ("Record Income & Expense Transactions", 70),
        ("Search, Filter & Sort Transactions", 60),
        ("Update / Delete Existing Transaction", 50),
        ("Configure Monthly Category Budgets", 40),
        ("Monitor Budget Utilization & Warnings", 30),
        ("Analyze 12-Month Spending Trends", 20),
        ("Generate & Download CSV Statement", 10),
    ]

    for label, y in use_cases:
        ellipse = patches.FancyBboxPatch((35, y - 3.5), 55, 7, boxstyle="round,pad=1.2", 
                                         edgecolor='#2563EB', facecolor='#FFFFFF', linewidth=1.4)
        ax.add_patch(ellipse)
        ax.text(62.5, y, label, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E293B')
        # Connecting line
        ax.plot([18, 35], [54, y], color='#94A3B8', linestyle='-', linewidth=1.2)

    plt.tight_layout()
    plt.savefig("assets/diagrams/use_case_diagram.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "UML Class Diagram — Domain Entities & Service Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    # Classes: Category, Transaction, Budget, User
    classes = [
        ("User", 5, 52, 26, 38, [
            "+ id: Integer [PK]",
            "+ username: String",
            "+ email: String",
            "+ full_name: String",
            "+ currency: String = '₹'"
        ], [
            "+ to_dict(): dict"
        ]),
        ("Category", 37, 52, 26, 38, [
            "+ id: Integer [PK]",
            "+ name: String",
            "+ type: Enum('Income','Expense')",
            "+ description: String",
            "+ is_default: Boolean"
        ], [
            "+ to_dict(): dict"
        ]),
        ("Transaction", 69, 52, 27, 38, [
            "+ id: Integer [PK]",
            "+ user_id: Integer [FK]",
            "+ category_id: Integer [FK]",
            "+ type: Enum('Income','Expense')",
            "+ amount: Decimal(10,2)",
            "+ date: Date",
            "+ payment_method: String",
            "+ description: String"
        ], [
            "+ to_dict(): dict"
        ]),
        ("Budget", 37, 8, 26, 36, [
            "+ id: Integer [PK]",
            "+ user_id: Integer [FK]",
            "+ category_id: Integer [FK]",
            "+ month: Integer (1-12)",
            "+ year: Integer",
            "+ amount: Decimal(10,2)"
        ], [
            "+ to_dict(): dict"
        ]),
        ("Services & Engine", 69, 8, 27, 36, [
            "+ TransactionService",
            "+ CategoryService",
            "+ BudgetService",
            "+ AnalyticsService"
        ], [
            "+ calculate_utilization()",
            "+ parse_and_validate_amount()",
            "+ get_dashboard_summary()",
            "+ get_report_data()"
        ])
    ]

    for title, x, y, w, h, attrs, methods in classes:
        # Outer box
        rect = patches.Rectangle((x, y), w, h, edgecolor='#1E293B', facecolor='#FFFFFF', linewidth=1.5)
        ax.add_patch(rect)
        # Header banner
        header = patches.Rectangle((x, y + h - 6), w, 6, edgecolor='#1E293B', facecolor='#EFF6FF', linewidth=1.5)
        ax.add_patch(header)
        ax.text(x + w / 2, y + h - 3, f"<<Entity>> {title}", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')
        
        # Attributes
        curr_y = y + h - 9
        for attr in attrs:
            ax.text(x + 1.5, curr_y, attr, fontsize=7, color='#0F172A')
            curr_y -= 3.2
            
        # Divider line
        div_y = y + 10
        ax.plot([x, x + w], [div_y, div_y], color='#CBD5E1', linewidth=1)
        
        # Methods
        curr_m = div_y - 3
        for m in methods:
            ax.text(x + 1.5, curr_m, m, fontsize=7, color='#059669')
            curr_m -= 3.2

    # Cardinality / Association lines
    ax.annotate('', xy=(37, 72), xytext=(31, 72), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.5))
    ax.text(33, 74, "1..*", fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(69, 72), xytext=(63, 72), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.5))
    ax.text(65, 74, "1..*", fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(50, 44), xytext=(50, 52), arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.5))
    ax.text(51.5, 48, "1..*", fontsize=7.5, fontweight='bold')

    plt.tight_layout()
    plt.savefig("assets/diagrams/class_diagram.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "UML Sequence Diagram — Transaction Creation & Real-Time Budget Check", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    lifelines = [
        ("Student UI\n(Streamlit)", 15),
        ("HTTP Client\n(Requests)", 38),
        ("Flask REST API\n(Controllers)", 62),
        ("MySQL DB\n(SQLAlchemy)", 85)
    ]

    for title, x in lifelines:
        box = patches.FancyBboxPatch((x - 9, 82), 18, 9, boxstyle="square,pad=0.4", 
                                     edgecolor='#2563EB', facecolor='#EFF6FF', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, 86.5, title, ha='center', va='center', fontsize=8, fontweight='bold', color='#1E40AF')
        # Dashed lifeline
        ax.plot([x, x], [12, 82], color='#94A3B8', linestyle='--', linewidth=1.2)

    # Sequence Messages
    steps = [
        (76, 15, 38, "1: Fill transaction form & click 'Record'", "->"),
        (68, 38, 62, "2: POST /api/transactions (JSON)", "->"),
        (60, 62, 62, "3: Validate amount > 0, type, date", "self"),
        (52, 62, 85, "4: INSERT INTO transactions (...)", "->"),
        (44, 85, 62, "5: Return ID & committed row", "-->"),
        (36, 62, 85, "6: Query category budget & total spent", "->"),
        (28, 85, 62, "7: Return spent vs budget (utilization %)", "-->"),
        (20, 62, 38, "8: Return HTTP 201 Created + Budget Alert", "-->"),
        (14, 38, 15, "9: Render success toast & update charts", "-->"),
    ]

    for y, x1, x2, msg, arrow_type in steps:
        if arrow_type == "self":
            ax.annotate('', xy=(x1 + 3, y - 4), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.2))
            ax.text(x1 + 4, y - 2, msg, fontsize=7.5, color='#1E293B')
        else:
            style = "->" if arrow_type == "->" else "->"
            ls = '-' if arrow_type == "->" else '--'
            color = '#2563EB' if arrow_type == "->" else '#059669'
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle=style, linestyle=ls, color=color, lw=1.2))
            ax.text((x1 + x2) / 2, y + 1.5, msg, ha='center', fontsize=7.5, color='#0F172A')

    plt.tight_layout()
    plt.savefig("assets/diagrams/sequence_diagram.png", bbox_inches='tight', dpi=300)
    plt.close()


def create_er_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "Entity-Relationship (ER) Diagram — MySQL Relational Schema", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')

    entities = [
        ("users", 8, 55, 24, 34, [
            "PK | id: INT AUTO_INC",
            "UQ | username: VARCHAR(50)",
            "UQ | email: VARCHAR(100)",
            "     full_name: VARCHAR(100)",
            "     currency: VARCHAR(10)",
            "     created_at: TIMESTAMP"
        ]),
        ("categories", 40, 55, 24, 34, [
            "PK | id: INT AUTO_INC",
            "     name: VARCHAR(50)",
            "     type: ENUM",
            "     description: VARCHAR(255)",
            "     is_default: BOOLEAN",
            "UQ | (name, type)"
        ]),
        ("transactions", 72, 55, 24, 34, [
            "PK | id: INT AUTO_INC",
            "FK | user_id: INT",
            "FK | category_id: INT",
            "     type: ENUM",
            "     amount: DECIMAL(10,2)",
            "     date: DATE",
            "     payment_method: VARCHAR",
            "     description: VARCHAR"
        ]),
        ("budgets", 40, 10, 24, 34, [
            "PK | id: INT AUTO_INC",
            "FK | user_id: INT",
            "FK | category_id: INT",
            "     month: INT (1-12)",
            "     year: INT",
            "     amount: DECIMAL(10,2)",
            "UQ | (category_id, m, y)"
        ])
    ]

    for title, x, y, w, h, fields in entities:
        rect = patches.Rectangle((x, y), w, h, edgecolor='#334155', facecolor='#FFFFFF', linewidth=1.5)
        ax.add_patch(rect)
        hdr = patches.Rectangle((x, y + h - 5.5), w, 5.5, edgecolor='#334155', facecolor='#F1F5F9', linewidth=1.5)
        ax.add_patch(hdr)
        ax.text(x + w / 2, y + h - 2.8, f"TABLE: {title.upper()}", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

        curr_y = y + h - 9
        for f in fields:
            prefix = f.split('|')[0] if '|' in f else ''
            text_color = '#DC2626' if 'PK' in prefix else ('#2563EB' if 'FK' in prefix else '#334155')
            ax.text(x + 1.2, curr_y, f, fontsize=6.8, color=text_color, family='monospace')
            curr_y -= 3.8

    # Relationship connectors
    # users -> transactions (1 to many)
    ax.annotate('', xy=(72, 75), xytext=(32, 75), arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.5))
    ax.text(52, 76.5, "1 to Many (owns)", ha='center', fontsize=8, color='#1E40AF')

    # categories -> transactions (1 to many)
    ax.annotate('', xy=(72, 65), xytext=(64, 65), arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5))
    ax.text(68, 66.5, "1..N", ha='center', fontsize=8, color='#065F46')

    # categories -> budgets (1 to many)
    ax.annotate('', xy=(52, 44), xytext=(52, 55), arrowprops=dict(arrowstyle="->", color='#D97706', lw=1.5))
    ax.text(53.5, 49, "1 to Many (budgets)", fontsize=8, color='#92400E')

    plt.tight_layout()
    plt.savefig("assets/diagrams/er_diagram.png", bbox_inches='tight', dpi=300)
    plt.close()


if __name__ == "__main__":
    print("[INFO] Generating System Architecture Diagram...")
    create_architecture_diagram()
    print("[INFO] Generating DFD Level 0...")
    create_dfd_level0()
    print("[INFO] Generating DFD Level 1...")
    create_dfd_level1()
    print("[INFO] Generating UML Use Case Diagram...")
    create_use_case_diagram()
    print("[INFO] Generating UML Class Diagram...")
    create_class_diagram()
    print("[INFO] Generating UML Sequence Diagram...")
    create_sequence_diagram()
    print("[INFO] Generating ER Diagram...")
    create_er_diagram()
    print("[SUCCESS] All 7 diagrams generated successfully in assets/diagrams/!")
