# Delete Row by Key Value Module

This module deletes rows from a Google Sheet where the specified key column matches the given key value.

## Usage
- **sheet_id**: The ID of the Google Spreadsheet.
- **sheet_name**: The name of the sheet to delete rows from.
- **key_column**: The column to match for row deletion.
- **key_value**: The value in the key column to match for deletion.

## Authentication
- Uses hardcoded API key and service account credentials (do not expose these in the UI).

## Endpoint
- `POST /execute` — Deletes all rows where `key_column` equals `key_value`.

## Example
```
{
  "sheet_id": "your-spreadsheet-id",
  "sheet_name": "Sheet1",
  "key_column": "Email",
  "key_value": "user@example.com"
}
```
