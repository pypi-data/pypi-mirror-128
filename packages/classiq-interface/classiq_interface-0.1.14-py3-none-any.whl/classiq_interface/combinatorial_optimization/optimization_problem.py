from typing import Dict, Union

import pydantic

from classiq_interface.backend.backend_preferences import (
    AwsBackendPreferences,
    AzureBackendPreferences,
    IBMBackendPreferences,
)
from classiq_interface.combinatorial_optimization.preferences import QAOAPreferences
from classiq_interface.executor.execution_preferences import OptimizerPreferences


class OptimizationProblem(pydantic.BaseModel):
    qaoa_preferences: QAOAPreferences = pydantic.Field(
        default_factory=QAOAPreferences,
        description="preferences for the QAOA algorithm",
    )
    optimizer_preferences: OptimizerPreferences = pydantic.Field(
        default_factory=OptimizerPreferences,
        description="preferences for the VQE execution",
    )
    serialized_model: Dict = None
    backend_preferences: Union[
        AzureBackendPreferences, IBMBackendPreferences, AwsBackendPreferences
    ] = pydantic.Field(
        default_factory=lambda: IBMBackendPreferences(
            backend_service_provider="IBMQ", backend_name="aer_simulator"
        ),
        description="Preferences for the requested backend to run the quantum circuit.",
    )
