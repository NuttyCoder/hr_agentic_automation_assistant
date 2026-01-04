import yaml
from typing import Any, Dict

from src.orchestration.tools_registry import get_tool
from src.governance.audit_logger import audit_log
from src.governance.pii_masking import mask_payload


class WorkflowRunner:
    """
    Executes YAML-defined workflows step-by-step.
    Supports:
    - tool calls
    - decisions
    - context updates
    - branching
    """

    async def execute(self, workflow_id: str, context) -> Dict[str, Any]:
        workflow = self._load_workflow(workflow_id)
        steps = workflow.get("steps", [])

        audit_log(
            event="workflow_loaded",
            correlation_id=context.correlation_id,
            details={"workflow_id": workflow_id, "steps": len(steps)}
        )

        for step in steps:
            step_id = step.get("id")
            step_type = step.get("type", "tool")

            audit_log(
                event="workflow_step_start",
                correlation_id=context.correlation_id,
                details={"step_id": step_id, "step_type": step_type}
            )

            if step_type == "tool":
                await self._run_tool_step(step, context)

            elif step_type == "decision":
                branch = self._evaluate_decision(step, context)
                next_step = step.get(branch)
                if next_step:
                    await self._run_tool_step({"id": f"{step_id}_{branch}", "tool": next_step}, context)

            elif step_type == "update_context":
                self._update_context(step, context)

            else:
                raise ValueError(f"Unknown step type: {step_type}")

        return context.output or {"message": "Workflow completed"}

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _load_workflow(self, workflow_id: str) -> Dict[str, Any]:
        path = f"src/orchestration/workflows/{workflow_id}.yaml"
        with open(path, "r") as f:
            return yaml.safe_load(f)

    async def _run_tool_step(self, step: Dict[str, Any], context):
        tool_name = step.get("tool")
        tool = get_tool(tool_name)

        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")

        masked_input = mask_payload(context.entities)

        audit_log(
            event="tool_invocation",
            correlation_id=context.correlation_id,
            details={"tool": tool_name, "input": masked_input}
        )

        result = await tool(context)

        audit_log(
            event="tool_result",
            correlation_id=context.correlation_id,
            details={"tool": tool_name, "result": mask_payload(result)}
        )

        # Store result in context
        context.last_tool = tool_name
        context.last_result = result

        # Allow workflows to set final output
        if step.get("final"):
            context.output = result

    def _evaluate_decision(self, step: Dict[str, Any], context) -> str:
        condition = step.get("condition")

        # Evaluate condition in context namespace
        try:
            decision = eval(condition, {}, {"context": context})
        except Exception as e:
            raise ValueError(f"Decision evaluation failed: {e}")

        audit_log(
            event="decision_evaluated",
            correlation_id=context.correlation_id,
            details={"condition": condition, "result": decision}
        )

        return "on_true" if decision else "on_false"

    def _update_context(self, step: Dict[str, Any], context):
        updates = step.get("set", {})
        for key, value in updates.items():
            setattr(context, key, value)

        audit_log(
            event="context_updated",
            correlation_id=context.correlation_id,
            details={"updates": updates}
        )
