"""NanamiLang Set Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF
from .base import Base


class Set(Base):
    """NanamiLang Set Data Type Class"""

    name: str = 'Set'
    _expected_type = set
    _python_reference: set

    def __init__(self, reference: set) -> None:
        """NanamiLang Set, initialize new instance"""

        ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF(
            list(reference),
            Base,
            message='Set: only can contain Nanamilang data types'
        )

        super(Set, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang Set, format() method implementation"""

        return '#{' + f'{" ".join([i.format() for i in self.reference()])}' + '}'

    def reference_as_list(self) -> list:
        """NanamiLang Set, reference_as_list() method implementation"""

        return list(self.reference())
