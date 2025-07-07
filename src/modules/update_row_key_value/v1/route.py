from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import requests
from urllib.parse import quote

#updated
import os

# === ENVIRONMENT VARIABLES ===
API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
SERVICE_ACCOUNT_JSON_STR = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
SERVICE_ACCOUNT_JSON = json.loads(SERVICE_ACCOUNT_JSON_STR) if SERVICE_ACCOUNT_JSON_STR else None
# === END ENVIRONMENT VARIABLES ===

def get_sheets_with_api_v4(spreadsheet_id, api_key=None):
    # Always use hardcoded API key
    api_key = HARDCODED_API_KEY
    try:
        metadata_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?key={api_key}"
        response = requests.get(metadata_url, timeout=10)
        if response.status_code != 200:
            return []
        metadata = response.json()
        sheets = metadata.get('sheets', [])
        available_sheets = []
        for sheet in sheets:
            properties = sheet.get('properties', {})
            sheet_name = properties.get('title', 'Unknown')
            sheet_id = properties.get('sheetId', 0)
            available_sheets.append({"name": sheet_name, "gid": sheet_id})
        return available_sheets
    except Exception as e:
        print(f"DEBUG: get_sheets_with_api_v4 failed: {str(e)}")
        return []

def get_sheet_header(spreadsheet_id, sheet_name, api_key):
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

@router.route("/content", methods=["POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data
        form_data = data.get("form_data", {})
        sheet_id = form_data.get("sheet_id", "")
        api_key = form_data.get("api_key", "")
        sheet_name_obj = form_data.get("sheet_name", "")
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        content_object_names = data.get("content_object_names", [])
        content_objects = []
        for content_name in content_object_names:
            cid = content_name.get("id")
            if cid == "sheet_names":
                if not sheet_id or not api_key:
                    content_objects.append({"content_object_name": "sheet_names", "data": []})
                    continue
                available_sheets = get_sheets_with_api_v4(sheet_id, api_key)
                sheet_options = []
                for sheet in available_sheets:
                    sheet_options.append({
                        "value": {"id": sheet["name"], "label": sheet["name"]},
                        "label": sheet["name"]
                    })
                content_objects.append({"content_object_name": "sheet_names", "data": sheet_options})
            elif cid in ["key_columns", "column_names"]:
                if not sheet_id or not api_key or not sheet_name:
                    content_objects.append({"content_object_name": cid, "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name, api_key)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": cid, "data": options})
            elif cid == "key_values":
                key_column = form_data.get("key_column", "")
                if isinstance(key_column, dict):
                    key_column = key_column.get("id", "") or key_column.get("label", "") or key_column.get("value", "")
                elif not isinstance(key_column, str):
                    key_column = str(key_column)
                if not sheet_id or not api_key or not sheet_name or not key_column:
                    content_objects.append({"content_object_name": "key_values", "data": []})
                    continue
                try:
                    range_string = f"{sheet_name}"
                    encoded_range = quote(range_string)
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={api_key}"
                    resp = requests.get(url, timeout=10)
                    all_values = resp.json().get("values", [])
                    if not all_values or len(all_values) < 2:
                        content_objects.append({"content_object_name": "key_values", "data": []})
                        continue
                    header = all_values[0]
                    if key_column not in header:
                        content_objects.append({"content_object_name": "key_values", "data": []})
                        continue
                    col_idx = header.index(key_column)
                    value_options = []
                    seen = set()
                    for row in all_values[1:]:
                        val = row[col_idx] if col_idx < len(row) else ""
                        if isinstance(val, dict):
                            val_id = val.get("id") or val.get("label") or val.get("value")
                        else:
                            val_id = val
                        if val_id and val_id not in seen:
                            value_options.append({"value": {"id": val_id, "label": str(val_id)}, "label": str(val_id)})
                            seen.add(val_id)
                    content_objects.append({"content_object_name": "key_values", "data": value_options})
                except Exception as e:
                    content_objects.append({"content_object_name": "key_values", "data": []})
            elif cid == "column_values":
                key_column = form_data.get("key_column", "")
                if isinstance(key_column, dict):
                    key_column = key_column.get("id", "") or key_column.get("label", "") or key_column.get("value", "")
                elif not isinstance(key_column, str):
                    key_column = str(key_column)
                if not sheet_id or not api_key or not sheet_name or not key_column:
                    content_objects.append({"content_object_name": "column_values", "data": []})
                    continue
                try:
                    range_string = f"{sheet_name}"
                    encoded_range = quote(range_string)
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={api_key}"
                    resp = requests.get(url, timeout=10)
                    all_values = resp.json().get("values", [])
                    if not all_values or len(all_values) < 2:
                        content_objects.append({"content_object_name": "column_values", "data": []})
                        continue
                    header = all_values[0]
                    if key_column not in header:
                        content_objects.append({"content_object_name": "column_values", "data": []})
                        continue
                    col_idx = header.index(key_column)
                    value_options = []
                    seen = set()
                    for row in all_values[1:]:
                        val = row[col_idx] if col_idx < len(row) else ""
                        if isinstance(val, dict):
                            val_id = val.get("id") or val.get("label") or val.get("value")
                        else:
                            val_id = val
                        if val_id and val_id not in seen:
                            value_options.append({"value": {"id": val_id, "label": str(val_id)}, "label": str(val_id)})
                            seen.add(val_id)
                    content_objects.append({"content_object_name": "column_values", "data": value_options})
                except Exception as e:
                    content_objects.append({"content_object_name": "column_values", "data": []})
            elif cid == "update_columns":
                if not sheet_id or not api_key or not sheet_name:
                    content_objects.append({"content_object_name": "update_columns", "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name, api_key)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": "update_columns", "data": options})
            elif cid == "column_names":
                if not sheet_id or not api_key or not sheet_name:
                    content_objects.append({"content_object_name": "column_names", "data": []})
                    continue
                header = get_sheet_header(sheet_id, sheet_name, api_key)
                options = [{"value": {"id": col, "label": col}, "label": col} for col in header]
                content_objects.append({"content_object_name": "column_names", "data": options})
        return Response(data={"content_objects": content_objects})
    except Exception as e:
        return Response(data={"content_objects": []})

@router.route("/execute", methods=["POST"])
def execute():
    try:
        request = Request(flask_request)
        data = request.data
        sheet_id = data.get("sheet_id", "")
        api_key = data.get("api_key", "")
        service_account_json = data.get("service_account_json", "")
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
        if isinstance(key_value_obj, dict):
            key_value = key_value_obj.get("id", "") or key_value_obj.get("label", "") or key_value_obj.get("value", "")
        elif isinstance(key_value_obj, str):
            key_value = key_value_obj
        if not sheet_id:
            return Response.error("Sheet ID is required")
        if not service_account_json:
            return Response.error("Service account JSON is required")
        if not sheet_name:
            return Response.error("Sheet name is required")
        if not row_data:
            return Response.error("Row data is required")
        if not key_column or not key_value:
            return Response.error("Key column and key value are required")
        range_string = f"{sheet_name}"
        encoded_range = quote(range_string)
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={api_key}"
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
        import json
        if isinstance(service_account_json, str):
            account_info = json.loads(service_account_json)
        else:
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
