import typing

from PyQt6.QtGui import QValidator


class OnlyFloats(QValidator):
    def validate(self, string: str, index: int) -> typing.Tuple['QValidator.State', str, int]:
        if string and string[-1] != ' ':
            try:
                float(string)
                return QValidator.State.Acceptable, string, index
            except ValueError:
                pass
        return QValidator.State.Invalid, string, index
    