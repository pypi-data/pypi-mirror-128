"""NanamiLang Undefined Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from .base import Base


class Undefined(Base):
    """NanamiLang Undefined Data Type Class"""

    name: str = 'Undefined'
    _expected_type = str
    _python_reference: str

    def __init__(self, reference: str) -> None:
        """NanamiLang Undefined, initialize new instance"""

        ASSERT_COLLECTION_IS_NOT_EMPTY(
            reference,
            message='Undefined: ref could not be empty'
        )

        super(Undefined, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Undefined, format() method implementation"""

        return f'undefined({self.origin()})'

    def origin(self) -> str:
        """NanamiLang Undefined, origin() method implementation"""

        return self._python_reference

    def reference(self) -> None:
        """NanamiLang Undefined, reference() method implementation"""

        return None
