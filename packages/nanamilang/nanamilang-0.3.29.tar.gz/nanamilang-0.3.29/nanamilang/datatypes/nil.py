"""NanamiLang Nil Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from .base import Base


class Nil(Base):
    """NanamiLang Nil Data Type Class"""

    name: str = 'Nil'
    _expected_type = str
    _python_reference: str

    def __init__(self, reference: str) -> None:
        """NanamiLang Nil, initialize new instance"""

        ASSERT_COLLECTION_IS_NOT_EMPTY(
            reference,
            message='Nil: ref could not be empty'
        )

        super(Nil, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Nil, format() method implementation"""

        return 'nil'

    def origin(self) -> str:
        """NanamiLang Undefined, origin() method implementation"""

        return self._python_reference

    def reference(self) -> None:
        """NanamiLang Nil, reference() method implementation"""

        return None
