import pydantic


class SquareClusterEntanglerParameters(pydantic.BaseModel):
    num_of_qubits: pydantic.conint(ge=2)
    schmidt_rank: pydantic.conint(ge=0)


class Open2DClusterEntanglerParameters(pydantic.BaseModel):
    qubit_count: pydantic.conint(ge=2)
    schmidt_rank: pydantic.conint(ge=0)
