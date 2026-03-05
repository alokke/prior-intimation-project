import requests

BASE_URL = "http://10.48.49.107:8080/SAP-SERVICE/hr"

headers = {
    "Content-Type": "application/json"
}

def get_employee_details(emp_id: str):

    payload = {"empId": emp_id}

    try:
        pa0002 = requests.post(f"{BASE_URL}/pa0002", json=payload, headers=headers).json()
        pa0001 = requests.post(f"{BASE_URL}/pa0001", json=payload, headers=headers).json()
        pa0008 = requests.post(f"{BASE_URL}/pa0008", json=payload, headers=headers).json()

        name = ""
        designation = ""
        scale = ""
        present_pay = ""
        station = ""

        # NAME
        if pa0002.get("pa0002DetailsList"):
            emp = pa0002["pa0002DetailsList"][0]
            name = emp.get("vorna", "") + " " + emp.get("nachn", "")

        # DESIGNATION + STATION
        if pa0001.get("pa0001DetailsList"):
            emp = pa0001["pa0001DetailsList"][0]

            designation = (
                emp.get("plstx") or
                emp.get("plansText") or
                emp.get("stext") or
                emp.get("plans") or
                ""
            )

            station = emp.get("werks", "")

        # PAY
        if pa0008.get("pa0008DetailsList"):
            emp = pa0008["pa0008DetailsList"][0]
            scale = emp.get("trfgr", "")
            present_pay = emp.get("bet01", "")

        return {
            "emp_id": emp_id,
            "name": name.strip(),
            "designation": designation.strip(),
            "scale": scale,
            "present_pay": present_pay,
            "station": station
        }

    except Exception as e:
        return {"error": str(e)}