from typing import Any, Dict, Optional


class OrchestrationContext:
    """
    Shared state for a single agentic workflow execution.

    This object is passed to:
    - Tools
    - Workflow runner
    - Governance modules
    - RPA bots
    - Adapters (ServiceNow, SuccessFactors)

    It provides:
    - Correlation ID for audit traceability
    - User identity and role
    - Intent and extracted entities
    - Workflow ID
    - Last tool executed + result
    - Final output for the orchestrator to return
    """

    def __init__(
        self,
        correlation_id: str,
        user: Dict[str, Any],
        intent: str,
        entities: Dict[str, Any],
        raw_input: Dict[str, Any]
    ):
        self.correlation_id = correlation_id

        # User context (Moveworks-style payload)
        self.user = user or {}
        self.user_id = self.user.get("id")
        self.user_role = self.user.get("role", "employee")

        # Intent + entities
        self.intent = intent
        self.entities = entities or {}

        # Raw input for audit purposes
        self.raw_input = raw_input

        # Workflow metadata
        self.workflow_id: Optional[str] = None

        # Execution state
        self.last_tool: Optional[str] = None
        self.last_result: Optional[Dict[str, Any]] = None

        # Final output returned to the user
        self.output: Optional[Dict[str, Any]] = None

    # ----------------------------------------------------------------------
    # Convenience helpers
    # ----------------------------------------------------------------------

    def set_entity(self, key: str, value: Any):
        """Update or add an entity."""
        self.entities[key] = value

    def get_entity(self, key: str, default=None):
        """Retrieve an entity safely."""
        return self.entities.get(key, default)

    def set_output(self, result: Dict[str, Any]):
        """Set the final output for the orchestrator."""
        self.output = result

    def __repr__(self):
        return (
            f"OrchestrationContext("
            f"correlation_id={self.correlation_id}, "
            f"user_id={self.user_id}, "
            f"intent={self.intent}, "
            f"entities={self.entities}, "
            f"workflow_id={self.workflow_id}, "
            f"last_tool={self.last_tool})"
        )
