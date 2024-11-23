import numpy as np
# Temporary fix for the deprecation of np.float
np.float = float

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Register converters to handle datetime objects
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data by removing the top and bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    """
    Draws a line plot of daily page views.
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the data
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    
    # Set titles and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Adjust layout for better spacing
    fig.tight_layout()
    
    # Save the figure
    fig.savefig('line_plot.png')
    
    return fig

def draw_bar_plot():
    """
    Draws a bar plot showing average page views per month for each year.
    """
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Create a figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot the bar chart
    df_bar_grouped.plot(kind='bar', ax=ax)
    
    # Set legend with month names
    ax.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    
    # Set titles and labels
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views per Month')
    
    # Adjust layout
    fig.tight_layout()
    
    # Save the figure
    fig.savefig('bar_plot.png')
    
    return fig

def draw_box_plot():
    """
    Draws box plots showing distribution of page views by year and month.
    """
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')
    
    # Explicitly cast to float to avoid issues with deprecated np.float
    df_box['value'] = df_box['value'].astype(float)
    
    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Year-wise box plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise box plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Adjust layout
    fig.tight_layout()
    
    # Save the figure
    fig.savefig('box_plot.png')
    
    return fig