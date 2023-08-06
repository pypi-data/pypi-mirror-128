import base64
import enum
import io
import json
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import pydantic
from PIL import Image

from classiq_interface.generator.generation_metadata import GenerationMetadata
from classiq_interface.generator.synthesis_metrics import SynthesisMetrics

_MAXIMUM_STRING_LENGTH = 250


class LongStr(str):
    def __repr__(self):
        if len(self) > _MAXIMUM_STRING_LENGTH:
            length = len(self)
            return f'"{self[:4]}...{self[-4:]}" ({length=})'
        return super().__repr__()


class QuantumFormat(str, enum.Enum):
    QASM = "qasm"
    QSHARP = "qs"
    QIR = "ll"
    IONQ = "ionq"
    CIRQ = "cirq"


class GenerationStatus(str, enum.Enum):
    NONE = "none"
    SUCCESS = "success"
    UNSAT = "unsat"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    ERROR = "error"


# TODO: Merge all output formats to single field (dictionary?) to avoid clutter
class GeneratedCircuit(pydantic.BaseModel):
    qubit_count: Optional[int]
    depth: Optional[int]
    qasm: Optional[str]
    qsharp: Optional[str]
    qir: Optional[str]
    ionq: Optional[str]
    cirq: Optional[str]
    output_format: List[QuantumFormat]
    image_raw: str
    interactive_html: Optional[str]
    metadata: GenerationMetadata
    synthesis_metrics: Optional[SynthesisMetrics]

    def show(self) -> None:
        self.image.show()

    def show_interactive(self):
        with tempfile.NamedTemporaryFile(
            "w", delete=False, suffix="_interactive_circuit.html"
        ) as f:
            url = f"file://{f.name}"
            f.write(self.interactive_html)
        webbrowser.open(url)

    @property
    def image(self):
        return Image.open(io.BytesIO(base64.b64decode(self.image_raw)))

    def save_results(self, filename: Optional[Union[str, Path]] = None) -> None:
        """
        Saves generated circuit results as json.
            Parameters:
                filename (Union[str, Path]): Optional, path + filename of file.
                                             If filename supplied add `.json` suffix.

            Returns:
                  None
        """
        if filename:
            path = Path(filename)
        else:
            path = Path(
                f"generated_circuit_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.json"
            )
        path.write_text(json.dumps(self.dict(), indent=4))

    @pydantic.validator("qasm")
    def reformat_qasm(cls, v):
        return LongStr(v)

    @pydantic.validator("image_raw")
    def reformat_image_raw(cls, v):
        return LongStr(v)

    @pydantic.validator("interactive_html")
    def reformat_interactive_html(cls, v):
        return LongStr(v)


class GenerationResult(pydantic.BaseModel):
    status: GenerationStatus
    details: Union[GeneratedCircuit, str]
