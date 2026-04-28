from urllib.parse import urlencode

import requests

from lf_workflow_dash.string_helpers import get_conclusion_time


def update_workflow_status(workflow_elem, token):  # pragma: no cover
    """Determine the status of a workflow run, using the github API.

    Args:
        workflow_elem (WorkflowElemData): the workflow to request
        token (str): auth token for hitting the github API
    """
    if workflow_elem is None:
        return

    print("  ", workflow_elem.workflow_name)
    # Make request
    request_url = (
        f"https://api.github.com/repos/{workflow_elem.owner}/{workflow_elem.repo}"
        f"/actions/workflows/{workflow_elem.workflow_name}/runs"
    )
    query_params = {}
    if workflow_elem.branch:
        query_params["branch"] = workflow_elem.branch
    if len(query_params) > 0:
        request_url += "?" + urlencode(query_params, doseq=True)

    payload = {}
    headers = {
        "accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.request("GET", request_url, headers=headers, data=payload, timeout=15)
    status_code = response.status_code
    conclusion = "pending"
    conclusion_time = ""
    is_stale = False

    # Process data
    if status_code == 200:  # API was successful
        response_json = response.json()
        if len(response_json["workflow_runs"]) == 0:  # workflow has no runs
            conclusion = "not yet run"

        else:
            last_run = response_json["workflow_runs"][0]
            workflow_elem.friendly_name = last_run["name"]

            # Get the workflow conclusion ("success", "failure", etc)
            conclusion = last_run["conclusion"]

            # Get the time this workflow concluded (in New York time)
            conclusion_time, is_stale = get_conclusion_time(last_run)

            # Check if the workflow is currently being executed
            if conclusion is None:
                # try next most recent
                if len(response_json["workflow_runs"]) > 1:
                    last_run = response_json["workflow_runs"][1]
                    conclusion = last_run["conclusion"]
                    conclusion_time, is_stale = get_conclusion_time(last_run)
                else:
                    conclusion = "pending"
                    conclusion_time = ""

    else:
        print("    ", status_code, request_url)
        conclusion = status_code

    workflow_elem.set_status(conclusion, conclusion_time, is_stale)
