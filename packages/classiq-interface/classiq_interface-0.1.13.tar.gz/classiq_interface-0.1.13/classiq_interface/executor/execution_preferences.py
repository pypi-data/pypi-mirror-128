import enum
from typing import List, Optional, Union

import pydantic

from classiq_interface.backend.backend_preferences import (
    AwsBackendPreferences,
    AzureBackendPreferences,
    IBMBackendPreferences,
    IonqBackendPreferences,
)
from classiq_interface.executor.error_mitigation import ErrorMitigationMethod
from classiq_interface.generator.noise_properties import NoiseProperties
from classiq_interface.generator.preferences.randomness import create_random_seed


class AmplitudeEstimation(pydantic.BaseModel):
    alpha: float = pydantic.Field(
        default=0.05, description="Confidence level of the AE algorithm"
    )
    epsilon: float = pydantic.Field(
        default=0.01, description="precision for estimation target `a`"
    )
    binary_search_threshold: Optional[pydantic.confloat(ge=0, le=1)] = pydantic.Field(
        description="The required probability on the tail of the distribution (1 - percentile)"
    )

    objective_qubits: List[int] = pydantic.Field(
        default=[],
        description="list specifying on which qubits to perform the amplitude estimation",
    )


class AmplitudeAmplification(pydantic.BaseModel):
    iterations: Union[List[int], int, None] = pydantic.Field(
        default=None, description="Number or list of numbers of iteration to use"
    )
    growth_rate: Optional[float] = pydantic.Field(
        default=None,
        description="Number of iteration used is set to round(growth_rate**iterations)",
    )
    sample_from_iterations: bool = pydantic.Field(
        default=False,
        description="If True, number of iterations used is picked randomly from [1, iteration] range",
    )


class CostType(str, enum.Enum):
    MIN = "MIN"
    AVERAGE = "AVERAGE"
    CVAR = "CVAR"


class OptimizerType(str, enum.Enum):
    COBYLA = "COBYLA"
    SPSA = "SPSA"
    L_BFGS_B = "L_BFGS_B"
    NELDER_MEAD = "NELDER_MEAD"
    ADAM = "ADAM"


class OptimizerPreferences(pydantic.BaseModel):
    type: OptimizerType = pydantic.Field(
        default=OptimizerType.COBYLA, description="Classical optimization algorithm."
    )
    num_shots: pydantic.PositiveInt = pydantic.Field(
        default=100, description="Number of repetitions of the quantum ansatz."
    )
    cost_type: CostType = pydantic.Field(
        default=CostType.CVAR,
        description="Summarizing method of the measured bit strings",
    )
    alpha_cvar: pydantic.confloat(gt=0, le=1) = pydantic.Field(
        default=None, description="Parameter for the CVAR summarizing method"
    )
    max_iteration: pydantic.PositiveInt = pydantic.Field(
        default=100, description="Maximal number of optimizer iterations"
    )
    tolerance: pydantic.PositiveFloat = pydantic.Field(
        default=None, description="Final accuracy in the optimization"
    )
    step_size: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        description="step size for numerically " "calculating the gradient",
    )

    @pydantic.validator("alpha_cvar", pre=True, always=True)
    def check_alpha_cvar(cls, alpha_cvar, values):
        cost_type = values.get("cost_type")
        if alpha_cvar is not None and cost_type != CostType.CVAR:
            raise ValueError("Use CVAR params only for CostType.CVAR.")

        if alpha_cvar is None and cost_type == CostType.CVAR:
            alpha_cvar = 0.04

        return alpha_cvar

    @pydantic.validator("tolerance", pre=True, always=True)
    def check_tolerance(cls, tolerance, values):
        optimizer_type = values.get("type")
        if tolerance is not None and optimizer_type == OptimizerType.SPSA:
            raise ValueError("No tolerance param for SPSA optimizer")

        if tolerance is None and optimizer_type != OptimizerType.SPSA:
            tolerance = 0.001

        return tolerance

    @pydantic.validator("step_size", pre=True, always=True)
    def check_step_size(cls, step_size, values):
        optimizer_type = values.get("type")
        if step_size is not None and optimizer_type not in (
            OptimizerType.L_BFGS_B,
            OptimizerType.ADAM,
        ):
            raise ValueError("Use step_size only for L_BFGS_B or ADAM optimizers.")

        if step_size is None and optimizer_type in (
            OptimizerType.L_BFGS_B,
            OptimizerType.ADAM,
        ):
            step_size = 0.05

        return step_size


class VQEOptimization(pydantic.BaseModel):
    optimizer_preferences: OptimizerPreferences = pydantic.Field(
        default_factory=OptimizerPreferences,
        description="preferences for the VQE execution",
    )
    is_maximization: bool = pydantic.Field(
        default=False,
        description="Whether the VQE goal is to maximize",
    )
    initial_point: List[float] = pydantic.Field(
        default=None,
        description="Initial values for the ansatz parameters",
    )


class ExecutionPreferences(pydantic.BaseModel):
    num_shots: int = 100
    timeout_sec: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="If set, limits the execution runtime. Value is in seconds. Not supported on all platforms.",
    )
    amplitude_estimation: Optional[AmplitudeEstimation]
    amplitude_amplification: Optional[AmplitudeAmplification]
    vqe_optimization: Optional[VQEOptimization]
    error_mitigation_method: Optional[ErrorMitigationMethod] = pydantic.Field(
        default=None,
        description="Error mitigation method. Currently supports complete and tensored measurement calibration.",
    )
    noise_properties: Optional[NoiseProperties] = pydantic.Field(
        default=None, description="Properties of the noise in the circuit"
    )
    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )
    backend_preferences: Union[
        AzureBackendPreferences,
        IBMBackendPreferences,
        AwsBackendPreferences,
        IonqBackendPreferences,
    ] = pydantic.Field(
        default_factory=lambda: IBMBackendPreferences(
            backend_service_provider="IBMQ", backend_name="aer_simulator_statevector"
        ),
        description="Preferences for the requested backend to run the quantum circuit.",
    )
