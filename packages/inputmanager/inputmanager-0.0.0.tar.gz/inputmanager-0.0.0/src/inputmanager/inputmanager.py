#!/usr/bin/env python3
"""
Created on Tue Apr 23 21:58:12 2019.

@author: Tristan Muscat
"""
# =============================================================================
# Libraries
# =============================================================================
from collections.abc import Callable
from collections.abc import Iterable
from typing import List
from typing import Optional
from typing import Union

# =====================================================================================================================
# Error class specific to typos
# =====================================================================================================================


class InputException(Exception):
    """Typing error."""

    def __init__(self, message):
        super().__init__(message)


# =====================================================================================================================
# Input management module
# =====================================================================================================================


def read_line(
    str_prompt: str,
    bl_case: Optional[bool] = False,
    set_values: Optional[Iterable[Union[str, float, bool]]] = None,
) -> str:
    """Read an input from the user after a prompt.

    The function prompt a user to enter an input, then verifies that the input is valid.

    Parameters
    ----------
    str_prompt: str
        The prompt displayed while waiting for an input.
    bl_case: boolean, optinal
        Should the program check for case. Default is False.
    set_test: set, optinal
        iterable of valid values the input can be. If None then the input can be anything. Default is None.

    Returns
    -------
    res: str
        The input validated.
    """
    res: str = input(str_prompt)  # To prompt an input.

    # Gotta be sure.
    if res is None:
        raise InputException("Input error !")

    if not bl_case and set_values:
        set_values = {str(x).lower() for x in set_values}

    # if a set is given, then we check the input is in this set.
    if set_values and res.lower() not in set_values:
        raise InputException("Input error !")

    return res


def read_yes_no(
    str_prompt: str,
    lst_pos_vals: Optional[List[Union[str, float, bool]]] = None,
    lst_neg_vals: Optional[List[Union[str, float, bool]]] = None,
    bl_res_bolean: Optional[bool] = True,
) -> Union[str, bool]:
    """Ask a yes or no question and get the answer.

    Compare the input to a set of accepted values. Returns the answer or an indicator that the answer is valid.

    Paramters
    ---------
    str_prompt: str
        The prompt displayed while waiting for an input.
    lst_pos_vals: list, optinal
        set of positive valid values the input can be. If None then a default set is used. Default is None.
    lst_neg_vals: list, optinal
        set of negative valid values the input can be. If None then a default set is used. Default is None.
    bl_res_bolean: bool, optinal
        Should the function return the answer or indicate if the answer is valid. Default is True.

    Returns
    -------
    res:
        the response, can be a string or a boolean.
    """
    # If no set is provided for the validation, we use a default set of values.
    # We use a or here, because if one is forgotten, might as well use default for both.
    if not lst_pos_vals:
        lst_pos_vals = ["yes", "y", "oui", "o"]

    if not lst_neg_vals:
        lst_neg_vals = ["no", "n", "non"]

    # Now we ask the question, get the answer and check it.
    res: Union[str, bool]
    res = read_line(str_prompt, False, lst_pos_vals + lst_neg_vals)

    # If the expected returned value is a boolean we convert it.
    if bl_res_bolean:
        res = res in lst_pos_vals

    return res


def read_numeric(
    str_prompt: str,
    bl_int: Optional[bool] = True,
    num_lb: Optional[float] = None,
    num_ub: Optional[float] = None,
    bl_inc_lb: Optional[bool] = True,
    bl_inc_ub: Optional[bool] = True,
) -> float:
    """Read a numeric (integer or not) value between bonds.

    Parameters
    ----------
    str_prompt: str
        The prompt displayed while waiting for an input.
    bl_int: bool, optional
        Should the input be an integer or can it be a float.
    num_lb: num, optional
        The lower bound. The default is None.
    num_ub: num, optional
        The upper bound. The default is None.
    bl_inc_lb: bool, optional
        Should the lower bound be included or not. The default is True.
    bl_inc_ub: num, optional
        Should the upper bound be included or not. The default is True.

    Returns
    -------
    res:
        The input, can be an integer or a float.
    """
    str_input: str = read_line(str_prompt)  # Getting the input.
    res: float

    # If an integer is expeceted as the input, then we test it first as it is the stronger constraint.
    if bl_int:
        try:
            res = int(str_input)
        except ValueError:
            raise InputException("Input must be an integer.")
    # If bl_int is False that means we still expect a numerical value, so testing for a float is engough.
    else:
        try:
            res = float(str_input)
        except ValueError:
            raise InputException("Input must be numeric.")

    if num_ub is not None and ((bl_inc_ub and res > num_ub) or (not bl_inc_ub and res >= num_ub)):
        raise InputException("Expected a smaller input.")

    if num_lb is not None and ((bl_inc_lb and res < num_lb) or (not bl_inc_lb and res <= num_lb)):
        raise InputException("Expected a bigger input.")

    return res


def force_read(fun_reader: Callable[..., Union[str, float, bool]], *argv, **kwargs) -> Union[str, float, bool]:
    """Loop until it gets a valid inputs.

    Ask an input and ask again if their is an error. It allows a program not to crash because of a typo.

    Parameters
    ----------
    fun_reader: function
        The function used to read an input.
    *argv: list
        The arguments of the chosen function.
    **kwargs: dict
        The arguments of the chosen function.

    Returns
    -------
    res:
        The input. Can be several types.
    """
    bl_intput_ok: bool = False
    res: Union[str, float, bool]

    # The question is repeated until the user gives an expected answer.
    while not bl_intput_ok:
        try:
            # Any of the "read" functions can be called, so the type
            # can be string, numeric or boolean.
            res = fun_reader(*argv, **kwargs)
            bl_intput_ok = True

        except InputException as e:
            print(e)

    return res
