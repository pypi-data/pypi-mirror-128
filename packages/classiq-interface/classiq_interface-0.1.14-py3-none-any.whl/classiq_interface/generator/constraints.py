from collections import defaultdict
from typing import Dict, List, Optional, Union

import pydantic

import classiq_interface.generator.validations.flow_graph as flow_graph
from classiq_interface.generator.custom_functions import CustomFunctionLibraryData
from classiq_interface.generator.function_call import FunctionCall
from classiq_interface.generator.preferences.randomness import create_random_seed
from classiq_interface.generator.qiskit_quantum_gates import QiskitBuiltinQuantumGates
from classiq_interface.generator.range_types import NonNegativeIntRange
from classiq_interface.generator.result import QuantumFormat
from classiq_interface.generator.transpilation import TranspilationPreferences
from classiq_interface.generator.user_defined_function_params import CustomFunction

DEFAULT_MINIMAL_DEPTH = 1


# TODO define a type that can be used in variable declaration that is consistent with usage
def normalize_dict_key_to_str(d):
    return {k.name: v for k, v in d.items()}


class QuantumCircuitConstraints(pydantic.BaseModel):
    """
    Input constraints for the generated quantum circuit.
    """

    # TODO: Consider moving timeout outside of constraints, and supply it (optionally) separate of the constraints.
    # TODO: Remove hard coded timeout when issue,https://github.com/MiniZinc/minizinc-python/pull/8 is resolved
    timeout_seconds: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=300, description="Generation timeout in seconds"
    )
    qubit_count: pydantic.PositiveInt = pydantic.Field(
        default=...,
        description="Number of qubits in generated quantum circuit",
    )
    max_depth: pydantic.PositiveInt
    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )
    gate_count_constraints: Dict[
        QiskitBuiltinQuantumGates, NonNegativeIntRange
    ] = pydantic.Field(default_factory=lambda: defaultdict(NonNegativeIntRange))
    # Must be validated before logic_flow
    custom_function_library: Optional[CustomFunctionLibraryData] = pydantic.Field(
        default=None,
        description="The user-defined custom function library.",
    )
    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list,
        description="List of function calls to be applied in the circuit",
    )
    transpilation: Optional[TranspilationPreferences] = pydantic.Field(
        default_factory=TranspilationPreferences
    )
    output_format: Union[
        QuantumFormat,
        pydantic.conlist(
            item_type=QuantumFormat, min_items=1, max_items=len(QuantumFormat)
        ),
    ] = pydantic.Field(
        default=[QuantumFormat.QASM],
        description="The quantum circuit output format(s). "
        "When multiple formats are requested, only the first one will be presented. "
        "Note that generating the `ll` format (Microsoft QIR) takes an extra time.",
    )

    _gate_count_constraints = pydantic.validator(
        "gate_count_constraints", allow_reuse=True
    )(normalize_dict_key_to_str)

    draw_as_functions: bool = pydantic.Field(
        default=False,
        description="If true, the generation output will be "
        "visualized as functions and not as an unrolled circuit",
    )

    class Config:
        extra = "forbid"

    @pydantic.validator("logic_flow")
    def validate_logic_flow(cls, logic_flow: List[FunctionCall], values):
        if not logic_flow:
            return logic_flow

        library: CustomFunctionLibraryData = values.get("custom_function_library")
        for function_call in logic_flow:
            params = function_call.function_params
            if isinstance(params, CustomFunction):
                params.validate_custom_function_in_library(library=library)
                function_data = library.custom_functions_dict[params.name]
                params.generate_io_names(
                    input_set=function_data.input_set,
                    output_set=function_data.output_set,
                )
                function_call.validate_custom_function_io()

        flow_graph.validate_flow_graph(logic_flow)

        return logic_flow

    @pydantic.validator("output_format")
    def validate_output_format(cls, output_format):
        if isinstance(output_format, QuantumFormat):
            return [output_format]
        else:
            if len(output_format) == len(set(output_format)):
                return output_format
            else:
                raise ValueError(
                    f"{output_format=}\n"
                    "has at least one format that appears twice or more"
                )
