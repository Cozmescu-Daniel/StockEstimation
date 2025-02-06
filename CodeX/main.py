import customtkinter as ctk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import statsmodels.api as sm
import tkinter as tk

# List of sample stock symbols for demonstration (this can be replaced by actual data or API)
sample_stock_list = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'META', 'NFLX', 'NVDA', 'SPY', 'BA']

# Global variable to store the time period for stock data
time_period = "1d"  # Default to 1 day for 24H

def fetch_stock_data():
    stock_symbol = stock_combobox.get().upper()
    if not stock_symbol:
        error_label.configure(text="Please enter a stock symbol")
        return

    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period=time_period)
        if hist.empty:
            error_label.configure(text="Invalid stock symbol or no data available")
            return

        # Handle missing 'Adj Close' data gracefully
        adj_close_price = hist.get('Adj Close', None)
        if adj_close_price is None:
            adj_close_price = hist['Close']  # Use 'Close' as a fallback

        # Display Minimum and Maximum values
        min_price = hist['Close'].min()
        max_price = hist['Close'].max()
        min_date = hist['Close'].idxmin()
        max_date = hist['Close'].idxmax()

        min_label.configure(text=f"Minimum: {min_price:.2f} USD (on {min_date.date()})")
        max_label.configure(text=f"Maximum: {max_price:.2f} USD (on {max_date.date()})")

        # Additional stock details (added in the same way as min/max)
        opening_price = hist['Open'].iloc[0]
        closing_price = hist['Close'].iloc[-1]
        total_volume = hist['Volume'].sum()

        stock_details_label.configure(text=f"Opening Price: {opening_price:.2f} USD\n"
                                          f"Closing Price: {closing_price:.2f} USD\n"
                                          f"Adjusted Close: {adj_close_price.iloc[-1]:.2f} USD\n"
                                          f"Volume: {total_volume}")

        plot_forecast(hist, stock_symbol)
    except Exception as e:
        error_label.configure(text=f"Failed to fetch data: {e}")


def plot_forecast(hist, stock_symbol):
    hist['Date'] = hist.index
    hist['Days'] = np.arange(len(hist))

    # Ensure date-time values are naive (no time zone info)
    hist['Date'] = hist['Date'].dt.tz_localize(None)

    X = sm.add_constant(hist['Days'])
    model = sm.OLS(hist['Close'], X).fit()

    future_days = np.arange(len(hist), len(hist) + 7)
    future_X = sm.add_constant(future_days)
    forecast = model.predict(future_X)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(hist['Date'], hist['Close'], label="Actual Price", marker='o')
    future_dates = pd.date_range(start=hist['Date'].iloc[-1], periods=8)[1:]
    ax.plot(future_dates, forecast, label="Forecasted Price", linestyle='dashed', marker='x', color='red')
    ax.set_title(f"Stock Price Forecast for {stock_symbol}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()

    # Function to display date and price on click
    def on_click(event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Convert the x-data back to the nearest date in the DataFrame
            clicked_date = pd.to_datetime(x).normalize()  # Normalize to remove any time info
            nearest_idx = np.argmin(np.abs(hist['Date'] - clicked_date))  # Find the nearest date index
            date_clicked = hist['Date'].iloc[nearest_idx]
            price_clicked = hist['Close'].iloc[nearest_idx]
            stock_details_label.configure(text=f"Selected Date: {date_clicked.date()}\n"
                                              f"Price: {price_clicked:.2f} USD\n"
                                              f"Opening Price: {hist['Open'].iloc[nearest_idx]:.2f} USD\n"
                                              f"Closing Price: {hist['Close'].iloc[nearest_idx]:.2f} USD\n"
                                              f"Volume: {hist['Volume'].iloc[nearest_idx]}")

    # Connect the events
    fig.canvas.mpl_connect('button_press_event', on_click)

    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create a canvas with the initial figure
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    # Function to resize the graph when the window is resized
    def on_resize(event):
        new_width = event.width
        new_height = event.height
        fig.set_size_inches(new_width / 100, new_height / 100)  # Adjusting the figure size dynamically
        canvas.draw()

    # Bind the resizing event to the function
    graph_frame.bind("<Configure>", on_resize)


def set_time_period(period):
    global time_period
    time_period = period
    fetch_stock_data()

# Close the app gracefully when the X button is clicked
def on_closing():
    root.quit()  # Cleanly close the app

# Initialize customtkinter root window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Stock Forecasting Tool")
root.geometry("700x600")

# Bind window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Top Frame
top_frame = ctk.CTkFrame(root)
top_frame.pack(pady=10)

# Use customtkinter label
ctk.CTkLabel(top_frame, text="Enter Stock Symbol:").pack(side=ctk.LEFT, padx=5)

# Create a searchable combo box for stock symbols
stock_combobox = ctk.CTkComboBox(top_frame, values=sample_stock_list, width=200)
stock_combobox.pack(side=ctk.LEFT, padx=5)

# Use customtkinter button
ctk.CTkButton(top_frame, text="Get Forecast", command=fetch_stock_data).pack(side=ctk.LEFT, padx=5)

# Error label to display errors
error_label = ctk.CTkLabel(root, text="", text_color="red")
error_label.pack(pady=5)

# Frame for time period selection (with checkboxes)
period_frame = ctk.CTkFrame(root)
period_frame.pack(pady=10)

# Variables to hold the selected time period
time_period_var = ctk.StringVar(value="1d")  # Default value

# Checkboxes for time period selection
ctk.CTkRadioButton(period_frame, text="1W", variable=time_period_var, value="1wk", command=lambda: set_time_period("1wk")).pack(side=ctk.LEFT, padx=5)
ctk.CTkRadioButton(period_frame, text="6M", variable=time_period_var, value="6mo", command=lambda: set_time_period("6mo")).pack(side=ctk.LEFT, padx=5)
ctk.CTkRadioButton(period_frame, text="1Y", variable=time_period_var, value="1y", command=lambda: set_time_period("1y")).pack(side=ctk.LEFT, padx=5)
ctk.CTkRadioButton(period_frame, text="5Y", variable=time_period_var, value="5y", command=lambda: set_time_period("5y")).pack(side=ctk.LEFT, padx=5)

# Minimum and Maximum Labels
min_label = ctk.CTkLabel(root, text="Minimum: ")
min_label.pack(pady=5)

max_label = ctk.CTkLabel(root, text="Maximum: ")
max_label.pack(pady=5)

# Stock details label
stock_details_label = ctk.CTkLabel(root, text="Stock Details: ")
stock_details_label.pack(pady=10)

# Graph Frame
graph_frame = ctk.CTkFrame(root)
graph_frame.pack(fill=ctk.BOTH, expand=True)

root.mainloop()
