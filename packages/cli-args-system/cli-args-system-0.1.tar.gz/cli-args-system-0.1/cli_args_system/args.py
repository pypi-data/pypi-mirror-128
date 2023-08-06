from sys import argv
from copy import deepcopy
from json import dumps
from typing import Any

from cli_args_system.extras import format_args, get_flags, cast_list
from cli_args_system.flags_content import FlagsContent
from cli_args_system.list_args import ListArgs


class Args(ListArgs):

    def __init__(self, consider_first=False, flags_case_sensitive=False, args_case_sensitive=True, convert_numbers=True,
                 flag_identifier='-', infinity_identifier=True, args=None) -> None:
        """consider_first: if is to consider the first argv element,
        if false, argv[0] will be removed\n
        flags_case_sensitive: if false, all flags will be lowercase \n
        convert_numbers: if True, it will convert in float or int all
        found numbers in argv\n
        flag_identifier: the char that is used to identifies a flag, ex:
        in "--a", the flag_identifier is "-"\n
        infinity_identifier: if false, just the first char will be considered
        as the flag identifier\n
        """
        super().__init__()
        if args is None:
            args = deepcopy(argv)
        self.args = format_args(
            args=args,
            consider_first=consider_first,
            case_sensitive=args_case_sensitive,
            convert_numbers=convert_numbers
        )

        self.flags = get_flags(
            args=self.args,
            flag_identifier=flag_identifier,
            case_sensitive=flags_case_sensitive,
            infinity_identifier=infinity_identifier
        )
        self.flags_names = list(self.flags.keys())

    def flags_content(self, *flags) -> FlagsContent:
        """returns a FlagsContent object, witch is a group of
        the found flags in argv\n
        flags: the flags that you want to find,
        you can pass a list, tuple, or str"""

        # generate a patronized list of flags
        flags_list = cast_list(*flags)

        # create the filtered args list that will be used
        # to insert the found flags content
        filtered_args = []

        at_least_one_flag_exist = False

        # loop into the flags lis
        for flag in flags_list:
            if flag.__class__ != str:
                raise TypeError('only str are valid for flags')
            try:
                # try to insert into the filtered list
                filtered_args += self.flags[flag]
                # if pass till here, means this flag were inserted in
                # the filtered args
                at_least_one_flag_exist = True
            except KeyError:
                pass

        # if at least one flag were found, returns FlagsContent object with
        # filtered args
        if at_least_one_flag_exist:
            return FlagsContent(content=filtered_args)
        else:
            # otherwise returns FlagsContent , with None as content
            return FlagsContent(content=None)

    def __eq__(self, o: Any) -> bool:
        """this methods is called when == is used"""

        # means that is a empty comparison
        # so it will return True if self.args is empty
        if o == {} or o == []:
            return True if self.args == [] else False

        comparison_type = o.__class__

        # if comparison type its a int, it will compare with args size
        if comparison_type == int:
            return o == len(self.args)

        # if is a tuple, it will cast the comparison
        # and compare with args
        if comparison_type == tuple:
            return list(o) == self.args

        # same with list, but don't cast it
        if comparison_type == list:
            return o == self.args

        # if is a dict, it will compare with the self.flags
        if comparison_type == dict:
            return o == self.flags

        return False

    def __repr__(self) -> str:
        """returns a json representation of the flags attribute"""
        return dumps(self.flags, indent=4)
