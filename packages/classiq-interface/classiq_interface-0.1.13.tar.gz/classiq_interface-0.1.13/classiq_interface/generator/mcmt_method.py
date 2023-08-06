import enum


class McmtMethod(str, enum.Enum):
    vchain = "vchain"
    recursive = "recursive"
    standard = "standard"
    standard_no_neg_ctrl = "standard_no_neg_ctrl"
