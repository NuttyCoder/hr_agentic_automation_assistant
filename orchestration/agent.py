import uuid
from typing import Dict, Any

from src.orchestration.workflow_runner import WorkflowRunner
from src.orchestration.tools_registry import get_tool
from src.orchestration.context_manager import OrchestrationContext
from src.governance.audit_logger import audit_log
from src.governance.pii_masking import mask_payload
from src.governance.policy_engine import enforce_policies


class HROrchestrator:
    """
    The central agent responsible for:
    - Selecting workflows
    - Planning tool calls
    - Executing steps
    - Enforcing governance
    - Producing final responses

    This is intentionally simple but structured like a real agentic system.
    """

    def __init__(self):
        self.workflow_runner = WorkflowRunner()

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Entry point for all agentic HR workflows.
        """
        correlation_id = str(uuid.uuid4())

        # Mask incoming payload for logs
        masked_input = mask_payload(payload)

        audit_log(
            event="workflow_start",
            correlation_id=correlation_id,
            details={"input": masked_input}
        )

        # Build orchestration context
        context = OrchestrationContext(
            correlation_id=correlation_id,
            user=payload.get("user"),
            intent=payload.get("intent"),
            entities=payload.get("entities", {}),
            raw_input=payload
        )

        # Enforce policies before doing anything
        enforce_policies(context)

        # Select workflow
        workflow_id = self._select_workflow(context.intent)
        context.workflow_id = workflow_id

        audit_log(
            event="workflow_selected",
            correlation_id=correlation_id,
            details={"workflow_id": workflow_id}
        )

        # Execute workflow
        result = await self.workflow_runner.execute(workflow_id, context)

        # Final audit
        audit_log(
            event="workflow_complete",
            correlation_id=correlation_id,
            details={"result": mask_payload(result)}
        )

        return result

    def _select_workflow(self, intent: str) -> str:
        """
        Map intents to workflow YAML files.
        """
        mapping = {
            "request_time_off": "request_time_off",
            "update_address": "update_address",
            "payroll_issue": "payroll_issue",
            "benefits_question": "benefits_policy_qa",
        }

        return mapping.get(intent, "unknown_intent")


# Convenience function used by FastAPI router
async def run_agentic_workflow(payload: Dict[str, Any]):
    orchestrator = HROrchestrator()
    return await orchestrator.run(payload)
