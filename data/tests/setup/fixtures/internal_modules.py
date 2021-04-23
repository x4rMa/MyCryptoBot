import os

import pytest

import data
from data.sources.binance import BinanceDataHandler
from data.tests.setup.fixtures.external_modules import double_callback
from data.tests.setup.test_data.sample_data import mock_websocket_raw_data_5m, mock_websocket_raw_data_1h

MODEL_APP_URL = 'https://example.com'
EXECUTION_APP_URL = 'https://example.com'


@pytest.fixture()
def mock_settings_env_vars(mocker):
    mocker.patch.dict(os.environ, {
        "MODEL_APP_URL": MODEL_APP_URL,
        "EXECUTION_APP_URL": EXECUTION_APP_URL,
    })


@pytest.fixture
def mock_trigger_signal_successfully(mocker):
    return mocker.patch.object(
        data.sources.binance._binance,
        'trigger_signal',
        lambda symbol, strategy, params, candle_size, exchange: True,
    )


@pytest.fixture
def mock_trigger_signal_fail(mocker):
    mocker.patch.object(
        data.sources.binance._binance,
        'trigger_signal',
        lambda symbol, strategy, params, candle_size, exchange: False,
    )


@pytest.fixture
def trigger_signal_spy(mocker):
    return mocker.spy(data.sources.binance._binance, 'trigger_signal')


def mock_start_multiplex_socket(self, streams, callback):
    double_callback(callback, mock_websocket_raw_data_5m)
    double_callback(callback, mock_websocket_raw_data_1h)

    return f"streams={'/'.join(streams)}"


@pytest.fixture
def mock_binance_handler_websocket(mocker):
    mocker.patch.object(BinanceDataHandler, "start_multiplex_socket", mock_start_multiplex_socket)


@pytest.fixture
def mock_binance_websocket_start(mocker):
    mocker.patch.object(BinanceDataHandler, "start", lambda self: None)


@pytest.fixture
def mock_binance_handler_start_data_ingestion(mocker):
    mocker.patch.object(
        BinanceDataHandler,
        "start_data_ingestion",
        lambda self: None
    )


@pytest.fixture
def mock_binance_handler_stop_data_ingestion(mocker):
    return mocker.patch.object(
        BinanceDataHandler,
        "stop_data_ingestion",
        lambda self: None
    )


@pytest.fixture
def binance_handler_stop_data_ingestion_spy(mocker):
    return mocker.spy(BinanceDataHandler, 'stop_data_ingestion')


@pytest.fixture
def binance_handler_instances_spy_start_bot(mocker):
    return mocker.patch('data.service.app.binance_instances', new_callable=list)


def immediate_execution(initialize_data_collection, strategy, params, symbol, candle_size):
    return initialize_data_collection(strategy, params, symbol, candle_size)


@pytest.fixture
def mock_executor_submit(mocker):
    mocker.patch.object(
        data.service.app.executor,
        "submit",
        immediate_execution
    )


@pytest.fixture
def binance_handler_instances_spy_stop_bot(db, create_symbol, create_assets, create_exchange, mocker):
    return mocker.patch(
        'data.service.app.binance_instances',
        [BinanceDataHandler("MovingAverageCrossover", symbol='BTCUSDT')]
    )


@pytest.fixture
def binance_handler_instances_spy(mocker):
    return mocker.spy(data.service.app, 'binance_instances')


@pytest.fixture
def mock_start_stop_symbol_trading_success_true(mocker):
    mocker.patch.object(
        data.service.app,
        'start_stop_symbol_trading',
        lambda symbol, exchange, start_or_stop: {"success": True, "response": ''},
    )


@pytest.fixture
def mock_start_stop_symbol_trading_success_false(mocker):
    return mocker.patch.object(
        data.service.app,
        'start_stop_symbol_trading',
        lambda symbol, exchange, start_or_stop: {"success": False, "response": 'Failed'},
    )


@pytest.fixture
def mock_check_job_status_response(mocker):
    return mocker.patch(
        'data.sources._sources.check_job_status',
    )


@pytest.fixture
def mock_generate_signal(mocker):
    return mocker.patch(
        'data.sources._sources.generate_signal',
    )


@pytest.fixture
def mock_wait_for_job_conclusion(mocker):
    return mocker.patch(
        'data.sources._sources.wait_for_job_conclusion',
    )