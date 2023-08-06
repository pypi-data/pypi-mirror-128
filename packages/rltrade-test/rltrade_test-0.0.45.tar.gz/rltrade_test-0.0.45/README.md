# rl-trade

## On colab 
1. Smart Portfolio Stock Trading with filter and Backtesting: [notebook](https://colab.research.google.com/drive/1hNxH9j-VwfyK6PHrK4JOAE4VKZUThFbO)
## On Local Machine (Os: ubuntu-linux)

### Python 3.7.11 or greater is required
    conda create -n env_name python=3.7
    conda activate env_name

### pip install for testing.
    pip install rltrade-test

### Login into your Interactive Borker app (live or paper)
    1. For training the model run train.py from examples folder.
    2. For trading use trade.py from examples folder.
 
#### Import
```python
from rltrade import config
from rltrade.models import SmartDRLAgent
from rltrade.data import IBKRDownloader
from rltrade.backtests import backtest_plot,backtest_stats
```
#### Parameters
```python
train_period = ('2018-01-01','2019-01-01') #for training the model
test_period = ('2019-01-01','2021-01-01') #for trading and backtesting

ticker_list = config.DOW_30_TICKER[:5]
tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
additional_indicators = config.ADDITIONAL_STOCK_INDICATORS

env_kwargs = {
    "initial_amount": 100000, 
    "ticker_col_name":"tic",
    "filter_threshold":1, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset','cagr','sortino'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "tech_indicator_list":tech_indicators + additional_indicators, 
    "reward_scaling": 1}

PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.0001,
            'batch_size':151}

```
#### Download Data and set up agent
df = IBKRDownloader(start_date = train_period[0], # first date
                    end_date = test_period[1], #last date
                    ticker_list = ticker_list).fetch_data() #requires subscription

```python
agent = SmartDRLAgent("ppo",
                    df=df,
                    ticker_list=ticker_list,
                    add_ticker_list=add_ticker_list,
                    ticker_col_name="tic",
                    tech_indicators=tech_indicators,
                    additional_indicators=additional_indicators,
                    train_period=train_period,
                    test_period=test_period,
                    env_kwargs=env_kwargs,
                    model_kwargs=PPO_PARAMS,
                    tb_log_name='ppo',
                    total_timesteps=500)

```
#### Training model and trading

```python
agent.train_model_filter() #training model on trading period
agent.save_model('models/dow5') #save the model for trading

df_daily_return,df_actions = agent.make_prediction() #testing model on testing period

```
#### Backtesting using pyfolio

```python
perf_stats_all = backtest_stats(df=df_daily_return,
                                baseline_ticker=["^DJI"],
                                value_col_name="daily_return",
                                baseline_start = test_period[0], 
                                baseline_end = test_period[1])

print(perf_stats_all)

backtest_plot(account_value=df_daily_return,
            baseline_ticker=["^DJI"],
            value_col_name="daily_return",
            baseline_start = test_period[0], 
            baseline_end = test_period[1])

```

