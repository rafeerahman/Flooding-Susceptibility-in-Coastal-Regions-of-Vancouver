"""
Modelling the data with graphs and a map
which shows the susceptible flooding regions - includes interactive features

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
from typing import List, Tuple, Dict
import csv

import python_ta
from python_ta import contracts

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# New imports 12/13/2020, commented ones are not needed to run
# import math
# import matplotlib.pylab as plt
# from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings("ignore")


################
# DISPLAY GRAPHS
################
def display_graph(data: Dict[str, List[Tuple]]) -> go.Figure():
    """Return a graph of the sea level change over the years.
    NOT a predictive model
    """
    years = []
    levels = []
    for row in data:
        years.append([pair[0] for pair in data[row]])
        levels.append([pair[1] for pair in data[row]])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years[0], y=levels[0], name='TOPEX'))
    fig.add_trace(go.Scatter(x=years[1], y=levels[1], name='Jason-1'))
    fig.add_trace(go.Scatter(x=years[2], y=levels[2], name='Jason-2'))
    fig.add_trace(go.Scatter(x=years[3], y=levels[3], name='Jason-3'))

    fig.update_layout(title='Sea Level Anomaly in the North Pacific Ocean from (1992 - 2020)',
                      xaxis_title='Year',
                      yaxis_title='Change in Sea Level (mm)',
                      template='plotly_dark')

    return fig


def display_annual_mean(data: str) -> go.Figure():
    """Return a graph of the sea level change over the years.
    Can work with the prediction model
    """
    df = pd.read_csv(data)

    fig = px.scatter(df, x=df['year'], y=df['mean_sea_level'], trendline="ols")

    fig.update_layout(title='Mean Sea Level Anomaly in the North Pacific Ocean from (1992 - 2300)',
                      xaxis_title='Year',
                      yaxis_title='Average Change in Sea Level (mm)',
                      template='plotly_dark')

    return fig


#############
# SARIMAX Model
#############
def predicted_sea_level(file: str) -> go.Figure():
    """ Uses training and testing data as well as the SARIMAX import
        to predict the future sea level anomoly.
    """
    # plt.style.use('dark_background')
    df = pd.read_csv(file)
    df.columns = ["Month", "Sea_Level"]
    df['Month'] = pd.to_datetime(df['Month'])

    # Taking only the max value each month per year to condense the data a bit.
    new_df = df.groupby(df['Month'].dt.to_period('M'), as_index=False).max()
    new_df['Month'] = pd.to_datetime(new_df['Month'])
    new_df.set_index("Month", inplace=True)

    # print(new_df.to_string())
    # new_df.plot()

    # Dickey-fuller test
    # print(adfuller(df))
    # Since data is not stationary, we need SARIMAX (Seasonal)

    # decomposed = seasonal_decompose(new_df['Sea_Level'], model='additive')

    # Plotting the trend, seasonal, and residual data
    # trend = decomposed.trend
    # seasonal = decomposed.seasonal
    # residual = decomposed.resid

    # plt.figure(figsize=(12,8))
    # plt.subplot(411)
    # plt.plot(new_df, label='Original', color='yellow')
    # plt.legend(loc='upper left')
    # plt.subplot(412)
    # plt.plot(trend, label='Trend', color='yellow')
    # plt.legend(loc='upper left')
    # plt.subplot(413)
    # plt.plot(seasonal, label='Seasonal', color='yellow')
    # plt.legend(loc='upper left')
    # plt.subplot(414)
    # plt.plot(residual, label='Residual', color='yellow')
    # plt.legend(loc='upper left')
    # plt.show()

    # A simulation to provide the P, Q, and D values with the lowest AIC
    # arima_model = auto_arima(new_df['Sea_Level'], start_p=1, d=1, start_q=1,
    #                          max_p=5, max_q=5, max_d=5, m=12,
    #                          start_P=0, D=1, start_Q=0, max_P=5, max_D=5, max_Q=5,
    #                          seasonal=True,
    #                          trace=True,
    #                          error_action='ignore',
    #                          surpress_warning=True,
    #                          stepwise=True, n_fits=3)
    # print(arima_model.summary())

    # Splitting data into train and test data. Then do the forecasting.
    # We can't randomly sample, because values have meaning to it, so
    # Take 85% from the BEGINNING of the data, and assign it training, while the remaining is for testing.

    size = int(len(new_df) * 0.85)
    X_train, X_test = new_df[0:size], new_df[size:len(new_df)]

    # Fitting a SARIMAX model
    model = SARIMAX(X_train['Sea_Level'],
                    order=(1, 1, 0),
                    seasonal_order=(3, 1, 0, 12))

    result = model.fit(disp=False)
    # print(result.summary())

    # Now this model is ready for forecasting
    # Train prediction
    start_index = 0
    end_index = len(X_train) - 1
    # Basically the data moves i+1 index.
    train_prediction = result.predict(start_index, end_index)
    # print(X_train.tail())
    # print(train_prediction.tail())

    # Prediction, from the end of our training data to the end of our actual data.
    start_index = len(X_train)
    end_index = len(new_df) - 1
    prediction = result.predict(start_index, end_index).rename('Predicted sea level')

    # Comparing the prediction to the actual/test values and seeing how accurate it is.
    # plot predictions and actual values
    # prediction.plot(legend=True)
    # X_test['Sea_Level'].plot(legend=True)

    # Root mean squared error, to see how much error there is.
    # rmse_train = math.sqrt(mean_squared_error(X_train, train_prediction))
    # print(rmse_train)
    # rmse_test = math.sqrt(mean_squared_error(X_test, prediction))
    # print(rmse_test)

    # Our forecast for the next 20 years (What we want).
    forecast = result.predict(start=len(new_df),
                              end=(len(new_df) - 1) + 30 * 12,
                              typ='levels').rename('Forecast')

    forecast_df = forecast.to_frame('Sea_Level')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_train.index.tolist(), y=X_train['Sea_Level'].tolist(),
                             name='Training'))
    fig.add_trace(go.Scatter(x=X_test.index.to_list(),
                             y=X_test['Sea_Level'].tolist(),
                             name='Test/Actual'))
    fig.add_trace(go.Scatter(x=forecast.index.tolist(), y=forecast_df['Sea_Level'].tolist(),
                             name='Forecast'))

    fig.update_layout(title='SARIMAX Model Sea Level Forecast Next 30 Years',
                      xaxis_title='Year',
                      yaxis_title='Change in Sea Level (mm)',
                      template='plotly_dark')
    return fig


#############
# DISPLAY MAPS
#############
def display_map() -> go.Figure():
    """Displays the map of the given data
    """
    # Main point - Vancouver latitude and longitude
    fig = px.scatter_mapbox(lat=[49.2500], lon=[-123.1000],
                            color_discrete_sequence=['fuchsia'], zoom=3, height=750)

    # add points that are at risk of flooding
    df = pd.read_csv('below_sea_level.csv')

    fig.add_trace(
        px.scatter_mapbox(
            df,
            title='Map of Vancouver Indicating Flood Regions',
            lat='lat',
            lon='long',
            color="elevation",
            color_discrete_sequence=['blue'],
            opacity=0.1,
            zoom=3
        ).data[0]
    )

    # set map style
    fig.update_layout(mapbox_style='open-street-map',
                      template='plotly_dark',
                      mapbox={'center': go.layout.mapbox.Center(lat=mean_coords()[0],
                                                                lon=mean_coords()[1]), 'zoom': 10})
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.update_coloraxes(colorscale='RdBu')

    return fig


def mean_coords() -> Tuple[float, float]:
    """
    Returns the average latitude and longitude of points contained in below_sea_level.csv
    """
    lat_total = 0
    long_total = 0
    cnt = 0
    with open('below_sea_level.csv') as file:
        reader = csv.reader(file)

        # skip header
        next(reader)

        # accumulate each row
        for row in reader:
            lat_total += float(row[0])
            long_total += float(row[1])
            cnt += 1

    # return the average
    return (lat_total / cnt, long_total / cnt)


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['numpy', 'plotly.express',
                          'plotly.graph_objects', 'pandas'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
