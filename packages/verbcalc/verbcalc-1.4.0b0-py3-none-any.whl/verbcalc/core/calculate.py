"""
Allows making calculations.
"""
from verbcalc.core.dispatcher import Dispatcher, InvalidExpressionException
from verbcalc.core.translator.translator import translate
from verbcalc.core.answers import CustomAnswers

DEFAULT_DISPATCHER = Dispatcher()


def calculate(sentence: str,
              dispatcher: Dispatcher = DEFAULT_DISPATCHER,
              silent: bool = False
              ) -> str:
    """
    Calculates result from sentence.

    Parameters:
        sentence:
            Sentence to take calculation from.

        dispatcher:
            Dispatcher object to use, if none provided it will use default one.

        silent:
            Returns only the answer instead of an entire answer sentence

    Returns:
        Calculated sentence.
    """

    try:
        result = dispatcher.dispatch(translate(sentence).split())

        answer = str(int(result)) if result % 1 == 0 else str(result)

        return answer if silent else ' '.join([CustomAnswers().get_phrase(),
                                               answer])

    except ZeroDivisionError:
        return 'You cannot divide by zero!'
    except InvalidExpressionException:
        return 'Your expression is invalid'
