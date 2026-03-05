from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from database import save_form_data
from sap_service import get_employee_details

import io
from xhtml2pdf import pisa
from datetime import datetime

# -------------------------------------------------
# CREATE FASTAPI APP
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# TEMPLATE DIRECTORY
# -------------------------------------------------
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------
# LOAD FORM PAGE
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def load_form(request: Request):
    return templates.TemplateResponse(
        "prior_proforma.html",
        {"request": request}
    )

# -------------------------------------------------
# FETCH EMPLOYEE FROM SAP
# -------------------------------------------------
@app.get("/employee/{emp_id}")
def fetch_employee(emp_id: str):
    data = get_employee_details(emp_id)
    return JSONResponse(content=data)

# -------------------------------------------------
# GENERATE PDF + SAVE DATA
# -------------------------------------------------
@app.post("/generate-pdf")
async def generate_pdf(
    request: Request,
    emp_id: str = Form(...),
    name_designation: str = Form(...),
    scale_pay: str = Form(...),
    purpose: str = Form(...),
    property_type: str = Form(...),
    probable_date: str = Form(...),
    mode: str = Form(...),
    location_7a: str = Form(...),
    description_7b: str = Form(...),
    hold_type_7c: str = Form(...),
    interest_7d: str = Form(...),
    ownership_7e: str = Form(...),
    price: str = Form(...),
    finance_source_main: str = Form(...),
    personal_savings_9a: str = Form(...),
    other_sources_9b: str = Form(...),
    sanction_details: str = Form(...),
    party_name_11a: str = Form(...),
    party_relation_11b: str = Form(...),
    official_dealings_11c: str = Form(...),
    transaction_mode_11d: str = Form(...),
    additional_facts: str = Form(...),
    station: str = Form(...),
    submission_date: str = Form(...)
):

    # -------------------------------------------------
    # FORMAT DATE TO DD-MM-YYYY
    # -------------------------------------------------
    if probable_date:
        probable_date = datetime.strptime(probable_date, "%Y-%m-%d").strftime("%d-%m-%Y")

    if submission_date:
        submission_date = datetime.strptime(submission_date, "%Y-%m-%d").strftime("%d-%m-%Y")

    # -------------------------------------------------
    # SAVE DATA TO DATABASE
    # -------------------------------------------------
    save_form_data(
        emp_id,
        name_designation,
        scale_pay,
        purpose,
        property_type,
        probable_date,
        mode,
        location_7a,
        description_7b,
        hold_type_7c,
        interest_7d,
        ownership_7e,
        price,
        finance_source_main,
        personal_savings_9a,
        other_sources_9b,
        sanction_details,
        party_name_11a,
        party_relation_11b,
        official_dealings_11c,
        transaction_mode_11d,
        additional_facts,
        station,
        submission_date
    )

    signature_name = name_designation

    # -------------------------------------------------
    # RENDER HTML TEMPLATE
    # -------------------------------------------------
    html_content = templates.get_template("pdf_template.html").render(
        emp_id=emp_id,
        name_designation=name_designation,
        scale_pay=scale_pay,
        purpose=purpose,
        property_type=property_type,
        probable_date=probable_date,
        mode=mode,
        location_7a=location_7a,
        description_7b=description_7b,
        hold_type_7c=hold_type_7c,
        interest_7d=interest_7d,
        ownership_7e=ownership_7e,
        price=price,
        finance_source_main=finance_source_main,
        personal_savings_9a=personal_savings_9a,
        other_sources_9b=other_sources_9b,
        sanction_details=sanction_details,
        party_name_11a=party_name_11a,
        party_relation_11b=party_relation_11b,
        official_dealings_11c=official_dealings_11c,
        transaction_mode_11d=transaction_mode_11d,
        additional_facts=additional_facts,
        station=station,
        submission_date=submission_date,
        signature_name=signature_name
    )

    # -------------------------------------------------
    # CREATE PDF
    # -------------------------------------------------
    pdf = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html_content), dest=pdf)
    pdf.seek(0)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Prior_Intimation.pdf"
        }
    )