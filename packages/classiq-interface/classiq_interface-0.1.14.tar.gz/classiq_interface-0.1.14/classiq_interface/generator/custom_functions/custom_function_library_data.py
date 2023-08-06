from typing import Dict, Optional, Tuple

import pydantic

from classiq_interface.generator.custom_functions.custom_function_data import (
    CustomFunctionData,
)

DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME = "default_custom_function_library_name"


class CustomFunctionLibraryData(pydantic.BaseModel):
    """Facility to store user-defined custom functions."""

    name: pydantic.constr(
        strict=True, regex=r"^([a-z][a-z0-9]*)(_[a-z0-9]+)*\Z"  # noqa: F722
    ) = pydantic.Field(
        default=DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME,
        description="The name of the custom function library",
    )

    custom_functions_dict: Dict[str, CustomFunctionData] = pydantic.Field(
        default_factory=dict,
        description="A dictionary containing the custom functions in the library.",
    )

    functions: Optional[Tuple[CustomFunctionData, ...]] = pydantic.Field(
        default=None,
        description="A tuple for inputting custom functions to the library.",
    )

    @pydantic.validator("custom_functions_dict")
    def validate_custom_functions_dict(
        cls, custom_functions_dict: Dict[str, CustomFunctionData]
    ):
        if not all(
            function_data.name == name
            for name, function_data in custom_functions_dict.items()
        ):
            raise AssertionError("Bad custom_functions_dict encountered.")
        return custom_functions_dict

    @pydantic.validator("functions")
    def validate_functions(cls, functions: Optional[Tuple[CustomFunctionData]], values):
        if not functions:
            return None
        if values.get("custom_functions_dict"):
            raise ValueError("Expected only a single function data input field")
        values["custom_functions_dict"] = {
            function_data.name: function_data for function_data in functions
        }
        return None
