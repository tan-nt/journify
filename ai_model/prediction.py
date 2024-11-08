import logging
from streamlit_float import *
import streamlit as st
from database.article import article_model
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
import numpy as np

logger = logging.getLogger()

def display_prediction():
    st.session_state.page = "ai-exploration"
    data = article_model.read_articles()  # Load data into a DataFrame
    df = pd.DataFrame(data)
    
    if 'update_date' in df.columns:
        try:
            # Ensure update_date column is in datetime format
            df['update_date'] = pd.to_datetime(df['update_date'], errors='coerce')
            df = df.dropna(subset=['update_date'])  # Drop rows where conversion failed
            df['year'] = df['update_date'].dt.year
            df['month'] = df['update_date'].dt.month

            # Aggregate data by year and month
            month_counts = df.groupby(['year', 'month']).size().reset_index(name='count')
            month_counts['date'] = pd.to_datetime(month_counts[['year', 'month']].assign(day=1))  # First day of each month

            # Prepare data for regression models
            X = np.array(range(len(month_counts))).reshape(-1, 1)  # Sequential months as independent variable
            y = month_counts['count'].values  # Number of articles as dependent variable

            # Fit Linear Regression model
            lr_model = LinearRegression()
            lr_model.fit(X, y)

            # Fit Support Vector Regressor
            svr_model = SVR(kernel='rbf', C=100, gamma=0.1)
            svr_model.fit(X, y)

            # Fit Random Forest Regressor
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X, y)

            # Fit Naive Bayes (as a workaround, use classification approach)
            nb_model = GaussianNB()
            nb_model.fit(X, np.clip(y, a_min=0, a_max=None))  # Ensure non-negative values for classification

            # Extend for future months (e.g., next 24 months for a 2-year forecast)
            future_X = np.arange(len(X), len(X) + 24).reshape(-1, 1)  # Predicting for the next 24 months
            
            # Forecast using each model and clip negative predictions to zero
            lr_forecast = np.clip(lr_model.predict(future_X), a_min=0, a_max=None)
            svr_forecast = np.clip(svr_model.predict(future_X), a_min=0, a_max=None)
            rf_forecast = np.clip(rf_model.predict(future_X), a_min=0, a_max=None)
            nb_forecast = np.clip(nb_model.predict(future_X), a_min=0, a_max=None)

            # Create dates for the future months
            last_date = month_counts['date'].max()
            future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=24, freq='MS')
            future_df = pd.DataFrame({
                'date': future_dates,
                'Linear Regression': lr_forecast,
                'SVR': svr_forecast,
                'Random Forest': rf_forecast,
                'Naive Bayes': nb_forecast
            })

            # Plot historical data as a solid line
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=month_counts['date'], y=month_counts['count'],
                                      mode='lines', name='Historical Data'))

            # Plot predictions from each model as a red dotted line
            fig3.add_trace(go.Scatter(x=future_df['date'], y=future_df['Linear Regression'],
                                      mode='lines', name='Forecast (Linear Regression)',
                                      line=dict(color='blue', dash='dot')))
            fig3.add_trace(go.Scatter(x=future_df['date'], y=future_df['SVR'],
                                      mode='lines', name='Forecast (SVR)',
                                      line=dict(color='green', dash='dot')))
            fig3.add_trace(go.Scatter(x=future_df['date'], y=future_df['Random Forest'],
                                      mode='lines', name='Forecast (Random Forest)',
                                      line=dict(color='orange', dash='dot')))
            fig3.add_trace(go.Scatter(x=future_df['date'], y=future_df['Naive Bayes'],
                                      mode='lines', name='Forecast (Naive Bayes)',
                                      line=dict(color='red', dash='dot')))

            # Layout adjustments
            fig3.update_layout(
                title="Historical and Forecasted Publication Trends by Month (2-Year Forecast)",
                xaxis_title="Date",
                yaxis_title="Number of Articles",
                showlegend=True
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error processing date column: {e}")
    else:
        st.warning("The 'update_date' column is not available in the dataset.")
        
    display_comment_prediction()
    display_login_prediction()

def display_comment_prediction():
    # Step 1: Generate simulated comment data per month
    np.random.seed(42)
    months = pd.date_range(start="2018-01-01", end="2023-12-01", freq='MS')
    comment_counts = np.random.poisson(lam=20, size=len(months))  # Randomly generate comments per month

    # Create DataFrame for comment data
    comment_df = pd.DataFrame({'date': months, 'comment_count': comment_counts})

    # Prepare data for models
    X = np.array(range(len(comment_df))).reshape(-1, 1)  # Sequential months as independent variable
    y = comment_df['comment_count'].values  # Monthly comment counts as dependent variable

    # Fit Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)

    # Fit Support Vector Regressor
    svr_model = SVR(kernel='rbf', C=100, gamma=0.1)
    svr_model.fit(X, y)

    # Fit Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Fit Naive Bayes (GaussianNB)
    nb_model = GaussianNB()
    nb_model.fit(X, np.clip(y, a_min=0, a_max=None))  # Clip y to non-negative for Naive Bayes

    # Extend for future months (e.g., next 24 months for a 2-year forecast)
    future_X = np.arange(len(X), len(X) + 24).reshape(-1, 1)  # Predicting for the next 24 months

    # Forecast using each model and clip negative predictions to zero
    lr_forecast = np.clip(lr_model.predict(future_X), a_min=0, a_max=None)
    svr_forecast = np.clip(svr_model.predict(future_X), a_min=0, a_max=None)
    rf_forecast = np.clip(rf_model.predict(future_X), a_min=0, a_max=None)
    nb_forecast = np.clip(nb_model.predict(future_X), a_min=0, a_max=None)

    # Create dates for the future months
    last_date = comment_df['date'].max()
    future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=24, freq='MS')
    future_df = pd.DataFrame({
        'date': future_dates,
        'Linear Regression': lr_forecast,
        'SVR': svr_forecast,
        'Random Forest': rf_forecast,
        'Naive Bayes': nb_forecast
    })

    # Plot historical data as a solid line
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=comment_df['date'], y=comment_df['comment_count'],
                             mode='lines', name='Historical Comment Data'))

    # Plot predictions from each model as dotted lines in different colors
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Linear Regression'],
                             mode='lines', name='Forecast (Linear Regression)',
                             line=dict(color='blue', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['SVR'],
                             mode='lines', name='Forecast (SVR)',
                             line=dict(color='green', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Random Forest'],
                             mode='lines', name='Forecast (Random Forest)',
                             line=dict(color='orange', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Naive Bayes'],
                             mode='lines', name='Forecast (Naive Bayes)',
                             line=dict(color='red', dash='dot')))

    # Layout adjustments
    fig.update_layout(
        title="Historical and Forecasted Comment Trends by Month (2-Year Forecast)",
        xaxis_title="Date",
        yaxis_title="Number of Comments",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_login_prediction():
    # Step 1: Generate simulated daily login data
    np.random.seed(42)
    days = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
    login_counts = np.random.randint(2, 16, size=len(days))  # Generate between 2-15 logins per day

    # Create DataFrame for daily login data
    login_df = pd.DataFrame({'date': days, 'login_count': login_counts})

    # Prepare data for models
    X = np.array(range(len(login_df))).reshape(-1, 1)  # Sequential days as independent variable
    y = login_df['login_count'].values  # Daily login counts as dependent variable

    # Fit Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)

    # Fit Support Vector Regressor
    svr_model = SVR(kernel='rbf', C=100, gamma=0.1)
    svr_model.fit(X, y)

    # Fit Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Fit Naive Bayes (GaussianNB)
    nb_model = GaussianNB()
    nb_model.fit(X, np.clip(y, a_min=0, a_max=None))  # Clip y to non-negative for Naive Bayes

    # Extend for future days (e.g., next 30 days for a 1-month forecast)
    future_X = np.arange(len(X), len(X) + 30).reshape(-1, 1)  # Predicting for the next 30 days

    # Forecast using each model and clip negative predictions to zero
    lr_forecast = np.clip(lr_model.predict(future_X), a_min=0, a_max=None)
    svr_forecast = np.clip(svr_model.predict(future_X), a_min=0, a_max=None)
    rf_forecast = np.clip(rf_model.predict(future_X), a_min=0, a_max=None)
    nb_forecast = np.clip(nb_model.predict(future_X), a_min=0, a_max=None)

    # Create dates for the future days
    last_date = login_df['date'].max()
    future_dates = pd.date_range(last_date + pd.DateOffset(days=1), periods=30, freq='D')
    future_df = pd.DataFrame({
        'date': future_dates,
        'Linear Regression': lr_forecast,
        'SVR': svr_forecast,
        'Random Forest': rf_forecast,
        'Naive Bayes': nb_forecast
    })

    # Plot historical data as a solid line
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=login_df['date'], y=login_df['login_count'],
                             mode='lines', name='Historical Login Data'))

    # Plot predictions from each model as dotted lines in different colors
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Linear Regression'],
                             mode='lines', name='Forecast (Linear Regression)',
                             line=dict(color='blue', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['SVR'],
                             mode='lines', name='Forecast (SVR)',
                             line=dict(color='green', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Random Forest'],
                             mode='lines', name='Forecast (Random Forest)',
                             line=dict(color='orange', dash='dot')))
    fig.add_trace(go.Scatter(x=future_df['date'], y=future_df['Naive Bayes'],
                             mode='lines', name='Forecast (Naive Bayes)',
                             line=dict(color='red', dash='dot')))

    # Layout adjustments
    fig.update_layout(
        title="Historical and Forecasted Daily Login Trends (1-Month Forecast)",
        xaxis_title="Date",
        yaxis_title="Number of Daily Logins",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
