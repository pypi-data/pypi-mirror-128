#!/usr/bin/env python

"""Tests for `alpyen` package."""

import pytest
import statistics

from click.testing import CliRunner

from alpyen import datacontainer
from alpyen import backtesting
from alpyen import cli
from alpyen import strategy


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'alpyen.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_backtesting_macrossing():
    # Read data
    data_folder_path = 'Data\\'
    ticker_name = 'BBH'
    short_lookback = 5
    long_lookback = 200
    short_lookback_name = ticker_name + '_MA_' + str(short_lookback)
    long_lookback_name = ticker_name + '_MA_' + str(long_lookback)
    ticker_names = [ticker_name]
    all_input = datacontainer.DataUtils.aggregate_yahoo_data(ticker_names, data_folder_path)

    # Subscribe to signals
    signal_info_dict = {}
    signal_info_dict[short_lookback_name]\
        = backtesting.SignalInfo('MA', ticker_names, [short_lookback])
    signal_info_dict[long_lookback_name]\
        = backtesting.SignalInfo('MA', ticker_names, [long_lookback])

    # Subscribe to strategies
    strategy_info_dict = {}
    strategy_name = ticker_name + '_MACrossing_01'
    strategy_info_dict[strategy_name] = backtesting.StrategyInfo(
        'MACrossing',
        [short_lookback_name, long_lookback_name],
        1, {}, ticker_names, {'combo1': [1.0]})

    # Create backtester
    number_path = 1000
    my_backtester = backtesting.Backtester(all_input, ticker_names, signal_info_dict, strategy_info_dict,
                                           number_path)
    my_backtester.run_backtest()
    backtest_results = my_backtester.get_results()

    # Check
    # Actual historical path
    assert backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)][0]\
           == pytest.approx(0.09503, 0.0001)
    assert backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)][0]\
           == pytest.approx(0.11913, 0.0001)
    assert backtest_results[strategy_name][str(backtesting.MetricType.Return)][0]\
           == pytest.approx(0.74978, 0.0001)
    # All (including simulated) paths
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)])\
           == pytest.approx(0.105, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)])\
           == pytest.approx(0.0308, 0.05)
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)])\
           == pytest.approx(0.152, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)])\
           == pytest.approx(0.0611, 0.05)
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.Return)])\
           == pytest.approx(0.865, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.Return)])\
           == pytest.approx(0.326, 0.05)


def test_backtesting_vaa():
    # Read data
    data_folder_path = 'Data\\'
    ticker_names = ['VOO', 'VWO', 'VEA', 'BND', 'SHY', 'IEF', 'LQD']
    all_input = datacontainer.DataUtils.aggregate_yahoo_data(ticker_names, data_folder_path)

    # Subscribe to signals
    signal_info_dict = {}
    lookback = 253
    for ticker in ticker_names:
        signal_info_dict[ticker + '_WM_1'] = backtesting.SignalInfo('WM', [ticker], [lookback])

    # Subscribe to strategies
    strategy_info_dict = {}
    strategy_name = '4ETF_VAA_01'
    strategy_info_dict[strategy_name] = backtesting.StrategyInfo(
        'VAA', [ticker + '_WM_1' for ticker in ticker_names],
        1, {'risk_on_size': 4, 'num_assets_to_hold': 2,
            'breadth_protection_threshold': 1, 'weighting_scheme': strategy.WeightingScheme.Equal},
        ticker_names, {'combo1': [1.0] * len(ticker_names)})

    # Create backtester
    number_path = 1000
    my_backtester = backtesting.Backtester(all_input, ticker_names, signal_info_dict, strategy_info_dict,
                                           number_path)
    my_backtester.run_backtest()
    backtest_results = my_backtester.get_results()

    # Check
    # Actual historical path
    assert backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)][0]\
           == pytest.approx(0.08549, 0.0001)
    assert backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)][0]\
           == pytest.approx(0.08114, 0.0001)
    assert backtest_results[strategy_name][str(backtesting.MetricType.Return)][0]\
           == pytest.approx(1.01538, 0.0001)
    # All (including simulated) paths
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)])\
           == pytest.approx(0.03377, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.PoorMansSharpeRatio)])\
           == pytest.approx(0.01799, 0.05)
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)])\
           == pytest.approx(0.13297, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.MaximumDrawDown)])\
           == pytest.approx(0.047857, 0.05)
    assert statistics.mean(backtest_results[strategy_name][str(backtesting.MetricType.Return)])\
           == pytest.approx(0.3629, 0.05)
    assert statistics.stdev(backtest_results[strategy_name][str(backtesting.MetricType.Return)])\
           == pytest.approx(0.2243, 0.05)


from alpyen import brokerinterface
from alpyen import signal

from typing import List, Dict
from eventkit import Event


# Signal and Strategy for debugging live trading
class TempSignal(signal.SignalBase):
    _signal_signature = 'TS'

    def __init__(self,
                 signature_str: str,
                 input_data_array: List[Event],
                 warmup_length: int) -> None:
        self._signal_name = input_data_array[0].name() + "_TS_" + str(warmup_length)
        self._signal_event = Event(self._signal_name)

    def calculate_signal(self) -> int:
        prices = self.get_data_by_name(self._input_data_array[0].name())
        return round(prices[-1] / 0.00001, 0) % 10


class TempStrategy(strategy.StrategyBase):
    _strategy_signature = 'TempStrategy'

    def __init__(self,
                 signature_str: str,
                 input_signal_array: List[Event],
                 trade_combo: strategy.TradeCombos,
                 warmup_length: int,
                 initial_capital: float = 100.0,
                 order_manager: brokerinterface.OrderManagerBase = None) -> None:
        self._strategy_name = 'My temp strategy'

    def make_order_decision(self) -> Dict[str, float]:
        signal_name = next(iter(self._signal_storage))
        if self._signal_storage[signal_name][-1] >= 0 and self._signal_storage[signal_name][-1] < 2:
            return {'combo_1': 2.0}
        elif self._signal_storage[signal_name][-1] >= 2 and self._signal_storage[signal_name][-1] < 4:
            return {'combo_1': -2.0}
        elif self._signal_storage[signal_name][-1] >= 4 and self._signal_storage[signal_name][-1] < 6:
            return {'combo_2': 3.0}
        elif self._signal_storage[signal_name][-1] >= 6 and self._signal_storage[signal_name][-1] < 8:
            return {'combo_2': -3.0}
        else:
            return {'combo_3': 1.0}


def test_backtesting_live():
    ib_api = brokerinterface.IBBrokerAPI()
    ib_api.connect(port=4002)

    # Contracts
    input_data_names = ['EURUSD', 'GBPUSD', 'CHFUSD']
    contracts = [brokerinterface.IBBrokerAPI.IBBrokerContract(brokerinterface.ContractType.FX,
                                                              x) for x in input_data_names]

    # Broker relay
    bar_relays = [brokerinterface.IBBrokerAPI.IBBrokerEventRelay(x, 'close') for x in input_data_names]

    # Signals
    temp_signal = signal.SignalBase('TS', [bar_relays[0].get_event()], 2)

    temp_signal_dataslot = signal.DataSlot(input_data_names[0], [temp_signal])

    # Subscription
    live_bars1 = ib_api.request_live_bars(contracts[0], brokerinterface.PriceDataType.Mid)
    live_bars2 = ib_api.request_live_bars(contracts[1], brokerinterface.PriceDataType.Mid)
    live_bars3 = ib_api.request_live_bars(contracts[2], brokerinterface.PriceDataType.Mid)

    mtm_data = signal.DataSlot(input_data_names[0], [temp_signal])

    live_bars1.updateEvent += bar_relays[0].live_bar
    live_bars2.updateEvent += bar_relays[1].live_bar
    live_bars3.updateEvent += bar_relays[2].live_bar

    # Create strategy
    contract_events = [bar_relay.get_event() for bar_relay in bar_relays]

    trade_combos = strategy.TradeCombos(contract_events,
                                        {'combo_1': [-50.0, 100.0, 0.0],
                                         'combo_2': [-100.0, 0.0, -60.0],
                                         'combo_3': [0.0, -100.0, 70.0]})
    portfolio_manager = brokerinterface.IBPortfolioManager(ib_api)
    e_c_dict = dict(zip(input_data_names, contracts))
    order_manager = brokerinterface.IBOrderManager(ib_api, portfolio_manager, e_c_dict)

    temp_strategy = strategy.StrategyBase(
        'TempStrategy',
        [temp_signal.get_signal_event()],
        trade_combos, 1, order_manager=order_manager)

    ib_api.get_handle().sleep(500)
