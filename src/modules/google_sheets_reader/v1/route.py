from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router
import requests
import csv
import io
import traceback
from urllib.parse import quote

print("DEBUG: google_sheets_reader/v1/route.py is being loaded!")

def get_sheets_with_api_v4(spreadsheet_id, api_key):
    """
    Use Google Sheets API v4 to get sheet information.
    """
    try:
        print(f"DEBUG: get_sheets_with_api_v4 called with spreadsheet_id={spreadsheet_id}, api_key={'[PROVIDED]' if api_key else '[MISSING]'}")
        
        if not api_key:
            print("DEBUG: API key is missing")
            return []  # Return empty list instead of Response.error
        
        # Get spreadsheet metadata to list all sheets
        metadata_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?key={api_key}"
        
        print(f"DEBUG: Fetching metadata from Sheets API v4: {metadata_url}")
        
        response = requests.get(metadata_url, timeout=10)
        print(f"DEBUG: API response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: API returned non-200 status: {response.status_code}")
            print(f"DEBUG: API response text: {response.text}")
            return []  # Return empty list instead of raising error
        
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
        import traceback
        print(f"DEBUG: RequestException traceback: {traceback.format_exc()}")
        return []  # Return empty list instead of Response.error
    except Exception as e:
        print(f"DEBUG: Sheets API v4 failed with general Exception: {str(e)}")
        import traceback
        print(f"DEBUG: General exception traceback: {traceback.format_exc()}")
        return []  # Return empty list instead of Response.error

def get_sheet_ranges(spreadsheet_id, sheet_name, api_key):
    """
    Get available cell references from a sheet for dynamic population.
    Returns individual cell references like A1, A2, B3, etc. based on actual data.
    """
    try:
        if not api_key or not sheet_name:
            return []
        
        # First, get basic sheet data to determine dimensions
        encoded_range = quote(f"{sheet_name}!A1:ZZ1000")
        data_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={api_key}"
        
        response = requests.get(data_url, headers={}, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        values = data.get('values', [])
        
        if not values:
            return []
        
        # Determine the actual data dimensions
        max_row = len(values)
        max_col = 0
        for row in values:
            if len(row) > max_col:
                max_col = len(row)
        
        print(f"DEBUG: Sheet dimensions: {max_row} rows, {max_col} columns")
        
        # Helper function to convert column number to letter
        def col_num_to_letter(col_num):
            if col_num <= 26:
                return chr(ord('A') + col_num - 1)
            else:
                # For columns beyond Z, use AA, AB, etc.
                first_letter = chr(ord('A') + (col_num - 1) // 26 - 1)
                second_letter = chr(ord('A') + (col_num - 1) % 26)
                return first_letter + second_letter
        
        # Generate cell reference options
        ranges = []
        
        # Add "all" option first
        ranges.append({
            "value": "all",
            "label": "All data"
        })
        
        # Generate individual cell references based on actual data
        if max_col > 0 and max_row > 0:
            # Limit to reasonable number of cells to avoid overwhelming the UI
            max_cells_to_show = 50
            cell_count = 0
            
            # Generate cell references row by row, column by column
            for row in range(1, min(max_row + 1, 21)):  # Limit to first 20 rows
                for col in range(1, min(max_col + 1, 11)):  # Limit to first 10 columns
                    if cell_count >= max_cells_to_show:
                        break
                    
                    col_letter = col_num_to_letter(col)
                    cell_ref = f"{col_letter}{row}"
                    
                    # Add descriptive labels for common cells
                    if row == 1:
                        label = f"{cell_ref} (Header row, Column {col_letter})"
                    elif row == 2:
                        label = f"{cell_ref} (First data row, Column {col_letter})"
                    else:
                        label = f"{cell_ref} (Row {row}, Column {col_letter})"
                    
                    ranges.append({
                        "value": cell_ref,
                        "label": label
                    })
                    cell_count += 1
                
                if cell_count >= max_cells_to_show:
                    break
            
            # Add some key corner cells if sheet is large
            if max_row > 20 or max_col > 10:
                last_col_letter = col_num_to_letter(min(max_col, 26))
                
                # Add last row, first column
                ranges.append({
                    "value": f"A{max_row}",
                    "label": f"A{max_row} (Last row, Column A)"
                })
                
                # Add last column, first row
                ranges.append({
                    "value": f"{last_col_letter}1",
                    "label": f"{last_col_letter}1 (Header row, Last column)"
                })
                
                # Add last cell with data
                ranges.append({
                    "value": f"{last_col_letter}{max_row}",
                    "label": f"{last_col_letter}{max_row} (Last cell with data)"
                })
        
        print(f"DEBUG: Generated {len(ranges)} cell reference options")
        return ranges
        
    except Exception as e:
        print(f"DEBUG: get_sheet_ranges failed: {str(e)}")
        import traceback
        print(f"DEBUG: get_sheet_ranges traceback: {traceback.format_exc()}")
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

def get_row_options(spreadsheet_id, sheet_name, api_key):
    """
    Get available row count options based on actual data in the sheet.
    Returns options like "All rows", "First 10 rows", "First 50 rows", etc.
    """
    try:
        if not api_key or not sheet_name:
            return []
        
        # Get basic sheet data to determine row count
        encoded_range = quote(f"{sheet_name}!A1:ZZ1000")
        data_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?key={api_key}"
        
        response = requests.get(data_url, headers={}, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        values = data.get('values', [])
        
        if not values:
            return []
        
        # Get actual row count (excluding header)
        total_rows = len(values) - 1  # Subtract 1 for header row
        
        print(f"DEBUG: Sheet has {total_rows} data rows (plus header)")
        
        # Generate row options
        options = []
        
        # Always add "All rows" option
        options.append({
            "value": "all",
            "label": f"All rows ({total_rows} rows)"
        })
        
        # Add specific row count options based on actual data
        row_counts = [5, 10, 25, 50, 100, 250, 500]
        
        for count in row_counts:
            if count < total_rows:
                options.append({
                    "value": str(count),
                    "label": f"First {count} rows"
                })
            elif count == total_rows:
                options.append({
                    "value": str(count),
                    "label": f"All {count} rows"
                })
        
        # Add custom options for large datasets
        if total_rows > 500:
            options.append({
                "value": "1000",
                "label": "First 1000 rows"
            })
        
        print(f"DEBUG: Generated {len(options)} row options")
        return options
        
    except Exception as e:
        print(f"DEBUG: get_row_options failed: {str(e)}")
        return []

@router.route("/content", methods=["POST"])
def content():
    """
    Provide dynamic content for the module UI.
    Fetches sheet information from Google Sheets using API key and sheet ID.
    """
    try:
        print("DEBUG: google_sheets_reader /content called")

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
                
            elif content_name.get("id") == "row_options":
                print("DEBUG: Processing row_options content object")
                
                # Need sheet_id, api_key, and sheet_name for row options
                sheet_name_obj = form_data.get("sheet_name", "")
                
                # Handle sheet_name - could be string, object from dropdown, or direct value
                sheet_name = ""
                if isinstance(sheet_name_obj, dict):
                    sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
                elif isinstance(sheet_name_obj, str):
                    sheet_name = sheet_name_obj
                
                print(f"DEBUG: sheet_name for row options = {sheet_name}")
                
                if not sheet_id or not api_key or not sheet_name:
                    print("DEBUG: Missing sheet_id, api_key, or sheet_name, returning empty row_options")
                    content_objects.append({
                        "content_object_name": "row_options",
                        "data": []
                    })
                    continue
                
                # Get row options
                print("DEBUG: Fetching row options")
                available_rows = get_row_options(sheet_id, sheet_name, api_key)
                
                # Format for StackSync
                row_options = []
                for row_item in available_rows:
                    row_options.append({
                        "value": {"id": row_item["value"], "label": row_item["label"]},
                        "label": row_item["label"]
                    })
                
                print(f"DEBUG: Formatted {len(row_options)} row options")
                print(f"DEBUG: Row options = {row_options}")
                
                content_objects.append({
                    "content_object_name": "row_options",
                    "data": row_options
                })
                
            elif content_name.get("id") == "sheet_ranges":
                print("DEBUG: Processing sheet_ranges content object")
                
                # Need sheet_id, api_key, and sheet_name for ranges
                sheet_name_obj = form_data.get("sheet_name", "")
                
                # Handle sheet_name - could be string, object from dropdown, or direct value
                sheet_name = ""
                if isinstance(sheet_name_obj, dict):
                    sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
                elif isinstance(sheet_name_obj, str):
                    sheet_name = sheet_name_obj
                
                print(f"DEBUG: sheet_name for ranges = {sheet_name}")
                
                if not sheet_id or not api_key or not sheet_name:
                    print("DEBUG: Missing sheet_id, api_key, or sheet_name, returning empty sheet_ranges")
                    content_objects.append({
                        "content_object_name": "sheet_ranges",
                        "data": []
                    })
                    continue
                
                # Get range information
                print("DEBUG: Fetching sheet ranges")
                available_ranges = get_sheet_ranges(sheet_id, sheet_name, api_key)
                
                # Format for StackSync
                range_options = []
                for range_item in available_ranges:
                    range_options.append({
                        "value": {"id": range_item["value"], "label": range_item["label"]},
                        "label": range_item["label"]
                    })
                
                print(f"DEBUG: Formatted {len(range_options)} range options")
                print(f"DEBUG: Range options = {range_options}")
                
                content_objects.append({
                    "content_object_name": "sheet_ranges",
                    "data": range_options
                })

        print(f"DEBUG: Returning {len(content_objects)} content objects")
        print(f"DEBUG: Content objects = {content_objects}")

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        print(f"DEBUG: /content error = {e}")
        import traceback
        print(f"DEBUG: Full traceback = {traceback.format_exc()}")
        return Response(data={"content_objects": []})

@router.route("/execute", methods=["POST"])
def execute():
    """
    Execute the Google Sheets reading operation.
    Fetches data from specified sheet using API key and sheet ID.
    """
    try:
        print("DEBUG: google_sheets_reader /execute called")
        
        # Parse the request
        request = Request(flask_request)
        data = request.data

        print(f"DEBUG: Parsed data = {data}")
        
        # Get required parameters
        sheet_id = data.get("sheet_id", "")
        api_key = data.get("api_key", "")
        sheet_name_obj = data.get("sheet_name", "")
        num_rows_obj = data.get("num_rows", "all")
        
        # Handle sheet_name - could be string, object from dropdown, or direct value
        sheet_name = ""
        if isinstance(sheet_name_obj, dict):
            # StackSync format: {"id": "sheet_name", "label": "sheet_name"}
            sheet_name = sheet_name_obj.get("id", "") or sheet_name_obj.get("label", "") or sheet_name_obj.get("value", "")
        elif isinstance(sheet_name_obj, str):
            sheet_name = sheet_name_obj
        
        # Handle num_rows - could be string, object from dropdown, or direct value
        num_rows = "all"
        if isinstance(num_rows_obj, dict):
            print(f"DEBUG: num_rows_obj is dict: {num_rows_obj}")
            # StackSync format uses 'id' key directly
            num_rows = num_rows_obj.get("id", "all")
            print(f"DEBUG: Extracted num_rows from dict.id: {num_rows}")
        elif isinstance(num_rows_obj, str) and num_rows_obj:
            num_rows = num_rows_obj
            print(f"DEBUG: num_rows_obj is string: {num_rows}")
        else:
            print(f"DEBUG: num_rows_obj is other type: {type(num_rows_obj)} = {num_rows_obj}")
        
        print(f"DEBUG: Raw sheet_name_obj = {sheet_name_obj}")
        print(f"DEBUG: Processed sheet_name = {sheet_name}")
        print(f"DEBUG: Raw num_rows_obj = {num_rows_obj}")
        print(f"DEBUG: Processed num_rows = {num_rows}")
        
        if not sheet_id:
            return Response.error("Sheet ID is required")
        
        if not api_key:
            return Response.error("API key is required")
        
        if not sheet_name:
            return Response.error("Sheet name is required")

        print(f"DEBUG: sheet_id = {sheet_id}")
        print(f"DEBUG: sheet_name = {sheet_name}")
        print(f"DEBUG: api_key = [PROVIDED]")
        print(f"DEBUG: num_rows = {num_rows}")

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
        
        # Apply row limit if specified
        if num_rows == "all":
            data_rows = all_data_rows
        else:
            try:
                row_limit = int(num_rows)
                data_rows = all_data_rows[:row_limit]
                print(f"DEBUG: Limited to {len(data_rows)} rows (requested {row_limit})")
            except (ValueError, TypeError):
                print(f"DEBUG: Invalid row limit '{num_rows}', using all rows")
                data_rows = all_data_rows
        
        # Convert to JSON format
        structured_data = []
        for i, row in enumerate(data_rows):
            row_dict = {}
            for j, header in enumerate(headers):
                value = row[j] if j < len(row) else ""
                row_dict[header] = value
            row_dict["_row_number"] = i + 2  # +2 because first row is headers
            structured_data.append(row_dict)
        
        print(f"DEBUG: Processed {len(structured_data)} data rows")
        
        # Create response
        result = {
            "sheet_id": sheet_id,
            "sheet_name": sheet_name,
            "num_rows": num_rows,
            "total_available_rows": len(all_data_rows),
            "returned_rows": len(data_rows),
            "headers": headers,
            "data": structured_data,
            "total_records": len(structured_data),
            "total_fields": len(headers)
        }
        
        return Response(
            data=result,
            metadata={
                "affected_records": len(structured_data),
                "message": f"Successfully fetched {len(structured_data)} records from sheet '{sheet_name}' ({num_rows} rows requested)"
            }
        )
                
    except Exception as e:
        print(f"DEBUG: /execute error = {e}")
        return Response.error(str(e))