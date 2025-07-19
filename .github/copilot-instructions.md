# Copilot Instructions for Stacksync App Connector Template

## Project Architecture
- This repo is a template for building Stacksync workflow connectors as Python microservices.
- Main entrypoint: `main.py` (registers Flask routes, loads modules).
- Modules live in `src/modules/{module_name}/{version}/` and include:
  - `route.py` (Flask endpoints)
  - `schema.json` (UI/data schema)
  - `module_config.yaml` (metadata)
  - `README.md` (module docs)
- Each module exposes `/execute`, `/content`, and optionally `/schema` endpoints for workflow integration.

## Developer Workflow
- Use `run_dev.sh` (Mac/Linux) or `run_dev.bat` (Windows) to start the dev server at `http://localhost:2003`.
- Build/rebuild with `./run_dev.sh --build` if dependencies or Docker config change.
- Add Python dependencies to `requirements.txt`.
- For new modules, copy `src/modules/new_empty_action/` and update names/configs.
- Edit `app_config.yaml` for connector-wide settings.

## Schema & Endpoint Patterns
- Module schemas (`schema.json`) define UI fields and validation for workflow actions.
- Use field types: `string`, `boolean`, `integer`, `array`, `object`.
- For JSON/code input, use `CodeblockWidget` with `language: json` in `ui_options`.
- Route handlers should echo only fields defined in the schema, using `Request(flask_request).data`.
- See `src/modules/create_contacts/` for a full-featured example.

## Integration & Conventions
- External API calls: use `requests` in `route.py`.
- Response format: always use `Response(data=..., metadata=...)` from `workflows_cdk`.
- Secrets: pass as JSON string or object, encrypted before storage.
- Dynamic content: implement `/content` endpoint for managed dropdowns, etc.
- Use `module_config.yaml` to declare module metadata and versioning.

## Key Files & References
- `main.py`: App entrypoint, router setup.
- `src/modules/create_contacts/`: Example of all patterns.
- `documentation/how-to-build-a-module-schema.md`: Step-by-step schema guide.
- `config/Dockerfile.dev`, `run_dev.sh`: Dev environment setup.

## Tips
- Keep schema and endpoint logic tightly synchronized.
- Use descriptive field labels and help texts in schemas.
- Prefer explicit field types and validation for robust UI/UX.
- For advanced patterns, see `/documentation` and Stacksync docs.

---

If any conventions or workflows are unclear, please request clarification or examples from the user.
