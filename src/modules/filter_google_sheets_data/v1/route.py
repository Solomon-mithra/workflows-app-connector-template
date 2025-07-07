from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import requests
import traceback
from urllib.parse import quote

print("DEBUG: filter_google_sheets_data/v1/route.py is being loaded!")

import os

# === ENVIRONMENT VARIABLES ===
API_KEY = os.environ.get("GOOGLE_SHEETS_API_KEY")
# === END ENVIRONMENT VARIABLES ===

def get_sheets_with_api_v4(spreadsheet_id, api_key=None):
    """
    Use Google Sheets API v4 to get sheet information.
    """
    try:
        print(f"DEBUG: get_sheets_with_api_v4 called with spreadsheet_id={spreadsheet_id}, api_key={'[PROVIDED]' if api_key else '[MISSING]'}")
        
        if not api_key:
            print("DEBUG: API key is missing")
            return []
        
        # Get spreadsheet metadata to list all sheets
        metadata_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?key={api_key}"
        
        print(f"DEBUG: Fetching metadata from Sheets API v4: {metadata_url}")
        
        response = requests.get(metadata_url, timeout=10)
        print(f"DEBUG: API response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: API returned non-200 status: {response.status_code}")
            print(f"DEBUG: API response text: {response.text}")
            return []
        
        response.raise_for_status()
        
        metadata = response.json()
        print(f"DEBUG: API response JSON keys: {list(metadata.keys())}")
        
        sheets = metadata.get('sheets', [])
        print(f"DEBUG: Found {len(sheets)} sheets in metadata")
        
        available_sheets = []
        for i, sheet in enumerate(sheets):
            properties = sheet.get('properties', {})
            sheet_name = properties.get('title', 'Unknown')
            sheet_id = properties.get('sheetId', 0)
            
            available_sheets.append({
                "name": sheet_name,
                "gid": sheet_id
            })
            print(f"DEBUG: Sheet {i+1}: {sheet_name} (GID: {sheet_id})")
        
        print(f"DEBUG: get_sheets_with_api_v4 returning {len(available_sheets)} sheets")
        return available_sheets
        
    except requests.RequestException as e:
        print(f"DEBUG: Sheets API v4 failed with RequestException: {str(e)}")
        print(f"DEBUG: RequestException traceback: {traceback.format_exc()}")
        return []
    except Exception as e:
        print(f"DEBUG: Sheets API v4 failed with general Exception: {str(e)}")
        print(f"DEBUG: General exception traceback: {traceback.format_exc()}")
        return []

def get_sheet_data_with_api_v4(spreadsheet_id, sheet_name, api_key):
    """
    Get sheet data using Sheets API v4.
    """
    try:
        if not api_key:
            return None
        
        # Get all data from the sheet
        range_string = f"{sheet_name}!A1:ZZ1000"
        
        print(f"DEBUG: Using range string: {range_string}")
        
        # URL encode the range to handle spaces and special characters
        encoded_range = quote(range_string)
        
        data_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={api_key}"
        
        print(f"DEBUG: Fetching data from Sheets API v4: {data_url}")
        
        response = requests.get(data_url, headers={}, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        values = data.get('values', [])
        
        print(f"DEBUG: API v4 returned {len(values)} rows")
        return values
        
    except requests.RequestException as e:
        print(f"DEBUG: Sheets API v4 data fetch failed: {str(e)}")
        return None

def filter_data_by_value(data_rows, headers, filter_value):
    """
    Filter rows that contain the specified value in any column.
    """
    if not filter_value or not data_rows:
        return data_rows
    
    filter_value_lower = str(filter_value).lower()
    filtered_rows = []
    
    for row in data_rows:
        # Check if filter value exists in any cell of the row
        row_contains_value = False
        for cell_value in row:
            if filter_value_lower in str(cell_value).lower():
                row_contains_value = True
                break
        
        if row_contains_value:
            filtered_rows.append(row)
    
    print(f"DEBUG: Filtered {len(data_rows)} rows down to {len(filtered_rows)} rows containing '{filter_value}'")
    return filtered_rows

@router.route("/content", methods=["POST"])
def content():
    """
    Provide dynamic content for the module UI.
    Fetches sheet information from Google Sheets using API key and sheet ID.
    """
    try:
        print("DEBUG: filter_google_sheets_data /content called")

        # Parse the request
        request = Request(flask_request)
        data = request.data

        print(f"DEBUG: Parsed data = {data}")

        # Get required parameters from form_data
        form_data = data.get("form_data", {})
        sheet_id = form_data.get("sheet_id", "")
        api_key = form_data.get("api_key", "")

        # Get requested content objects
        content_object_names = data.get("content_object_names", [])
        content_objects = []

        print(f"DEBUG: Content object names requested = {content_object_names}")
        print(f"DEBUG: sheet_id = {sheet_id}")
        print(f"DEBUG: api_key = {'[PROVIDED]' if api_key else '[NOT PROVIDED]'}")

        # Process each requested content object
        for content_name in content_object_names:
            if content_name.get("id") == "sheet_names":
                print("DEBUG: Processing sheet_names content object")
                
                # If no sheet_id or api_key, return empty list
                if not sheet_id or not api_key:
                    print("DEBUG: Missing sheet_id or api_key, returning empty sheet_names")
                    content_objects.append({
                        "content_object_name": "sheet_names",
                        "data": []
                    })
                    continue

                # Get sheet information using API v4
                print("DEBUG: Fetching sheets using API v4")
                available_sheets = get_sheets_with_api_v4(sheet_id, api_key)
                
                # Format for StackSync - using the documentation format
                sheet_options = []
                for sheet in available_sheets:
                    sheet_options.append({
                        "value": {"id": sheet["name"], "label": sheet["name"]},
                        "label": sheet["name"]
                    })
                
                print(f"DEBUG: Formatted {len(sheet_options)} sheet options")
                print(f"DEBUG: Sheet options = {sheet_options}")
                
                content_objects.append({
                    "content_object_name": "sheet_names",
                    "data": sheet_options
                })

        print(f"DEBUG: Returning {len(content_objects)} content objects")
        print(f"DEBUG: Content objects = {content_objects}")

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        print(f"DEBUG: /content error = {e}")
        print(f"DEBUG: Full traceback = {traceback.format_exc()}")
        return Response(data={"content_objects": []})

@router.route("/execute", methods=["POST"])
def execute():
    """
    Execute the Google Sheets filtering operation.
    Fetches data from specified sheet and filters rows containing the specified value.
    """
    try:
        print("DEBUG: filter_google_sheets_data /execute called")
        
        # Parse the request
        request = Request(flask_request)
        data = request.data

        print(f"DEBUG: Parsed data = {data}")
        
        # Get required parameters
        sheet_id = data.get("sheet_id", "")
        api_key = data.get("api_key", "")
        sheet_name_obj = data.get("sheet_name", "")
        filter_value = data.get("filter_value", "")
        
        # Handle sheet_name - could be string, object from dropdown, or direct value
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        
        print(f"DEBUG: Raw sheet_name_obj = {sheet_name_obj}")
        print(f"DEBUG: Processed sheet_name = {sheet_name}")
        print(f"DEBUG: filter_value = {filter_value}")
        
        if not sheet_id:
            return Response.error("Sheet ID is required")
        
        if not api_key:
            return Response.error("API key is required")
        
        if not sheet_name:
            return Response.error("Sheet name is required")
        
        if not filter_value:
            return Response.error("Filter value is required")

        print(f"DEBUG: sheet_id = {sheet_id}")
        print(f"DEBUG: sheet_name = {sheet_name}")
        print(f"DEBUG: api_key = [PROVIDED]")
        print(f"DEBUG: filter_value = {filter_value}")

        # Get data using API v4
        api_v4_data = get_sheet_data_with_api_v4(sheet_id, sheet_name, api_key)
        
        if not api_v4_data:
            return Response.error("Failed to fetch data from Google Sheet")
        
        # Convert to structured format
        if len(api_v4_data) < 1:
            return Response.error("No data found in the sheet")
        
        # First row as headers
        headers = api_v4_data[0]
        all_data_rows = api_v4_data[1:]
        
        # Filter rows containing the specified value
        filtered_rows = filter_data_by_value(all_data_rows, headers, filter_value)
        
        # Convert to JSON format
        structured_data = []
        for i, row in enumerate(filtered_rows):
            row_dict = {}
            for j, header in enumerate(headers):
                value = row[j] if j < len(row) else ""
                row_dict[header] = value
            row_dict["_row_number"] = all_data_rows.index(row) + 2  # +2 because first row is headers
            structured_data.append(row_dict)
        
        print(f"DEBUG: Processed {len(structured_data)} filtered rows from {len(all_data_rows)} total rows")
        
        # Create response
        result = {
            "sheet_id": sheet_id,
            "sheet_name": sheet_name,
            "filter_value": filter_value,
            "total_available_rows": len(all_data_rows),
            "filtered_rows": len(filtered_rows),
            "headers": headers,
            "data": structured_data,
            "total_records": len(structured_data),
            "total_fields": len(headers)
        }
        
        return Response(
            data=result,
            metadata={
                "affected_records": len(structured_data),
                "message": f"Successfully filtered {len(structured_data)} records from sheet '{sheet_name}' containing '{filter_value}'"
            }
        )
                
    except Exception as e:
        print(f"DEBUG: /execute error = {e}")
        print(f"DEBUG: Execute traceback = {traceback.format_exc()}")
        return Response.error(str(e))
