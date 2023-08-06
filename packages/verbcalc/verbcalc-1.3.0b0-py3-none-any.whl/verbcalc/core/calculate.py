"""
Allows making calculations.
"""
from verbcalc.core.dispatcher import Dispatcher
from verbcalc.core.translator.translator import translate

DEFAULT_DISPATCHER = Dispatcher()


def calculate(sentence: str,
              dispatcher: Dispatcher = DEFAULT_DISPATCHER
              ) -> str:
    """
    Calculates result from sentence.

    Parameters:
        sentence:
            Sentence to take calculation from.

        dispatcher:
            Dispatcher object to use, if none provided it will use default one.

    Returns:
        Calculated sentence.
    """

    try:
        result = dispatcher.dispatch(translate(sentence).split())
        if result % 1 == 0:
            return 'The result is ' + str(int(result))
        else:
            return 'The result is ' + str(result)
    except ZeroDivisionError:
        return 'You cannot divide by zero!'
