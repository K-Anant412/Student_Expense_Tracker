import sys
import os

try:
    import docx2pdf
    print("[INFO] Attempting conversion using docx2pdf...")
    docx2pdf.convert("Student_Expense_Tracker_Project_Report.docx", "Student_Expense_Tracker_Project_Report.pdf")
    print("[SUCCESS] PDF generated using docx2pdf!")
except Exception as e:
    print(f"[WARN] docx2pdf failed: {e}. Falling back to ReportLab...")
