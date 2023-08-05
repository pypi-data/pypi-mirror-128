import os
import numpy
from botcity.plugins.csv import BotCSVPlugin

cur_dir = os.path.abspath(os.path.dirname(__file__))


def test_read():
    """
    Read test.

    Performs:
        read(),
        add_row(),
        sort(),
        as_list(),
        as_dict()
    """
    # read() + add_row() + sort()
    answer = BotCSVPlugin().read(os.path.join(cur_dir, 'read.csv')).add_row([0, 22]).sort(['H1', 'H2'], False)

    # as_list() + as_list
    assert numpy.array_equal(answer.as_list(), [[10, 11], [0, 22], [0, 1]])
    assert answer.as_dict() == {'H1': [10, 0, 0], 'H2': [11, 22, 1]}


def test_write():
    """
    Write test.

    Performs:
        add_rows(),
        sort(),
        as_dict(),
        write()
    """
    # add_rows() + sort() + as_dict()
    source = [{'H1': 0, 'H2': 22}, {'H1': 10, 'H2': 11}, {'H1': 0, 'H2': 1}]
    answer = BotCSVPlugin().add_rows(source).sort(['H1', 'H2'], False)
    assert answer.as_dict() == {'H1': [10, 0, 0], 'H2': [11, 22, 1]}

    # write()
    # TODO
