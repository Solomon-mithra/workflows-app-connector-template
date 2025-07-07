from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import requests
from urllib.parse import quote

import os

# === ENVIRONMENT VARIABLES ===
API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
SERVICE_ACCOUNT_JSON_STR = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
SERVICE_ACCOUNT_JSON = json.loads(SERVICE_ACCOUNT_JSON_STR) if SERVICE_ACCOUNT_JSON_STR else None
# === END ENVIRONMENT VARIABLES ===

def get_sheet_header(spreadsheet_id, sheet_name, api_key=None):
    # Always use hardcoded API key
    api_key = HARDCODED_API_KEY
    try:
        range_string = f"{sheet_name}!1:1"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json().get("values", [])
        if not data:
            return []
        return data[0]
    except Exception as e:
        print(f"DEBUG: get_sheet_header failed: {str(e)}")
        return []

@router.route("/execute", methods=["POST"])
def execute():
    try:
        request = Request(flask_request)
        data = request.data
        sheet_id = data.get("sheet_id", "")
        sheet_name_obj = data.get("sheet_name", "")
        conditions = data.get("conditions", [])
        # Normalize sheet_name
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        if not sheet_id:
            return Response.error("Sheet ID is required")
        if not sheet_name:
            return Response.error("Sheet name is required")
        if not conditions or not isinstance(conditions, list):
            return Response.error("At least one condition is required")
        api_key = HARDCODED_API_KEY
        service_account_json = HARDCODED_SERVICE_ACCOUNT_JSON
        # Fetch all rows
        range_string = f"{sheet_name}"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={api_key}"
        resp = requests.get(url, timeout=10)
        all_values = resp.json().get("values", [])
        if not all_values or len(all_values) < 2:
            return Response.error("Could not fetch sheet data to determine rows to delete.")
        header = all_values[0]
        # Validate all key_columns exist
        for cond in conditions:
            key_column_obj = cond.get("key_column", "")
            key_column = ""
            if isinstance(key_column_obj, dict):
                key_column = key_column_obj.get("id", "") or key_column_obj.get("label", "") or key_column_obj.get("value", "")
            elif isinstance(key_column_obj, str):
                key_column = key_column_obj
            if key_column not in header:
                return Response.error(f"Key column '{key_column}' not found in header: {header}")
        # Build list of rows to delete (AND logic: all conditions must match)
        rows_to_delete = []
        for i, row in enumerate(all_values[1:], start=2):
            match = True
            for cond in conditions:
                key_column_obj = cond.get("key_column", "")
                key_value_obj = cond.get("key_value", "")
                key_column = ""
                if isinstance(key_column_obj, dict):
                    key_column = key_column_obj.get("id", "") or key_column_obj.get("label", "") or key_column_obj.get("value", "")
                elif isinstance(key_column_obj, str):
                    key_column = key_column_obj
                key_value = ""
                if isinstance(key_value_obj, dict):
                    key_value = key_value_obj.get("id", "") or key_value_obj.get("label", "") or key_value_obj.get("value", "")
                elif isinstance(key_value_obj, str):
                    key_value = key_value_obj
                col_idx = header.index(key_column)
                val = row[col_idx] if col_idx < len(row) else ""
                if val != key_value:
                    match = False
                    break
            if match:
                rows_to_delete.append(i)
        if not rows_to_delete:
            return Response.error("No rows found matching all conditions.")
        # Prepare batch delete request
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        import json
        account_info = service_account_json
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
        creds.refresh(GoogleRequest())
        token = creds.token
        # Get the correct sheetId for the sheet_name
        meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?key={api_key}"
        meta_resp = requests.get(meta_url, timeout=10)
        sheet_gid = 0
        if meta_resp.status_code == 200:
            meta = meta_resp.json()
            for s in meta.get("sheets", []):
                props = s.get("properties", {})
                if props.get("title") == sheet_name:
                    sheet_gid = props.get("sheetId", 0)
                    break
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
        delete_requests = []
        for row_num in sorted(rows_to_delete, reverse=True):
            delete_requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_gid,
                        "dimension": "ROWS",
                        "startIndex": row_num - 1,
                        "endIndex": row_num
                    }
                }
            })
        body = {"requests": delete_requests}
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(batch_url, headers=headers, json=body, timeout=30)
        if resp.status_code not in [200, 201]:
            error_detail = resp.text
            try:
                error_json = resp.json()
                error_detail = error_json.get("error", {}).get("message", resp.text)
            except:
                pass
            return Response.error(f"Failed to delete rows: {error_detail}")
        return Response(
            data={
                "sheet_id": sheet_id,
                "sheet_name": sheet_name,
                "conditions": conditions,
                "rows_deleted": len(rows_to_delete),
                "message": f"Deleted {len(rows_to_delete)} row(s) matching all conditions."
            },
            metadata={
                "affected_records": len(rows_to_delete),
                "message": f"Successfully deleted {len(rows_to_delete)} row(s) in sheet '{sheet_name}' matching all conditions."
            }
        )
    except Exception as e:
        return Response.error(str(e))

@router.route("/content", methods=["POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data
        form_data = data.get("form_data", {})
        sheet_id = form_data.get("sheet_id", "")
        api_key = HARDCODED_API_KEY
        content_object_names = data.get("content_object_names", [])
        content_objects = []
        for content_name in content_object_names:
            cid = content_name.get("id")
            array_index = content_name.get("array_index") if isinstance(content_name, dict) else None
            if isinstance(array_index, str) and array_index.isdigit():
                array_index = int(array_index)
            if cid == "sheet_names":
                if not sheet_id:
                    content_objects.append({"content_object_name": "sheet_names", "data": []})
                    continue
                # Fetch sheet names using API v4
                meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?key={api_key}"
                resp = requests.get(meta_url, timeout=10)
                if resp.status_code != 200:
                    content_objects.append({"content_object_name": "sheet_names", "data": []})
                    continue
                meta = resp.json()
                sheet_options = []
                for s in meta.get("sheets", []):
                    props = s.get("properties", {})
                    name = props.get("title", "")
                    if name:
                        sheet_options.append({
                            "value": {"id": name, "label": name},
                            "label": name
                        })
                content_objects.append({"content_object_name": "sheet_names", "data": sheet_options})
            elif cid == "column_names":
                sheet_name_obj = form_data.get("sheet_name", "")
                sheet_name = ""
                if isinstance(sheet_name_obj, dict):
                    sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
                elif isinstance(sheet_name_obj, str):
                    sheet_name = sheet_name_obj
                if not sheet_id or not sheet_name:
                    content_objects.append({"content_object_name": "column_names", "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name, api_key)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": "column_names", "data": options})
        return Response(data={"content_objects": content_objects})
    except Exception as e:
        print(f"DEBUG: /content error: {e}")
        return Response(data={"content_objects": []})
