# Module Schema Specification

This document provides a comprehensive reference for all available options when building module schemas for Stacksync Workflows.

## Schema Structure

### Root Schema Object

```json
{
  "metadata": {
    "workflows_module_schema_version": "1.0.0"
  },
  "fields": [...],
  "ui_options": {...}
}
```

**Required Properties:**

- `metadata` - Schema metadata configuration
- `fields` - Array of field definitions

**Optional Properties:**

- `ui_options` - Global UI configuration options

---

## Metadata Configuration

### workflows_module_schema_version

- **Type:** String
- **Required:** Yes
- **Default:** "1.0.0"
- **Description:** Specifies the schema version for compatibility

```json
{
  "metadata": {
    "workflows_module_schema_version": "1.0.0"
  }
}
```

---

## Field Types

### String Fields

**Basic String Field:**

```json
{
  "id": "field_name",
  "type": "string",
  "label": "Display Label",
  "description": "Field description",
  "default": "Default value"
}
```

**Properties:**

- `id` (string, required) - Unique field identifier
- `type` (string, required) - Must be "string"
- `label` (string, optional) - Display label for the field
- `description` (string, optional) - Help text for users
- `default` (string, optional) - Default value

### Number Fields

**Basic Number Field:**

```json
{
  "id": "count",
  "type": "number",
  "label": "Count",
  "default": 0
}
```

**Properties:**

- `id` (string, required) - Unique field identifier
- `type` (string, required) - Must be "number"
- `label` (string, optional) - Display label
- `default` (number, optional) - Default numeric value

### Integer Fields

**Basic Integer Field:**

```json
{
  "id": "whole_number",
  "type": "integer",
  "label": "Whole Number",
  "default": 1
}
```

### Boolean Fields

**Basic Boolean Field:**

```json
{
  "id": "enable_feature",
  "type": "boolean",
  "label": "Enable Feature",
  "default": false
}
```

### Connection Fields

**Connection Field:**

```json
{
  "type": "connection",
  "id": "api_connection",
  "label": "API Connection",
  "allowed_app_types": ["salesforce", "hubspot"],
  "allowed_connection_management_types": ["managed", "custom"]
}
```

**Properties:**

- `allowed_app_types` (array, required) - List of supported connection types
- `allowed_connection_management_types` (array, required) - Connection management options

**Supported App Types:**

- `salesforce` - Salesforce CRM
- `hubspot` - HubSpot CRM
- `postgres` - PostgreSQL database
- `mysql` - MySQL database
- `custom_api` - Custom API connections

**Connection Management Types:**

- `managed` - Platform-managed connections
- `custom` - User-provided credentials

### Object Fields

**Simple Object Field:**

```json
{
  "type": "object",
  "id": "settings",
  "label": "Settings",
  "fields": [
    {
      "id": "name",
      "type": "string",
      "label": "Name"
    }
  ]
}
```

**Object with Choices:**

```json
{
  "type": "object",
  "id": "platform",
  "label": "Platform",
  "choices": {
    "values": [
      {
        "value": { "id": "linkedin", "label": "LinkedIn" },
        "label": "LinkedIn"
      }
    ]
  }
}
```

### Array Fields

**String Array:**

```json
{
  "type": "array",
  "id": "tags",
  "label": "Tags",
  "items": {
    "type": "string",
    "label": "Tag"
  }
}
```

**Object Array:**

```json
{
  "type": "array",
  "id": "users",
  "label": "Users",
  "items": {
    "type": "object",
    "fields": [
      {
        "id": "name",
        "type": "string",
        "label": "Name"
      }
    ]
  }
}
```

---

## UI Widgets

### Available Widgets

**input** (default for strings)

```json
{
  "ui_options": {
    "ui_widget": "input"
  }
}
```

**textarea** (multi-line text)

```json
{
  "ui_options": {
    "ui_widget": "textarea"
  }
}
```

**password** (hidden text input)

```json
{
  "ui_options": {
    "ui_widget": "password"
  }
}
```

**SelectWidget** (dropdown selection)

```json
{
  "ui_options": {
    "ui_widget": "SelectWidget"
  }
}
```

**checkbox** (boolean checkbox)

```json
{
  "ui_options": {
    "ui_widget": "checkbox"
  }
}
```

**CodeblockWidget** (code editor)

```json
{
  "ui_options": {
    "ui_widget": "CodeblockWidget",
    "ui_options": {
      "language": "json"
    }
  }
}
```

**hidden** (hidden field)

```json
{
  "ui_options": {
    "ui_widget": "hidden"
  }
}
```

### CodeblockWidget Languages

Supported syntax highlighting languages:

- `json` - JSON format
- `sql` - SQL queries
- `javascript` - JavaScript code
- `python` - Python code
- `yaml` - YAML configuration
- `xml` - XML markup
- `html` - HTML markup
- `css` - CSS styling

---

## Validation Rules

### Basic Validation

**required** - Field is mandatory

```json
{
  "validation": {
    "required": true
  }
}
```

**min_length** - Minimum string length

```json
{
  "validation": {
    "min_length": 3
  }
}
```

**max_length** - Maximum string length

```json
{
  "validation": {
    "max_length": 100
  }
}
```

**minimum** - Minimum numeric value

```json
{
  "validation": {
    "minimum": 0
  }
}
```

**maximum** - Maximum numeric value

```json
{
  "validation": {
    "maximum": 1000
  }
}
```

**pattern** - Regular expression validation

```json
{
  "validation": {
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  }
}
```

### Format Validation

**email** - Email address format

```json
{
  "format": "email"
}
```

**uri** - URI format

```json
{
  "format": "uri"
}
```

**date** - Date format (YYYY-MM-DD)

```json
{
  "format": "date"
}
```

**date-time** - Date-time format (ISO 8601)

```json
{
  "format": "date-time"
}
```

**uuid** - UUID format

```json
{
  "format": "uuid"
}
```

---

## Dynamic Content

### Basic Content Configuration

```json
{
  "content": {
    "type": ["managed"],
    "content_objects": [
      {
        "id": "users"
      }
    ]
  }
}
```

**Properties:**

- `type` (array, required) - Content management types
- `content_objects` (array, required) - List of content objects to fetch

**Content Management Types:**

- `managed` - Platform manages the content loading
- `custom` - Custom content loading logic

### Content Dependencies

**Field-dependent content:**

```json
{
  "content": {
    "type": ["managed"],
    "content_objects": [
      {
        "id": "users_in_channel",
        "content_object_depends_on_fields": [
          {
            "id": "channel"
          }
        ]
      }
    ]
  }
}
```

**Array item dependencies:**

```json
{
  "content_object_depends_on_fields": [
    {
      "id": "channels.items"
    }
  ]
}
```

---

## Choices Configuration

### Static Choices

**Simple string choices:**

```json
{
  "choices": {
    "values": [
      { "value": "option1", "label": "Option 1" },
      { "value": "option2", "label": "Option 2" }
    ]
  }
}
```

**Object choices:**

```json
{
  "choices": {
    "values": [
      {
        "value": { "id": "contact", "label": "Contact" },
        "label": "Contact"
      },
      {
        "value": { "id": "lead", "label": "Lead" },
        "label": "Lead"
      }
    ]
  }
}
```

### Dynamic Choices

**Empty choices for dynamic loading:**

```json
{
  "choices": {
    "values": []
  }
}
```

---

## Schema Rules (Conditional Logic)

### Basic Rules Structure

```json
{
  "rules": [
    {
      "if": {
        "and": [
          {
            "id": "field_id",
            "operator": "equal",
            "value": "expected_value"
          }
        ]
      },
      "then": {
        "fields": [
          {
            "id": "target_field",
            "ui_options": {
              "ui_widget": "hidden"
            },
            "apply_as": "merge"
          }
        ]
      }
    }
  ]
}
```

### Condition Operators

**equal** - Exact match

```json
{
  "id": "status",
  "operator": "equal",
  "value": "active"
}
```

**not_equal** - Not equal to

```json
{
  "id": "status",
  "operator": "not_equal",
  "value": "inactive"
}
```

**is_in** - Value in array

```json
{
  "id": "category",
  "operator": "is_in",
  "value": ["premium", "enterprise"]
}
```

**is_not_in** - Value not in array

```json
{
  "id": "category",
  "operator": "is_not_in",
  "value": ["free", "trial"]
}
```

**is_empty** - Field is empty

```json
{
  "id": "optional_field",
  "operator": "is_empty"
}
```

**is_not_empty** - Field has value

```json
{
  "id": "required_field",
  "operator": "is_not_empty"
}
```

**greater_than** - Numeric comparison

```json
{
  "id": "count",
  "operator": "greater_than",
  "value": 10
}
```

**less_than** - Numeric comparison

```json
{
  "id": "count",
  "operator": "less_than",
  "value": 100
}
```

### Logic Combinators

**and** - All conditions must be true

```json
{
  "and": [
    { "id": "field1", "operator": "equal", "value": "value1" },
    { "id": "field2", "operator": "equal", "value": "value2" }
  ]
}
```

**or** - Any condition must be true

```json
{
  "or": [
    { "id": "field1", "operator": "equal", "value": "value1" },
    { "id": "field2", "operator": "equal", "value": "value2" }
  ]
}
```

### Rule Effects

**apply_as** options:

- `merge` - Merge with existing field configuration
- `fully_replace` - Replace entire field configuration

**Show/Hide Fields:**

```json
{
  "then": {
    "fields": [
      {
        "id": "conditional_field",
        "ui_options": {
          "ui_widget": null
        },
        "apply_as": "merge"
      }
    ]
  }
}
```

**Hide Fields:**

```json
{
  "then": {
    "fields": [
      {
        "id": "conditional_field",
        "ui_options": {
          "ui_widget": "hidden"
        },
        "apply_as": "merge"
      }
    ]
  }
}
```

---

## UI Layout Options

### Global UI Options

**Field Ordering:**

```json
{
  "ui_options": {
    "ui_order": ["field1", "field2", "field3"]
  }
}
```

### Field-Level UI Options

**Horizontal Layout:**

```json
{
  "ui_options": {
    "ui_layout": {
      "type": "horizontal",
      "elements": ["first_name", "last_name"]
    }
  }
}
```

---

## Advanced Features

### Action Handlers

Action handlers define what should happen when users interact with fields. They trigger specific behaviors when field values change.

#### load_schema

**Purpose:** Triggers a schema reload when the field value changes, allowing for dynamic updates to other fields based on the new value.

**Basic Usage:**

```json
{
  "id": "country",
  "type": "string",
  "label": "Country",
  "on_action": {
    "load_schema": true
  }
}
```

**What happens when `load_schema` is triggered:**

1. You change the value of the field `country`
2. A trigger sends an HTTP POST request to the module /schema endpoint with :

- the full schema
- the full form data
- the full content objects

3. The module returns a new schema
4. The new schema is merged with the existing schema
5. The frontend updates the UI to reflect the new schema

#### Common Use Cases

**Use Case 1: Cascading Dropdowns**

```json
{
  "id": "country",
  "type": "object",
  "label": "Country",
  "on_action": {
    "load_schema": true
  },
  "choices": {
    "values": [
      {"value": {"id": "us", "label": "United States"}, "label": "United States"},
      {"value": {"id": "ca", "label": "Canada"}, "label": "Canada"}
    ]
  }
},
{
  "id": "state",
  "type": "object",
  "label": "State/Province",
  "content": {
    "type": ["managed"],
    "content_objects": [
      {
        "id": "states_by_country",
        "content_object_depends_on_fields": [
          {"id": "country"}
        ]
      }
    ]
  }
}
```

**Use Case 2: Conditional Field Display**

```json
{
  "id": "data_source",
  "type": "string",
  "label": "Data Source",
  "on_action": {
    "load_schema": true
  },
  "choices": {
    "values": [
      {"value": "database", "label": "Database"},
      {"value": "api", "label": "API"},
      {"value": "file", "label": "File"}
    ]
  }
},
{
  "id": "database_config",
  "type": "object",
  "label": "Database Configuration",
  "rules": [
    {
      "if": {
        "and": [
          {
            "id": "data_source",
            "operator": "equal",
            "value": "database"
          }
        ]
      },
      "then": {
        "fields": [
          {
            "id": "database_config",
            "ui_options": {
              "ui_widget": null
            },
            "apply_as": "merge"
          }
        ]
      }
    }
  ]
}
```

**Use Case 3: Dynamic Validation**

```json
{
  "id": "field_type",
  "type": "string",
  "label": "Field Type",
  "on_action": {
    "load_schema": true
  },
  "choices": {
    "values": [
      {"value": "email", "label": "Email"},
      {"value": "phone", "label": "Phone"},
      {"value": "text", "label": "Text"}
    ]
  }
},
{
  "id": "field_value",
  "type": "string",
  "label": "Field Value",
  "rules": [
    {
      "if": {
        "and": [
          {
            "id": "field_type",
            "operator": "equal",
            "value": "email"
          }
        ]
      },
      "then": {
        "fields": [
          {
            "id": "field_value",
            "format": "email",
            "validation": {
              "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            },
            "apply_as": "merge"
          }
        ]
      }
    }
  ]
}
```

#### Backend Implementation

When `load_schema: true` is triggered, your `/content` endpoint receives the updated form data:

```python
@router.route("/content", methods=["POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data

        # Get updated form data after field change
        form_data = data.get("form_data", {})
        content_object_names = data.get("content_object_names", [])

        content_objects = []

        for content_name in content_object_names:
            if content_name == "states_by_country":
                # Get the selected country from updated form data
                selected_country = form_data.get("country", {})
                country_id = selected_country.get("id") if selected_country else None

                if country_id == "us":
                    states = [
                        {"value": {"id": "ca", "label": "California"}, "label": "California"},
                        {"value": {"id": "ny", "label": "New York"}, "label": "New York"}
                    ]
                elif country_id == "ca":
                    states = [
                        {"value": {"id": "on", "label": "Ontario"}, "label": "Ontario"},
                        {"value": {"id": "bc", "label": "British Columbia"}, "label": "British Columbia"}
                    ]
                else:
                    states = []

                content_objects.append({
                    "content_object_name": "states_by_country",
                    "data": states
                })

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        return Response.error(str(e))
```

#### Performance Considerations

- **Use Sparingly:** Only add `load_schema: true` to fields that actually need to trigger updates
- **Optimize Backend:** Ensure your `/content` endpoint responds quickly to avoid UI lag
- **Cache When Possible:** Cache static data that doesn't change between requests
- **Batch Updates:** If multiple fields need to trigger updates, consider grouping them

#### Best Practices

1. **Clear User Feedback:** Show loading indicators when schema is reloading
2. **Preserve User Input:** Ensure field values aren't lost during reload
3. **Error Handling:** Gracefully handle failures in content loading
4. **Debouncing:** Consider debouncing rapid field changes to avoid excessive requests

#### Debugging Tips

- Check browser network tab to see `/content` requests when fields change
- Verify that `content_object_depends_on_fields` references match your field IDs exactly
- Test with browser console open to catch any JavaScript errors
- Use simple test data first, then add complexity

---

## Complete Field Example

Here's a comprehensive example showing most available options:

```json
{
  "id": "user_email",
  "type": "string",
  "label": "User Email",
  "description": "Enter the user's email address",
  "default": "",
  "format": "email",
  "validation": {
    "required": true,
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  },
  "validation_messages": {
    "required": "Email is required for notifications",
    "pattern": "Please enter a valid email address"
  },
  "ui_options": {
    "ui_widget": "input"
  },
  "on_action": {
    "load_schema": true
  },
  "rules": [
    {
      "if": {
        "and": [
          {
            "id": "user_email",
            "operator": "is_not_empty"
          }
        ]
      },
      "then": {
        "fields": [
          {
            "id": "send_notification",
            "ui_options": {
              "ui_widget": null
            },
            "apply_as": "merge"
          }
        ]
      }
    }
  ]
}
```

This specification covers all major aspects of module schema configuration. Refer to this document when building your schemas to understand all available options and their proper usage.
