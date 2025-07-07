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

def get_google_credentials(service_account_json=None):
    """
    Get Google service account credentials from complete JSON.
    """
    try:
        if service_account_json:
            print("DEBUG: Using service account credentials from JSON")
            
            # Parse the JSON string if it's a string
            if isinstance(service_account_json, str):
                account_info = json.loads(service_account_json)
            else:
                account_info = service_account_json
            
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file"
            ]
            
            credentials = service_account.Credentials.from_service_account_info(
                account_info, scopes=scopes
            )
            return credentials
        else:
            print("DEBUG: No service account JSON provided")
            return None
            
    except Exception as e:
        print(f"DEBUG: Error getting service account credentials: {str(e)}")
        return None

def get_google_service(service_account_json=None):
    """
    Get Google Sheets service using service account credentials.
    """
    if not GOOGLE_LIBS_AVAILABLE:
        print("DEBUG: Google API libraries not available")
        return None
        
    credentials = get_google_credentials(service_account_json)
    if credentials:
        try:
            service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
            print("DEBUG: Successfully created Google Sheets service with service account")
            return service
        except Exception as e:
            print(f"DEBUG: Error creating Google service: {str(e)}")
            return None
    return None

def add_row_with_service_account(spreadsheet_id, sheet_name, row_values, target_row, service_account_json):
    """
    Add row using Google Sheets API v4 with service account authentication (direct HTTP).
    Always appends to the end of the sheet, ignoring target_row.
    """
    try:
        # 1. Get access token from service account JSON
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request

        # Parse JSON if needed
        if isinstance(service_account_json, str):
            account_info = json.loads(service_account_json)
        else:
            account_info = service_account_json

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
        creds.refresh(Request())
        token = creds.token

        # 2. Prepare the API call
        # Always append to the end: use only the sheet name as the range
        range_part = f"{sheet_name}"
        range_part_encoded = quote(range_part, safe='')
        url = (
            f"https://sheets.googleapis.com/v4/spreadsheets/"
            f"{spreadsheet_id}/values/{range_part_encoded}:append"
            "?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        body = {
            "values": [row_values]
        }

        # 3. Make the request
        resp = requests.post(url, headers=headers, json=body)
        if resp.status_code not in [200, 201]:
            return False, f"Failed to add row: {resp.status_code} {resp.text}"

        result = resp.json()
        updated_range = result.get("updates", {}).get("updatedRange", range_part)
        updated_cells = result.get("updates", {}).get("updatedCells", 0)

        return True, f"Successfully added row at {updated_range} ({updated_cells} cells updated)"

    except Exception as e:
        error_msg = f"Failed to add row using service account: {str(e)}"
        print(f"DEBUG: {error_msg}")
        print(f"DEBUG: Service account add row traceback: {traceback.format_exc()}")
        return False, error_msg

def get_sheets_with_api_v4(spreadsheet_id):
    """
    Use Google Sheets API v4 to get sheet information.
    """
    try:
        print(f"DEBUG: get_sheets_with_api_v4 called with spreadsheet_id={spreadsheet_id}, api_key={'[PROVIDED]' if API_KEY else '[MISSING]'}")
        
        if not API_KEY:
            print("DEBUG: API key is missing")
            return []
        
        # Official API v4 endpoint for getting spreadsheet metadata
        metadata_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?key={API_KEY}"
        
        print(f"DEBUG: Fetching metadata from: {metadata_url}")
        
        response = requests.get(metadata_url, timeout=10)
        print(f"DEBUG: API response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: API returned non-200 status: {response.status_code}")
            print(f"DEBUG: API response text: {response.text}")
            return []
        
        response.raise_for_status()
        
        metadata = response.json()
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

def find_next_empty_row(spreadsheet_id, sheet_name, api_key):
    """
    Find the next empty row in the sheet by checking existing data.
    """
    try:
        # Get existing data to find the last used row
        range_string = f"{sheet_name}!A:A"  # Check column A for data
        encoded_range = quote(range_string)
        
        # Official API v4 endpoint for getting values
        data_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={api_key}"
        
        response = requests.get(data_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        values = data.get('values', [])
        
        # Next empty row is after the last row with data
        next_row = len(values) + 1
        print(f"DEBUG: Found {len(values)} rows with data, next empty row is {next_row}")
        return next_row
        
    except Exception as e:
        print(f"DEBUG: Error finding next empty row: {str(e)}")
        return 1  # Default to row 1 if we can't determine

def add_row_to_sheet(spreadsheet_id, sheet_name, api_key, row_values, target_row=None):
    """
    Add a row to Google Sheet using official API v4 endpoints.
    Uses PUT /v4/spreadsheets/{spreadsheetId}/values/{range} for updating.
    """
    try:
        if not api_key or not sheet_name or not row_values:
            return False, "Missing required parameters"
        
        # Determine target row
        if target_row is None:
            target_row = find_next_empty_row(spreadsheet_id, sheet_name, api_key)
        
        # Prepare the range for the target row
        range_name = f"{sheet_name}!A{target_row}"
        encoded_range = quote(range_name)
        
        # Official API v4 endpoint for updating values
        update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}"
        
        # Prepare the payload according to API documentation
        payload = {
            "values": [row_values],
            "majorDimension": "ROWS"
        }
        
        params = {
            "key": api_key,
            "valueInputOption": "USER_ENTERED"
        }
        
        print(f"DEBUG: Adding row to {range_name}")
        print(f"DEBUG: Update URL: {update_url}")
        print(f"DEBUG: Payload: {payload}")
        print(f"DEBUG: Params: {params}")
        
        # Use PUT method as specified in official documentation
        response = requests.put(
            update_url,
            json=payload,
            params=params,
            timeout=30
        )
        
        print(f"DEBUG: API response status: {response.status_code}")
        print(f"DEBUG: API response text: {response.text}")
        
        if response.status_code not in [200, 201]:
            error_detail = ""
            try:
                error_json = response.json()
                error_detail = error_json.get("error", {}).get("message", response.text)
            except:
                error_detail = response.text
            
            print(f"DEBUG: Add row failed with status {response.status_code}: {error_detail}")
            return False, f"Failed to add row: {error_detail}"
        
        result = response.json()
        print(f"DEBUG: Add row successful: {result}")
        
        updated_cells = result.get("updatedCells", 0)
        updated_range = result.get("updatedRange", range_name)
        
        return True, f"Successfully added row at {updated_range} ({updated_cells} cells updated)"
        
    except Exception as e:
        error_msg = f"Failed to add row to sheet: {str(e)}"
        print(f"DEBUG: {error_msg}")
        print(f"DEBUG: Add row traceback: {traceback.format_exc()}")
        return False, error_msg

@router.route("/content", methods=["POST"])
def content():
    """
    Provide dynamic content for the module UI.
    Fetches sheet information from Google Sheets using API key and sheet ID.
    """
    try:
        print("DEBUG: add_row_to_sheet /content called")

        # Parse the request
        request = Request(flask_request)
        data = request.data

        print(f"DEBUG: Parsed data = {data}")

        # Get required parameters from form_data
        form_data = data.get("form_data", {})
        sheet_id = form_data.get("sheet_id", "")
        sheet_name_obj = form_data.get("sheet_name", "")
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj

        # Get requested content objects
        content_object_names = data.get("content_object_names", [])
        content_objects = []

        print(f"DEBUG: Content object names requested = {content_object_names}")
        print(f"DEBUG: sheet_id = {sheet_id}")
        print(f"DEBUG: api_key = {'[PROVIDED]' if API_KEY else '[NOT PROVIDED]'}")
        print(f"DEBUG: service_account_json = {'[PROVIDED]' if SERVICE_ACCOUNT_JSON else '[NOT PROVIDED]'}")

        # Process each requested content object
        for content_name in content_object_names:
            if content_name.get("id") == "sheet_names":
                print("DEBUG: Processing sheet_names content object")
                
                # If no sheet_id or api_key, return empty list
                if not sheet_id or not API_KEY:
                    print("DEBUG: Missing sheet_id or api_key, returning empty sheet_names")
                    content_objects.append({
                        "content_object_name": "sheet_names",
                        "data": []
                    })
                    continue

                # Get sheet information using API v4 (still use API key for reading metadata)
                print("DEBUG: Fetching sheets using API v4")
                available_sheets = get_sheets_with_api_v4(sheet_id)
                
                # Format for StackSync
                sheet_options = []
                for sheet in available_sheets:
                    sheet_options.append({
                        "value": {"id": sheet["name"], "label": sheet["name"]},
                        "label": sheet["name"]
                    })
                
                print(f"DEBUG: Formatted {len(sheet_options)} sheet options")
                
                content_objects.append({
                    "content_object_name": "sheet_names",
                    "data": sheet_options
                })
            elif content_name.get("id") == "column_names":
                print("DEBUG: Processing column_names content object")
                # If no sheet_id or sheet_name, return empty list
                if not sheet_id or not sheet_name:
                    print("DEBUG: Missing sheet_id or sheet_name, returning empty column_names")
                    content_objects.append({
                        "content_object_name": "column_names",
                        "data": []
                    })
                    continue
                # Get column names (header) from the sheet using API key
                header = []
                try:
                    range_string = f"{sheet_name}!1:1"
                    encoded_range = quote(range_string)
                    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?key={API_KEY}"
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json().get("values", [])
                        if data:
                            header = data[0]
                except Exception as e:
                    print(f"DEBUG: Failed to fetch column names: {str(e)}")
                # Format for StackSync
                column_options = []
                for col in header:
                    column_options.append({
                        "value": {"id": col, "label": col},
                        "label": col
                    })
                print(f"DEBUG: Formatted {len(column_options)} column options")
                content_objects.append({
                    "content_object_name": "column_names",
                    "data": column_options
                })

        print(f"DEBUG: Returning {len(content_objects)} content objects")

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        print(f"DEBUG: /content error = {e}")
        print(f"DEBUG: Full traceback = {traceback.format_exc()}")
        return Response(data={"content_objects": []})

@router.route("/execute", methods=["POST"])
def execute():
    """
    Execute the add row operation.
    Adds a new row with data to the specified Google Sheet.
    """
    try:
        print("DEBUG: add_row_to_sheet /execute called")
        
        # Parse the request
        request = Request(flask_request)
        data = request.data

        print(f"DEBUG: Parsed data = {data}")
        
        # Get required parameters
        sheet_id = data.get("sheet_id", "")
        service_account_json = SERVICE_ACCOUNT_JSON
        sheet_name_obj = data.get("sheet_name", "")
        row_data = data.get("row_data", [])
        target_row = data.get("target_row")
        
        # Handle sheet_name - could be string, object from dropdown, or direct value
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        
        print(f"DEBUG: Raw sheet_name_obj = {sheet_name_obj}")
        print(f"DEBUG: Processed sheet_name = {sheet_name}")
        print(f"DEBUG: row_data = {row_data}")
        print(f"DEBUG: target_row = {target_row}")
        print(f"DEBUG: service_account_json = {'[PROVIDED]' if service_account_json else '[NOT PROVIDED]'}")
        
        if not sheet_id:
            return Response.error("Sheet ID is required")
        
        if not service_account_json:
            return Response.error("Service account JSON is required (from env)")
        
        if not sheet_name:
            return Response.error("Sheet name is required")
        
        if not row_data:
            return Response.error("Row data is required")

        # Extract values from row_data array
        row_values = []
        for item in row_data:
            if isinstance(item, dict):
                column_value = item.get("column_value", "")
                row_values.append(str(column_value))
            elif isinstance(item, str):
                row_values.append(item)
        
        if not row_values:
            return Response.error("No valid row data provided")
        
        print(f"DEBUG: Processed row_values = {row_values}")

        # Add row to sheet using service account
        success, message = add_row_with_service_account(
            spreadsheet_id=sheet_id,
            sheet_name=sheet_name,
            row_values=row_values,
            target_row=target_row,
            service_account_json=service_account_json
        )
        
        if not success:
            return Response.error(message)
        
        # Create response
        result = {
            "sheet_id": sheet_id,
            "sheet_name": sheet_name,
            "target_row": target_row,
            "row_values": row_values,
            "columns_added": len(row_values),
            "message": message
        }
        
        return Response(
            data=result,
            metadata={
                "affected_records": 1,
                "message": f"Successfully added row to sheet '{sheet_name}' with {len(row_values)} columns"
            }
        )
                
    except Exception as e:
        print(f"DEBUG: /execute error = {e}")
        print(f"DEBUG: Execute traceback = {traceback.format_exc()}")
        return Response.error(str(e))
