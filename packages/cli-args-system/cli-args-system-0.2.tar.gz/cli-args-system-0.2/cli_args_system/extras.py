from typing import Union


def format_flag(
        flag: str,
        case_sensitive: bool,
        flag_identifier: str,
        infinity_identifier: bool) -> str:
    """this method is responsible for format a given flag \n
    flag: the flag \n
    case_sensitive: if false all will be lower\n
    flag_identifier: the char who identifies the flag ex: -b i=(-)\n
    infinity_identifier: if its possible to set ---x flags\n"""
    if not case_sensitive:
        flag = flag.lower()

    # if identifier is false, just remove the first char
    if not infinity_identifier:
        return flag[1::]

    # this loop is to find the first char that
    # is not the identifier
    for index, char in enumerate(flag):
        # when find the difference split the flag with the
        # current index
        if char != flag_identifier:
            return flag[index::]

    return flag


def is_a_flag(
        possible_flag: Union[str, int, float],
        case_sensitive: bool,
        flag_identifier: str) -> bool:
    """this method is used to recognize flags\n
    case_sensitive: if not wil compare in lower_case \n
    flag_identifier: the identifier tha tels if its a flag\n"""

    # this is for when the method is called
    # with numbers args
    if possible_flag.__class__ in [int, float]:
        return False

    if not case_sensitive:
        possible_flag = possible_flag.lower()

    # if char[0] its equal to flag_identifier and the
    # len of comparison is > 1 means its a flag
    # the len comparison is to not return true for "-" args
    if possible_flag[0] == flag_identifier and len(possible_flag) > 1:
        return True

    return False


def get_flags(
        args: list,
        flag_identifier: str,
        case_sensitive: bool,
        infinity_identifier: bool) -> dict:
    """this method returns a dict, with all flags passed in args \n
    args: the list of args \n
    case_sensitive: if is False, the flags will be lower_case
    flag_identifier: the char that identifiers what is a flag, ex:"-"\n
    infinity_identifier: is is False, just the first element will be
    considered as a flag identifier \n"""
    # create the default dict, and default flag
    flags: dict = {'default': []}
    current_flag = 'default'

    # go in a loop for all args
    for arg in args:

        # if is a flag is true, changes the current flags
        if is_a_flag(possible_flag=arg, case_sensitive=case_sensitive, flag_identifier=flag_identifier):
            # changes the current flag
            current_flag = format_flag(
                flag=arg,
                case_sensitive=case_sensitive,
                flag_identifier=flag_identifier,
                infinity_identifier=infinity_identifier
            )
            # this is to prevent previews equals current flags
            if current_flag not in flags.keys():
                # creates a new list inside the flags dict
                flags[current_flag] = []
        else:
            # if is not a flag, append with tue current flag
            flags[current_flag].append(arg)
    return flags


def convert_number(possible_number: str) -> Union[str, float, int]:
    """convert the possible_number  in a number if its possible,
    case if were not possible to convert, will return the possible_number
    (the same arg of method)"""

    try:
        # try to cast in an int
        return int(possible_number)
    except ValueError:
        try:
            # case cat a Value error, try to cast in a float
            return float(possible_number)
        except ValueError:
            # case if were not a int either a float, will cat here
            # and return the same arg
            return possible_number


def format_args(args: list, consider_first: bool, case_sensitive=bool, convert_numbers=bool):
    """this method format args, based on args passed
    args: the list of "argv"
    consider_first: if the first element of args is to be considered
    case_sensitive: if False, all will be lower
    convert_numbers: convert numbers in float or int if possible"""
    # split the args removing the first occurrence, if not consider first
    if not consider_first:
        args = args[1::]

    # map the args to all be lower
    if not case_sensitive:
        args = list(map(lambda arg: arg.lower(), args))

    # make a mapping calling the convert number function
    if convert_numbers:
        args = list(map(convert_number, args))
    return args


def cast_list(*elements) -> list:
    """this method transform everything in a list, ex:\n
    cast_list("a","b") returns: ["a","b"]\n
    cast_list([1,2]) returns: [1,2]\n"""
    # when * is used all the arguments will be passed as tuple

    # means just one element were passed as arg
    if len(elements) == 1:
        # means nothing were passed as arg
        if elements[0] is None:
            return []

        # means a tuple or list were passed as argument
        if elements[0].__class__ in [list, tuple]:
            # transform this in a list
            return list(elements[0])

        # else will make a list with elements 0
        # this is when a str or int is passed
        return [elements[0]]
    else:

        # if its a larger element, just cast with list
        return list(elements)


def get_num_comparison(o: Union[int, list, tuple]) -> Union[int, None]:
    object_type = o.__class__
    if object_type == int:
        return o
    if object_type in [list, tuple]:
        return len(o)
    return None
