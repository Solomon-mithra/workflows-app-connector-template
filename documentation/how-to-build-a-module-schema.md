# How to Build a Module Schema on Stacksync Workflows

In this tutorial, we'll guide you through creating module schemas step-by-step. Module schemas define the user interface forms for your workflow actions. This guide focuses on the practical, hands-on process of building schemas.

> 📖 **Reference:** For complete technical details, see the [Module Schema Specification](./module-schema-specification.md)

## What You'll Learn

By following this guide, you'll learn to:

- Create basic schemas with different field types
- Add dynamic content that loads from your API
- Implement field validation and conditional logic
- Test and deploy your schemas

## Step 1: Locate Your Schema File

**Step 1.1:** Navigate to your connector project folder.

**Step 1.2:** Open the `src/modules/` directory.

**Step 1.3:** Find your action folder (e.g., `create_contacts`, `get_posts`).

**Step 1.4:** Open the version folder (e.g., `v1/`).

**Step 1.5:** Locate the `schema.json` file.

Your file path should look like: `src/modules/your_action/v1/schema.json`

## Step 2: Create Your First Schema

**Step 2.1:** Open your `schema.json` file in your code editor.

**Step 2.2:** Start with this basic structure:

```json
{
  "metadata": {
    "workflows_module_schema_version": "1.0.0"
  },
  "fields": [],
  "ui_options": {}
}
```

**Step 2.3:** Save the file.

**Step 2.4:** Test that your connector loads without errors.

> 💡 **Tip:** Always start with the minimal structure and build incrementally.

## Step 3: Add Your First Field

**Step 3.1:** Add a simple text field inside the `fields` array:

```json
{
  "metadata": {
    "workflows_module_schema_version": "1.0.0"
  },
  "fields": [
    {
      "id": "api_key",
      "type": "string",
      "label": "API Key"
    }
  ]
}
```

**Step 3.2:** Save and reload your connector.

**Step 3.3:** Create a test workflow and add your action.

**Step 3.4:** Verify the field appears in the form.

> 📖 **Reference:** See [Field Types](./module-schema-specification.md#field-types) for all available field types.

## Step 4: Make the Field Required

**Step 4.1:** Add validation to make the field required:

```json
{
  "id": "api_key",
  "type": "string",
  "label": "API Key",
  "validation": {
    "required": true
  }
}
```

**Step 4.2:** Save the file.

**Step 4.3:** Test the validation by trying to save without entering a value.

**Step 4.4:** Verify that an error message appears.

> 📖 **Reference:** See [Validation Rules](./module-schema-specification.md#validation-rules) for all validation options.

## Step 5: Add a Password Widget

**Step 5.1:** Add UI options to hide the API key:

```json
{
  "id": "api_key",
  "type": "string",
  "label": "API Key",
  "validation": {
    "required": true
  },
  "ui_options": {
    "ui_widget": "password"
  }
}
```

**Step 5.2:** Save and test that the input is now hidden.

> 📖 **Reference:** See [UI Widgets](./module-schema-specification.md#ui-widgets) for all available widgets.

## Step 6: Add a Description

**Step 6.1:** Add a helpful description for users:

```json
{
  "id": "api_key",
  "type": "string",
  "label": "API Key",
  "description": "Your API key for authentication",
  "validation": {
    "required": true
  },
  "ui_options": {
    "ui_widget": "password"
  }
}
```

**Step 6.2:** Save and verify the description appears below the field.

## Step 7: Add a Selection Field

**Step 7.1:** Add a second field for platform selection:

```json
{
  "fields": [
    {
      "id": "api_key",
      "type": "string",
      "label": "API Key",
      "description": "Your API key for authentication",
      "validation": {
        "required": true
      },
      "ui_options": {
        "ui_widget": "password"
      }
    },
    {
      "id": "platform",
      "type": "object",
      "label": "Platform",
      "ui_options": {
        "ui_widget": "SelectWidget"
      }
    }
  ]
}
```

**Step 7.2:** Save and verify both fields appear.

## Step 8: Add Static Choices

**Step 8.1:** Add choices to the platform field:

```json
{
  "id": "platform",
  "type": "object",
  "label": "Platform",
  "ui_options": {
    "ui_widget": "SelectWidget"
  },
  "choices": {
    "values": [
      {
        "value": { "id": "linkedin", "label": "LinkedIn" },
        "label": "LinkedIn"
      },
      {
        "value": { "id": "twitter", "label": "Twitter" },
        "label": "Twitter"
      }
    ]
  }
}
```

**Step 8.2:** Save and test selecting different platforms.

> 📖 **Reference:** See [Choices Configuration](./module-schema-specification.md#choices-configuration) for choice formats.

## Step 9: Set Field Order

**Step 9.1:** Add the `ui_options` section at the root level:

```json
{
  "metadata": {
    "workflows_module_schema_version": "1.0.0"
  },
  "fields": [...],
  "ui_options": {
    "ui_order": ["api_key", "platform"]
  }
}
```

**Step 9.2:** Save and verify the fields appear in the specified order.

## Step 10: Add a Large Text Field

**Step 10.1:** Add a message field with textarea widget:

```json
{
  "id": "message",
  "type": "string",
  "label": "Message",
  "description": "The message to send",
  "ui_options": {
    "ui_widget": "textarea"
  }
}
```

**Step 10.2:** Update the UI order to include the new field:

```json
{
  "ui_options": {
    "ui_order": ["api_key", "platform", "message"]
  }
}
```

**Step 10.3:** Save and test the multi-line text area.

## Step 11: Add Dynamic Content Setup

**Step 11.1:** Add a user selection field that will load dynamically:

```json
{
  "id": "user_id",
  "type": "object",
  "label": "User",
  "description": "Select a user",
  "ui_options": {
    "ui_widget": "SelectWidget"
  },
  "choices": {
    "values": []
  },
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

**Step 11.2:** Add it to your UI order:

```json
{
  "ui_options": {
    "ui_order": ["api_key", "platform", "user_id", "message"]
  }
}
```

**Step 11.3:** Save the schema.

> 📖 **Reference:** See [Dynamic Content](./module-schema-specification.md#dynamic-content) for content configuration.

## Step 12: Implement Dynamic Content in Code

**Step 12.1:** Open your `route.py` file in the same folder.

**Step 12.2:** Find the `/content` endpoint (or create it if it doesn't exist).

**Step 12.3:** Add the users content handler:

```python
@router.route("/content", methods=["POST"])
def content():
    try:
        request = Request(flask_request)
        data = request.data

        content_object_names = data.get("content_object_names", [])
        content_objects = []

        for content_name in content_object_names:
            if content_name == "users":
                users = [
                    {"value": {"id": "1", "label": "John Doe"}, "label": "John Doe"},
                    {"value": {"id": "2", "label": "Jane Smith"}, "label": "Jane Smith"}
                ]

                content_objects.append({
                    "content_object_name": "users",
                    "data": users
                })

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        return Response.error(str(e))
```

**Step 12.4:** Save the route file.

## Step 13: Test Dynamic Content

**Step 13.1:** Reload your connector.

**Step 13.2:** Open your test workflow action.

**Step 13.3:** Click the refresh button next to the User field.

**Step 13.4:** Verify that the dropdown loads with John Doe and Jane Smith.

**Step 13.5:** Select a user and save.

## Step 14: Add Field Dependencies

**Step 14.1:** Add a channel field that will affect the user field:

```json
{
  "id": "channel",
  "type": "object",
  "label": "Channel",
  "ui_options": {
    "ui_widget": "SelectWidget"
  },
  "choices": {
    "values": [
      {
        "value": { "id": "general", "label": "General" },
        "label": "General"
      },
      {
        "value": { "id": "tech", "label": "Tech Team" },
        "label": "Tech Team"
      }
    ]
  }
}
```

**Step 14.2:** Update the user field to depend on the channel:

```json
{
  "id": "user_id",
  "type": "object",
  "label": "User",
  "description": "Select a user in the channel",
  "ui_options": {
    "ui_widget": "SelectWidget"
  },
  "choices": {
    "values": []
  },
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

**Step 14.3:** Update UI order:

```json
{
  "ui_options": {
    "ui_order": ["api_key", "platform", "channel", "user_id", "message"]
  }
}
```

> 📖 **Reference:** See [Content Dependencies](./module-schema-specification.md#content-dependencies) for dependency patterns.

## Step 15: Update Content Handler for Dependencies

**Step 15.1:** Update your content endpoint to handle the dependency:

```python
for content_name in content_object_names:
    if content_name == "users_in_channel":
        form_data = data.get("form_data", {})
        selected_channel = form_data.get("channel", {})
        channel_id = selected_channel.get("id") if selected_channel else None

        if channel_id == "general":
            users = [
                {"value": {"id": "1", "label": "John Doe"}, "label": "John Doe"},
                {"value": {"id": "3", "label": "Alice Brown"}, "label": "Alice Brown"}
            ]
        elif channel_id == "tech":
            users = [
                {"value": {"id": "2", "label": "Jane Smith"}, "label": "Jane Smith"},
                {"value": {"id": "4", "label": "Bob Wilson"}, "label": "Bob Wilson"}
            ]
        else:
            users = []

        content_objects.append({
            "content_object_name": "users_in_channel",
            "data": users
        })
```

**Step 15.2:** Save and test that users change based on channel selection.

## Step 16: Add Schema Endpoint for Dynamic Updates

**Step 16.1:** Create a `/schema` endpoint in your `route.py` file:

```python
@router.route("/schema", methods=["POST"])
def schema():
    try:
        request = Request(flask_request)
        data = request.data

        # Get the current form data
        form_data = data.get("form_data", {})

        # Load your base schema from the schema.json file
        with open("schema.json", "r") as f:
            base_schema = json.load(f)

        # Apply any dynamic modifications based on form_data
        # For example, modify field visibility or validation

        return Response(data=base_schema)

    except Exception as e:
        return Response.error(str(e))
```

**Step 16.2:** This endpoint is called when fields with `on_action: {"load_schema": true}` are changed.

**Step 16.3:** The returned schema is merged with the existing schema to update the UI.

## Step 17: Test Your Complete Schema

**Step 17.1:** Save all files.

**Step 17.2:** Reload your connector in the Stacksync interface.

**Step 17.3:** Create a new test workflow.

**Step 17.4:** Add your action to the workflow.

**Step 17.5:** Test each functionality:

- Verify all fields appear in correct order
- Test validation by leaving required fields empty
- Test dynamic content loading with refresh button
- Test field dependencies by changing channel selection

## Step 18: Handle Data in Execute Endpoint

**Step 18.1:** Open your `route.py` file.

**Step 18.2:** Find the `/execute` endpoint.

**Step 18.3:** Add code to handle your schema data:

```python
@router.route("/execute", methods=["POST"])
def execute():
    try:
        request = Request(flask_request)
        data = request.data

        # Get values from your schema
        api_key = data.get("api_key")
        platform = data.get("platform", {})
        channel = data.get("channel", {})
        user_id = data.get("user_id", {})
        message = data.get("message")

        # Use the data for your logic
        result = {
            "success": True,
            "platform": platform.get("label"),
            "user": user_id.get("label"),
            "message": message
        }

        return Response(
            data=result,
            metadata={"processed_at": "2024-01-01T00:00:00Z"}
        )

    except Exception as e:
        return Response.error(str(e))
```

**Step 18.4:** Save and test by running your workflow.

## Step 19: Add Input Validation

**Step 19.1:** Add more validation rules to your message field:

```json
{
  "id": "message",
  "type": "string",
  "label": "Message",
  "description": "The message to send",
  "ui_options": {
    "ui_widget": "textarea"
  },
  "validation": {
    "required": true,
    "min_length": 10,
    "max_length": 500
  }
}
```

**Step 19.2:** Test that validation works by entering messages that are too short or too long.

## Step 20: Final Testing Checklist

**Step 20.1:** Test all validation rules:

- Required fields show errors when empty
- Length limits are enforced
- Format validation works

**Step 20.2:** Test dynamic content:

- Content loads when refreshing
- Dependencies update correctly
- No errors in browser console

**Step 20.3:** Test schema updates:

- Fields with `load_schema: true` trigger schema reloads
- `/schema` endpoint returns updated schemas correctly
- UI updates reflect schema changes

**Step 20.4:** Test workflow execution:

- Data reaches execute endpoint correctly
- All field values are accessible
- Workflow completes successfully

## Congratulations!

You've successfully built a complete module schema with:

- ✅ Basic field types (string, object, number)
- ✅ Field validation and UI widgets
- ✅ Dynamic content loading via `/content` endpoint
- ✅ Field dependencies
- ✅ Schema updates via `/schema` endpoint
- ✅ Integration with your `/execute` endpoint

## Next Steps

**Step 21:** Explore more advanced features:

- Add array fields for multiple values
- Implement custom error messages
- Create multi-step wizard forms
- Add more complex validation patterns

> 📖 **Reference:** See the [Module Schema Specification](./module-schema-specification.md) for complete technical details on all available options.

Remember: Start simple and build complexity gradually. Each step should work before moving to the next!
