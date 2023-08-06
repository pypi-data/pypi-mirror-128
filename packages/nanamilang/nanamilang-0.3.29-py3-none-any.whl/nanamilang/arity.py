"""NanamiLang Arity Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang.shortcuts import (
    ASSERT_IS_INSTANCE_OF, ASSERT_LIST_LENGTH_IS_EVEN,
    ASSERT_COLLECTION_IS_NOT_EMPTY, ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF
)


class Arity:
    """NanamiLang, builtin.Arity"""
    Even: str = 'Even'
    AtLeastOne: str = 'AtLeastOne'
    LengthVariants: str = 'LengthVariants'
    FunctionAllArgsAre: str = 'FunctionAllArgsAre'
    FunctionAllArgsVariants: str = 'FunctionAllArgsVariants'
    FunctionArgumentsTypeMap: str = 'FunctionArgumentsTypeMap'

    @staticmethod
    def validate(label: str, collection: list, flags: list):
        """NanamiLang Arity.validate() function implementation"""

        for maybe_flag_pair in flags:
            if len(maybe_flag_pair) == 2:
                flag, values = maybe_flag_pair
            else:
                flag, values = maybe_flag_pair[0], None
            if flag == Arity.AtLeastOne:
                ASSERT_COLLECTION_IS_NOT_EMPTY(
                    collection,
                    f'{label}: '
                    f'invalid arity, expected at least one form/argument'
                )
            elif flag == Arity.LengthVariants:
                assert len(collection) in values, (
                    f'{label}: '
                    f'invalid arity, numbers of form(s)/argument(s) possible: {values}'
                )
            elif flag == Arity.FunctionAllArgsAre:
                desired = values[0]
                ASSERT_EVERY_COLLECTION_ITEM_IS_INSTANCE_OF(
                    collection, desired,
                    f'{label}: '
                    f'all function arguments need to be a {desired.name}'
                )
            elif flag == Arity.FunctionAllArgsVariants:
                desired = [v.name for v in values]
                assert len(list(filter(lambda x: x.name in desired,
                                       collection))) == len(collection), (
                    f'{label}: '
                    f'all function arguments need to be either {" or ".join(desired)}'
                )
            elif flag == Arity.FunctionArgumentsTypeMap:
                for [arg, arg_desc] in zip(collection, values):
                    arg_name, arg_type = arg_desc
                    ASSERT_IS_INSTANCE_OF(
                        arg, arg_type, f'{label}: {arg_name} needs to be {arg_type.name}'
                    )
            elif flag == Arity.Even:
                ASSERT_LIST_LENGTH_IS_EVEN(
                    collection,
                    f'{label}: invalid arity, number of function arguments must be even')
