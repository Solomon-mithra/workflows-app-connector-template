import requests
from workflows_cdk import Response, Request
from main import router
from flask import request as flask_request

API_URL = "https://cloud.browser-use.com/api/v1/run-task"

REQUIRED_FIELDS = ["task"]
ALLOWED_FIELDS = [
    "task", "secrets", "allowed_domains", "save_browser_data", "structured_output_json", "llm_model",
    "use_adblock", "use_proxy", "proxy_country_code", "highlight_elements", "included_file_names",
    "browser_viewport_width", "browser_viewport_height", "max_agent_steps", "enable_public_share"
]

@router.route("/execute", methods=["POST"])
def execute():
    """
    Accepts schema input and returns a structured result, following documentation example.
    """
    try:
        request = Request(flask_request)
        data = request.data

        # Get values from your schema
        task = data.get("task")
        secrets = data.get("secrets")
        allowed_domains = data.get("allowed_domains")
        save_browser_data = data.get("save_browser_data")
        structured_output_json = data.get("structured_output_json")
        llm_model = data.get("llm_model")
        use_adblock = data.get("use_adblock")
        use_proxy = data.get("use_proxy")
        proxy_country_code = data.get("proxy_country_code")
        highlight_elements = data.get("highlight_elements")
        included_file_names = data.get("included_file_names")
        browser_viewport_width = data.get("browser_viewport_width")
        browser_viewport_height = data.get("browser_viewport_height")
        max_agent_steps = data.get("max_agent_steps")
        enable_public_share = data.get("enable_public_share")

        # Use the data for your logic
        result = {
            "success": True,
            "task": task,
            "secrets": secrets,
            "allowed_domains": allowed_domains,
            "save_browser_data": save_browser_data,
            "structured_output_json": structured_output_json,
            "llm_model": llm_model,
            "use_adblock": use_adblock,
            "use_proxy": use_proxy,
            "proxy_country_code": proxy_country_code,
            "highlight_elements": highlight_elements,
            "included_file_names": included_file_names,
            "browser_viewport_width": browser_viewport_width,
            "browser_viewport_height": browser_viewport_height,
            "max_agent_steps": max_agent_steps,
            "enable_public_share": enable_public_share
        }

        return Response(
            data=result,
            metadata={"processed_at": "2024-01-01T00:00:00Z"}
        )

    except Exception as e:
        return Response.error(str(e))
