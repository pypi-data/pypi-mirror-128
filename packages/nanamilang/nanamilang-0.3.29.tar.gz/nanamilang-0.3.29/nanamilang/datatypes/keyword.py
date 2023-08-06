"""NanamiLang Keyword Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import ASSERT_COLLECTION_IS_NOT_EMPTY
from .base import Base


class Keyword(Base):
    """NanamiLang Keyword Data Type Class"""

    name: str = 'Keyword'
    _expected_type = str
    _python_reference: str

    def __init__(self, reference: str) -> None:
        """NanamiLang Keyword, initialize new instance"""

        ASSERT_COLLECTION_IS_NOT_EMPTY(
            reference,
            message='Keyword: ref could not empty'
        )

        super(Keyword, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Keyword, format() method implementation"""

        return f':{self._python_reference}'
