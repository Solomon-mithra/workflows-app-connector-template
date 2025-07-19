# Run Task Connector Example

This directory contains an example implementation of a connector action for creating browser automation tasks using the Browser-Use Cloud API. This connector demonstrates how to define an action that can be used to add new automation tasks via a standardized workflow module interface.

## Endpoint
POST /api/v1/run-task

## Description
Creates a new browser automation task and returns the task ID that can be used to track progress.

## Request Body
- `task` (string, required): Instructions for what the agent should do.
- `secrets` (object): Dictionary of secrets to be used by the agent.
- `allowed_domains` (array): List of domains the agent is allowed to visit.
- `save_browser_data` (boolean, default: false): Save browser cookies and other data.
- `structured_output_json` (string): JSON schema for output model.
- `llm_model` (string, default: gpt-4.1): LLM model to use.
- `use_adblock` (boolean, default: true): Use adblocker.
- `use_proxy` (boolean, default: true): Use proxy for captcha solving.
- `proxy_country_code` (string, default: us): Country code for proxy.
- `highlight_elements` (boolean, default: true): Highlight elements on the page.
- `included_file_names` (array): File names to include in the task.
- `browser_viewport_width` (integer, default: 1280): Browser viewport width.
- `browser_viewport_height` (integer, default: 960): Browser viewport height.
- `max_agent_steps` (integer, default: 75): Maximum agent steps.
- `enable_public_share` (boolean, default: false): Enable public sharing of task execution.

## Response
- `id` (string): The unique identifier for the created task.

See https://cloud.browser-use.com/ for more details.
