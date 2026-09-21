# Builds Data\Input\MasterExcel_ClientAccessDB.xlsx skeleton (headers only).
# Schema per build brief Section 7. Real rows are maintained jointly by the
# Customer Management (CM) team and the RPA administrator - not fabricated here.
import openpyxl
from openpyxl.styles import Font, PatternFill

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "ClientAccess"

headers = [
    "Client Email", "MatGroup", "MatGroup4", "Brand Name", "Status",
    "Date Registered", "Registered By", "Last Updated", "Updated By", "Remarks",
]
ws.append(headers)
for c in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=c)
    cell.fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    cell.font = Font(bold=True, color="FFFFFF")
ws.freeze_panes = "A2"

widths = [30, 14, 14, 24, 12, 16, 18, 16, 18, 30]
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[chr(64 + i)].width = w

# Example rows - for local testing of Section 3.3 sender authorization only.
# Replace with real registrations before go-live.
ws.append([
    "supamas.t@dksh.com", "0453", "0453-01", "Example Brand", "Active",
    "2026-09-15", "RPA Admin", "2026-09-15", "RPA Admin",
    "Example row for testing - replace with real registration data",
])
ws.append([
    "sirirat.char@dksh.com", "0453", "0453-01", "Example Brand", "Suspended",
    "2025-01-10", "RPA Admin", "2026-09-15", "RPA Admin",
    "Example row for testing NotAuthorized exception path - access suspended",
])

wb.save(r"C:\Users\hecrpasupport.th\Documents\MyRPA\Collection_OutstandingStatement_Automation\Data\Input\MasterExcel_ClientAccessDB.xlsx")
print("MasterExcel_ClientAccessDB.xlsx written.")
