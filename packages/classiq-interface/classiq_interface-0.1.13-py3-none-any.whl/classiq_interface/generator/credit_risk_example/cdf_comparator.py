from enum import Enum

from classiq_interface.generator.arith import binary_ops
from classiq_interface.generator.arith.register_user_input import RegisterUserInput


class CDFComparator(binary_ops.LessEqual):
    def create_io_enums(self):

        if isinstance(self.left_arg, RegisterUserInput) and isinstance(
            self.right_arg, RegisterUserInput
        ):
            self._input_enum = Enum(
                "BinaryOpInputs",
                {
                    self.left_arg.name: self.left_arg.name,
                    self.right_arg.name: self.right_arg.name,
                },
            )
            self._output_enum = Enum(
                "BinaryOpOutputs",
                {
                    self.output_name: self.output_name,
                    self.left_arg.name: self.left_arg.name,
                    self.right_arg.name: self.right_arg.name,
                },
            )
            return

        if isinstance(self.left_arg, RegisterUserInput):
            arg_name = self.left_arg.name
        else:
            assert isinstance(
                self.right_arg, RegisterUserInput
            ), "At least one argument should be a register"
            arg_name = self.right_arg.name

        self._input_enum = Enum("BinaryOpInputs", {arg_name: arg_name})
        self._output_enum = Enum(
            "BinaryOpOutputs",
            {self.output_name: self.output_name, arg_name: arg_name},
        )
