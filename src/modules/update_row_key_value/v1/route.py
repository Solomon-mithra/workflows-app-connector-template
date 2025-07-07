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
        row_data = data.get("row_data", [])
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        key_column = ""
        if isinstance(key_column_obj, dict):
            key_column = key_column_obj.get("id", "") or key_column_obj.get("label", "") or key_column_obj.get("value", "")
        elif isinstance(key_column_obj, str):
            key_column = key_column_obj
        key_value = ""
        # Now key_value is always a string
        if isinstance(key_value_obj, str):
            key_value = key_value_obj
        elif isinstance(key_value_obj, dict):
            key_value = key_value_obj.get("id", "") or key_value_obj.get("label", "") or key_value_obj.get("value", "")
        else:
            key_value = str(key_value_obj)
        if not sheet_id:
            return Response.error("Sheet ID is required")
        if not service_account_json:
            return Response.error("Service account JSON is required (from env)")
        if not sheet_name:
            return Response.error("Sheet name is required")
        if not row_data:
            return Response.error("Row data is required")
        if not key_column or not key_value:
            return Response.error("Key column and key value are required")
        range_string = f"{sheet_name}"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={API_KEY}"
        resp = requests.get(url, timeout=10)
        all_values = resp.json().get("values", [])
        if not all_values or len(all_values) < 2:
            return Response.error("Could not fetch sheet data to determine rows to update.")
        header = all_values[0]
        if key_column not in header:
            return Response.error(f"Key column '{key_column}' not found in header: {header}")
        key_col_idx = header.index(key_column)
        col_name_to_idx = {col: idx for idx, col in enumerate(header)}
        rows_to_update = []
        for i, row in enumerate(all_values[1:], start=2):
            val = row[key_col_idx] if key_col_idx < len(row) else ""
            if val == key_value:
                rows_to_update.append((i, row))
        if not rows_to_update:
            return Response.error(f"No rows found where '{key_column}' == '{key_value}'")
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        account_info = service_account_json
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
        creds.refresh(GoogleRequest())
        token = creds.token
        batch_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values:batchUpdate"
        data_updates = []
        for row_num, row in rows_to_update:
            updated_row = list(row) + [""] * (len(header) - len(row))
            for item in row_data:
                col_name = item.get("column_name", "")
                col_value = item.get("column_value", "")
                if isinstance(col_name, dict):
                    col_name = col_name.get("id", "") or col_name.get("label", "") or col_name.get("value", "")
                if col_name in col_name_to_idx:
                    updated_row[col_name_to_idx[col_name]] = col_value
            for item in row_data:
                col_name = item.get("column_name", "")
                if isinstance(col_name, dict):
                    col_name = col_name.get("id", "") or col_name.get("label", "") or col_name.get("value", "")
                if col_name in col_name_to_idx:
                    col_idx = col_name_to_idx[col_name]
                    col_letter = chr(col_idx + ord('A'))
                    range_name = f"{sheet_name}!{col_letter}{row_num}"
                    data_updates.append({
                        "range": range_name,
                        "majorDimension": "ROWS",
                        "values": [[updated_row[col_idx]]]
                    })
        if not data_updates:
            return Response.error("No columns to update.")
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": data_updates,
            "includeValuesInResponse": False
        }
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
            return Response.error(f"Failed to update rows: {error_detail}")
        result = resp.json()
        updated_rows = len(rows_to_update)
        updated_cells = len(data_updates)
        return Response(
            data={
                "sheet_id": sheet_id,
                "sheet_name": sheet_name,
                "key_column": key_column,
                "key_value": key_value,
                "rows_updated": updated_rows,
                "cells_updated": updated_cells,
                "message": f"Updated {updated_rows} row(s) and {updated_cells} cell(s) where {key_column} == {key_value}."
            },
            metadata={
                "affected_records": updated_rows,
                "message": f"Successfully updated {updated_rows} row(s) in sheet '{sheet_name}' where {key_column} == {key_value}"
            }
        )
    except Exception as e:
        return Response.error(str(e))
