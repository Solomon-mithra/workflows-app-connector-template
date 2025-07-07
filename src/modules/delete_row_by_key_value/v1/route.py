from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import requests
from urllib.parse import quote
import os
import json

# === ENVIRONMENT VARIABLES ===
API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
SERVICE_ACCOUNT_JSON_STR = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
SERVICE_ACCOUNT_JSON = json.loads(SERVICE_ACCOUNT_JSON_STR) if SERVICE_ACCOUNT_JSON_STR else None
# === END ENVIRONMENT VARIABLES ===

def get_sheets_with_api_v4(spreadsheet_id):
    try:
        metadata_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?key={API_KEY}"
        response = requests.get(metadata_url, timeout=10)
        if response.status_code != 200:
            return []
        metadata = response.json()
        sheets = metadata.get('sheets', [])
        return [{"name": s['properties']['title'], "gid": s['properties']['sheetId']} for s in sheets]
    except Exception as e:
        print(f"DEBUG: get_sheets_with_api_v4 failed: {str(e)}")
        return []

def get_sheet_header(spreadsheet_id, sheet_name):
    try:
        range_string = f"{sheet_name}!1:1"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={API_KEY}"
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

def get_column_values(spreadsheet_id, sheet_name, key_column):
    try:
        range_string = f"{sheet_name}"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={API_KEY}"
        resp = requests.get(url, timeout=10)
        all_values = resp.json().get("values", [])
        if not all_values or len(all_values) < 2:
            return []
        header = all_values[0]
        if key_column not in header:
            return []
        col_idx = header.index(key_column)
        value_options = []
        seen = set()
        for row in all_values[1:]:
            val = row[col_idx] if col_idx < len(row) else ""
            if val and val not in seen:
                value_options.append({"value": {"id": val, "label": str(val)}, "label": str(val)})
                seen.add(val)
        return value_options
    except Exception as e:
        print(f"DEBUG: get_column_values failed: {str(e)}")
        return []

def get_sheet_id(spreadsheet_id, sheet_name):
    # Helper to get the numeric sheetId for batchUpdate
    sheets = get_sheets_with_api_v4(spreadsheet_id)
    for s in sheets:
        if s["name"] == sheet_name:
            return s["gid"]
    return 0

@router.route("/content", methods=["POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data
        form_data = data.get("form_data", {})
        sheet_id = form_data.get("sheet_id", "")
        sheet_name_obj = form_data.get("sheet_name", "")
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        key_column_obj = form_data.get("key_column", "")
        key_column = ""
        if isinstance(key_column_obj, dict):
            key_column = key_column_obj.get("id", "") or key_column_obj.get("label", "") or key_column_obj.get("value", "")
        elif isinstance(key_column_obj, str):
            key_column = key_column_obj
        content_object_names = data.get("content_object_names", [])
        content_objects = []
        for content_name in content_object_names:
            cid = content_name.get("id")
            if cid == "sheet_names":
                if not sheet_id:
                    content_objects.append({"content_object_name": "sheet_names", "data": []})
                    continue
                available_sheets = get_sheets_with_api_v4(sheet_id)
                sheet_options = [{"value": {"id": s["name"], "label": s["name"]}, "label": s["name"]} for s in available_sheets]
                content_objects.append({"content_object_name": "sheet_names", "data": sheet_options})
            elif cid == "column_names":
                if not sheet_id or not sheet_name:
                    content_objects.append({"content_object_name": "column_names", "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": "column_names", "data": options})
            elif cid == "key_columns":
                if not sheet_id or not sheet_name:
                    content_objects.append({"content_object_name": "key_columns", "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": "key_columns", "data": options})
            elif cid == "key_values":
                if not sheet_id or not sheet_name or not key_column:
                    content_objects.append({"content_object_name": "key_values", "data": []})
                    continue
                value_options = get_column_values(sheet_id, sheet_name, key_column)
                content_objects.append({"content_object_name": "key_values", "data": value_options})
        return Response(data={"content_objects": content_objects})
    except Exception as e:
        return Response(data={"content_objects": []})

@router.route("/execute", methods=["POST"])
def execute():
    try:
        request = Request(flask_request)
        data = request.data
        sheet_id = data.get("sheet_id", "")
        service_account_json = SERVICE_ACCOUNT_JSON
        sheet_name_obj = data.get("sheet_name", "")
        key_column_obj = data.get("key_column", "")
        key_value_obj = data.get("key_value", "")
        conditions = data.get("conditions", [])
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        key_column = ""
        key_value = ""
        if conditions and isinstance(conditions, list):
            # Only support first condition for now
            cond = conditions[0]
            key_column = cond.get("key_column", "")
            key_value = cond.get("key_value", "")
            if isinstance(key_column, dict):
                key_column = key_column.get("id", "") or key_column.get("label", "") or key_column.get("value", "")
            if isinstance(key_value, dict):
                key_value = key_value.get("id", "") or key_value.get("label", "") or key_value.get("value", "")
        if not sheet_id:
            return Response.error("Sheet ID is required")
        if not service_account_json:
            return Response.error("Service account JSON is required (from env)")
        if not sheet_name:
            return Response.error("Sheet name is required")
        if not key_column or not key_value:
            return Response.error("Key column and key value are required")
        range_string = f"{sheet_name}"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={API_KEY}"
        resp = requests.get(url, timeout=10)
        all_values = resp.json().get("values", [])
        if not all_values or len(all_values) < 2:
            return Response.error("Could not fetch sheet data to determine rows to delete.")
        header = all_values[0]
        if key_column not in header:
            return Response.error(f"Key column '{key_column}' not found in header: {header}")
        key_col_idx = header.index(key_column)
        rows_to_delete = []
        for i, row in enumerate(all_values[1:], start=2):
            val = row[key_col_idx] if key_col_idx < len(row) else ""
            if val == key_value:
                rows_to_delete.append(i)
        if not rows_to_delete:
            return Response.error(f"No rows found where '{key_column}' == '{key_value}'")
        # Use batchUpdate to delete rows
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        account_info = service_account_json
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
        creds.refresh(GoogleRequest())
        token = creds.token
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate"
        # Prepare delete requests (reverse order to avoid shifting rows)
        requests_body = []
        for row_num in sorted(rows_to_delete, reverse=True):
            requests_body.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": get_sheet_id(sheet_id, sheet_name),
                        "dimension": "ROWS",
                        "startIndex": row_num-1,
                        "endIndex": row_num
                    }
                }
            })
        body = {"requests": requests_body}
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        resp = requests.post(batch_url, headers=headers, json=body, timeout=30)
        if resp.status_code not in [200, 201]:
            error_detail = resp.text
            try:
                error_json = resp.json()
                error_detail = error_json.get("error", {}).get("message", resp.text)
            except:
                pass
            return Response.error(f"Failed to delete rows: {error_detail}")
        return Response(data={"message": f"Deleted {len(rows_to_delete)} row(s) where {key_column} == {key_value}."})
    except Exception as e:
        return Response.error(str(e))
