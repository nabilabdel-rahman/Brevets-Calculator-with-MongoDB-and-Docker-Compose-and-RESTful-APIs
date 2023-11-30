"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

from acp_times import open_time, close_time
import arrow

def test_start():
    date = arrow.get("2021-01-01T00:00")
    distance = 200
    
    assert open_time(0, distance, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).format('YYYY-MM-DDTHH:mm')
    
def test_max_times():
    date = arrow.get("2021-01-01T00:00")
    
    assert close_time(200, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=810).format('YYYY-MM-DDTHH:mm')
    
    assert close_time(300, 300, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1200).format('YYYY-MM-DDTHH:mm')

    assert close_time(400, 400, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1620).format('YYYY-MM-DDTHH:mm')

    assert close_time(600, 600, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=2400).format('YYYY-MM-DDTHH:mm')

    assert close_time(1000, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=4500).format('YYYY-MM-DDTHH:mm')

def test_min_times():
    date = arrow.get("2021-01-01T00:00")

    assert open_time(200, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=353).format('YYYY-MM-DDTHH:mm')
    
    assert open_time(300, 300, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=540).format('YYYY-MM-DDTHH:mm')

    assert open_time(400, 400, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=728).format('YYYY-MM-DDTHH:mm')

    assert open_time(600, 600, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1128).format('YYYY-MM-DDTHH:mm')

    assert open_time(1000, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1985).format('YYYY-MM-DDTHH:mm')

def test_oddities():
    date = arrow.get("2021-01-01T00:00")

    assert open_time(5, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=9).format('YYYY-MM-DDTHH:mm')
    assert close_time(5, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get("2021-01-01T01:15").format('YYYY-MM-DDTHH:mm')

    assert open_time(10, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=18).format('YYYY-MM-DDTHH:mm')
    assert close_time(10, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get("2021-01-01T01:30").format('YYYY-MM-DDTHH:mm')

    assert close_time(15, 200, date).format('YYYY-MM-DDTHH:mm') != arrow.get("2021-01-01T01:00").format('YYYY-MM-DDTHH:mm')


def test_exceptions():
    date = arrow.get("2021-01-01T00:00")

    assert open_time(200, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=353).format('YYYY-MM-DDTHH:mm')
    assert close_time(200, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=810).format('YYYY-MM-DDTHH:mm')

    assert open_time(200, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=353).format('YYYY-MM-DDTHH:mm')
    assert close_time(200, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=800).format('YYYY-MM-DDTHH:mm')

    assert open_time(400, 400, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=728).format('YYYY-MM-DDTHH:mm')
    assert close_time(400, 400, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1620).format('YYYY-MM-DDTHH:mm')

    assert open_time(400, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=728).format('YYYY-MM-DDTHH:mm')
    assert close_time(400, 1000, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(minutes=1600).format('YYYY-MM-DDTHH:mm')

def test_zero_close_times():
    date = arrow.get("2021-01-01T00:00")

    assert close_time(0, 200, date).format('YYYY-MM-DDTHH:mm') == arrow.get(date).shift(hours=1).format('YYYY-MM-DDTHH:mm')

def test_new_year():
    assert open_time(60, 200, arrow.get("2020-12-31T23:59")).format('YYYY-MM-DDTHH:mm') == arrow.get("2021-01-01T01:45").format('YYYY-MM-DDTHH:mm')
    assert close_time(60, 200, arrow.get("2020-12-31T23:59")).format('YYYY-MM-DDTHH:mm') == arrow.get("2021-01-01T03:59").format('YYYY-MM-DDTHH:mm')