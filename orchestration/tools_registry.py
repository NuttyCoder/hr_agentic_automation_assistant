from typing import Callable, Dict, Any, Awaitable

# Import tool functions from services, adapters, and RPA bots
from src.services.hr_profile_service import get_employee_profile
from src.services.pto_service import get_pto_balance, create_pto_request
from src.services.ticketing_service import create_ticket
from src.services.benefits_service import get_benefits_info
from src.services.policy_service import query_policy

from src.adapters.servicenow_client import create_servicenow_incident
from src.adapters.successfactors_client import update_employee_address

from src.rpa.bots.address_update_bot import run_address_update_bot
from src.rpa.bots.payroll_investigation_bot import run_payroll_investigation

# -------------------------------------------------------------------------
# TOOL REGISTRY
# -------------------------------------------------------------------------

"""
Each tool must be an async function that accepts a single argument:
    context: OrchestrationContext

Tools return a dict result that the workflow runner stores in context.
"""

TOOLS: Dict[str, Callable[..., Awaitable[Any]]] = {
    # HR Profile & PTO
    "get_employee_profile": get_employee_profile,
    "get_pto_balance": get_pto_balance,
    "create_pto_request": create_pto_request,

    # Ticketing
    "create_ticket": create_ticket,

    # Benefits & Policy
    "get_benefits_info": get_benefits_info,
    "query_policy": query_policy,

    # HR Systems (Adapters)
    "servicenow_create_incident": create_servicenow_incident,
    "successfactors_update_address": update_employee_address,

    # RPA Bots
    "rpa_address_update": run_address_update_bot,
    "rpa_payroll_investigation": run_payroll_investigation,
}

# -------------------------------------------------------------------------
# TOOL LOOKUP
# -------------------------------------------------------------------------

def get_tool(name: str) -> Callable[..., Awaitable[Any]]:
    """
    Retrieve a tool by name.
    Returns None if the tool is not registered.
    """
    return TOOLS.get(name)
