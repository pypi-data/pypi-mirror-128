"""NanamiLan HashMap Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from functools import reduce
from nanamilang.shortcuts import ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF
from .base import Base
from .nil import Nil


class HashMap(Base):
    """NanamiLang HashMap Data Type Class"""

    name: str = 'HashMap'
    _expected_type = dict
    _python_reference: dict

    def get(self, key: Base) -> Base:
        """NanamiLang HashMap, get() implementation"""

        for k, v in self.reference().items():
            if k.name == key.name:
                if k.reference() == key.reference():
                    return v
        return Nil('nil')
        # Since, we can get None, we need to cast it to the NanamiLang Nil

    def __init__(self, reference: dict) -> None:
        """NanamiLang HashMap, initialize new instance"""

        if reference.items():
            ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF(
                list(reduce(lambda e, x: e + (x[0], x[1]), reference.items())),
                Base,
                message='HashMap: only can contain Nanamilang data types'
            )

        super(HashMap, self).__init__(reference=reference)

    def format(self) -> str:
        """NanamiLang HashMap, format() method implementation"""

        return '{' + f'{" ".join([f"{k.format()} {v.format()}" for k, v in self.reference().items()])}' + '}'

    def reference_as_list(self) -> list:
        """NanamiLang HashMap, reference_as_list() method implementation"""

        if self.reference().items():
            return reduce(lambda existing, current: existing + (current[0], current[1]), self.reference().items())
        else:
            return []
