import sys  # noqa: F401
from unittest.mock import DEFAULT, MagicMock, call, patch

import circum.endpoint  # noqa: F401

import circum_hc_sr04.hc_sr04
from circum_hc_sr04.hc_sr04 import _hc_sr04, _update_thread, run_hc_sr04

import pytest


def test_hc_sr04():
    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        top = MagicMock()

        with patch("circum_hc_sr04.Bluetin_Echo.Bluetin_Echo.Echo") as echo_class:
            with patch("circum_hc_sr04.hc_sr04._create_tracker_thread") as thread:
                with patch("circum.endpoint.start_endpoint") as endpoint:

                    import circum_hc_sr04.hc_sr04  # noqa: F401
                    from circum_hc_sr04.hc_sr04 import hc_sr04, run_hc_sr04

                    echo_class.return_value = MagicMock()

                    expected_calls = [
                        # initialize Echo
                        call.echo(1, 2, 3),
                        # _create_tracker_thread
                        call.thread(echo_class(), 0, 4),
                        # start endpoint
                        call.endpoint(None, 'hc_sr04', run_hc_sr04),
                    ]

                    top.attach_mock(echo_class, 'echo')
                    top.attach_mock(thread, 'thread')
                    top.attach_mock(endpoint, 'endpoint')

                    _hc_sr04(None, 0, 1, 2, 3, 4)

                    top.assert_has_calls(expected_calls)


class EndLoopException(Exception):
    pass


class FakeTarget():
    def __init__(self, x, y, z, a):
        self.xPosCm = x
        self.yPosCm = y
        self.zPosCm = z
        self.amplitude = a


def test__update_thread_gettargets_returns_above_threshold():
    echo = MagicMock()

    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        import circum_hc_sr04
        from circum_hc_sr04.hc_sr04 import _update_thread

        with patch("circum_hc_sr04.hc_sr04.tracking_semaphore") as tracking_semaphore:

            echo.attach_mock(tracking_semaphore, 'tracking_semaphore')

            # run the loop once, then except out
            echo.read = MagicMock()
            echo.read.return_value = 300
            echo.read.side_effect = [DEFAULT, EndLoopException]

            expected_calls = [
                # _get_targets
                call.read('cm', 0),
                # _update_thread
                call.tracking_semaphore.acquire(),
                call.tracking_semaphore.release(),
                # _get_targets
                call.read('cm', 0),
            ]

            assert not circum_hc_sr04.hc_sr04.updated

            with pytest.raises(EndLoopException):
                _update_thread(echo, 0, 250)

            assert circum_hc_sr04.hc_sr04.updated

            circum_hc_sr04.hc_sr04.updated = False

            echo.assert_has_calls(expected_calls)

            circum_hc_sr04.hc_sr04.tracking_info["objects"] == []


def test__update_thread_gettargets_returns_target_once():
    echo = MagicMock()

    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        import circum_hc_sr04
        from circum_hc_sr04.hc_sr04 import _update_thread

        with patch("circum_hc_sr04.hc_sr04.tracking_semaphore") as tracking_semaphore:

            echo.attach_mock(tracking_semaphore, 'tracking_semaphore')

            # run the loop once, then except out
            echo.read = MagicMock()
            echo.read.return_value = 200
            echo.read.side_effect = [DEFAULT, EndLoopException]

            expected_calls = [
                # _get_targets
                call.read('cm', 0),
                # _update_thread
                call.tracking_semaphore.acquire(),
                call.tracking_semaphore.release(),
                # _get_targets
                call.read('cm', 0),
            ]

            expected_targets = [
                {
                    "x": 0,
                    "y": 0,
                    "z": 2
                }
            ]

            assert not circum_hc_sr04.hc_sr04.updated

            with pytest.raises(EndLoopException):
                _update_thread(echo, 0, 250)

            assert circum_hc_sr04.hc_sr04.updated

            circum_hc_sr04.hc_sr04.updated = False

            echo.assert_has_calls(expected_calls)

            circum_hc_sr04.hc_sr04.tracking_info["objects"] == expected_targets


def test__update_thread_gettargets_returns_target_multiple():
    echo = MagicMock()

    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        import circum_hc_sr04
        from circum_hc_sr04.hc_sr04 import _update_thread

        with patch("circum_hc_sr04.hc_sr04.tracking_semaphore") as tracking_semaphore:

            echo.attach_mock(tracking_semaphore, 'tracking_semaphore')

            # run the loop once, then except out
            echo.read = MagicMock()
            echo.read.side_effect = [200, 201, EndLoopException]

            expected_calls = [
                # _get_targets
                call.read('cm', 0),
                # _update_thread
                call.tracking_semaphore.acquire(),
                call.tracking_semaphore.release(),
                # _get_targets
                call.read('cm', 0),
                # _update_thread
                call.tracking_semaphore.acquire(),
                call.tracking_semaphore.release(),
                # _get_targets
                call.read('cm', 0),
            ]

            expected_targets = [
                {
                    "x": 0,
                    "y": 0,
                    "z": 2.01
                }
            ]

            assert not circum_hc_sr04.hc_sr04.updated

            with pytest.raises(EndLoopException):
                _update_thread(echo, 0, 250)

            assert circum_hc_sr04.hc_sr04.updated

            circum_hc_sr04.hc_sr04.updated = False

            echo.assert_has_calls(expected_calls)

            circum_hc_sr04.hc_sr04.tracking_info["objects"] == expected_targets


def test_run_walabot_updated_false():
    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        import circum_hc_sr04
        from circum_hc_sr04.hc_sr04 import run_hc_sr04

        with patch("circum_hc_sr04.hc_sr04.tracking_semaphore") as tracking_semaphore:
            expected_calls = [
                call.acquire(),
                call.release(),
            ]

            assert not circum_hc_sr04.hc_sr04.updated
            assert run_hc_sr04(None) is None

            tracking_semaphore.assert_has_calls(expected_calls)


def test_run_walabot_updated_true():
    with patch.dict('sys.modules', {'RPi.GPIO': MagicMock()}):
        import circum_hc_sr04
        from circum_hc_sr04.hc_sr04 import run_hc_sr04

        with patch("circum_hc_sr04.hc_sr04.tracking_semaphore") as tracking_semaphore:
            expected_calls = [
                call.acquire(),
                call.release(),
            ]

            circum_hc_sr04.hc_sr04.updated = True
            circum_hc_sr04.hc_sr04.tracking_info = [0, 1, 2]
            ret = run_hc_sr04(None)
            assert ret is not None
            assert ret == circum_hc_sr04.hc_sr04.tracking_info
            assert ret is not circum_hc_sr04.hc_sr04.tracking_info

            tracking_semaphore.assert_has_calls(expected_calls)

            circum_hc_sr04.hc_sr04.update = False
