from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import json

import os

# === ENVIRONMENT VARIABLES ===
API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
SERVICE_ACCOUNT_JSON_STR = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
SERVICE_ACCOUNT_JSON = json.loads(SERVICE_ACCOUNT_JSON_STR) if SERVICE_ACCOUNT_JSON_STR else None
# === END ENVIRONMENT VARIABLES ===

@router.route("/execute", methods=["POST"])
def execute():
    try:
        request_obj = Request(flask_request)
        data = request_obj.data
        sheet_id = data.get("sheet_id", "")
        service_account_json = data.get("service_account_json", "")
        tab_sheet_name = data.get("tab_sheet_name", "")
        if not sheet_id:
            return Response.error("Sheet ID is required")
        if not service_account_json:
            return Response.error("Service account JSON is required")
        if not tab_sheet_name:
            return Response.error("Tab Sheet Name is required")
        # Import inside function to avoid PyO3 re-init error
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        if isinstance(service_account_json, str):
            account_info = json.loads(service_account_json)
        else:
            account_info = service_account_json
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
        creds.refresh(GoogleRequest())
        token = creds.token
        # Prepare the request to add a new tab (sheet) to an existing spreadsheet
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = {
            "requests": [
                {"addSheet": {"properties": {"title": tab_sheet_name}}}
            ]
        }
        import requests
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code not in [200, 201]:
            try:
                error_json = resp.json()
                error_detail = error_json.get("error", {}).get("message", resp.text)
            except Exception:
                error_detail = resp.text
            return Response.error(f"Failed to create tab: {error_detail}")
        result = resp.json()
        new_tab_id = result.get("replies", [{}])[0].get("addSheet", {}).get("properties", {}).get("sheetId")
        return Response(data={
            "success": True,
            "sheet_id": sheet_id,
            "new_tab_sheet_name": tab_sheet_name,
            "new_tab_id": new_tab_id,
            "message": f"Tab '{tab_sheet_name}' created successfully."
        })
    except Exception as e:
        return Response.error(f"Failed to create tab: {str(e)}")
