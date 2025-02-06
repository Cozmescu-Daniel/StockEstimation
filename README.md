# Stock Forecasting Tool 📈

Welcome to the **Stock Forecasting Tool**! This project allows users to fetch stock data, visualize historical stock prices, and generate simple price forecasts using a linear regression model.

## Features ✨
- Fetch stock data for various companies using Yahoo Finance API.
- Visualize the stock's historical prices along with a simple forecast.
- Selectable time periods for fetching stock data (e.g., 1 week, 6 months, 1 year, 5 years).
- Dynamic resizing of charts based on the window size.
- Error handling for invalid stock symbols or missing data.

## Technologies Used 🛠️
- **Python** – The primary programming language.
- **CustomTkinter** – A modern and beautiful GUI framework built on Tkinter.
- **yfinance** – A popular library for accessing financial data from Yahoo Finance.
- **Matplotlib** – Used for plotting the historical stock prices and forecast.
- **Statsmodels** – Used for statistical modeling to generate stock price forecasts.

## Requirements 📋
To run this project locally, you will need to install the following Python libraries:
- `pip install customtkinter yfinance matplotlib statsmodels pandas numpy`

## How to Use the Tool 🖥️
Clone the repository:
- `git clone https://github.com/Cozmescu-Daniel/StockPrediction.git`

Navigate to the project directory:
- `cd StockPrediction`

Run the main.py script to launch the application:
- `python main.py`

The tool will display a GUI window where you can:
  
- Select a stock symbol (e.g., AAPL, MSFT).
- Choose the time period for which you want to fetch data (1W, 6M, 1Y, 5Y).
- View a graph with actual stock prices and predicted prices for the next 7 days.

## Example 🖼️
![image](https://github.com/user-attachments/assets/30160b56-afdf-47cd-a386-f79d169b8150)
The graph will show:

- The actual historical stock prices.
- A forecast of the stock's price for the next 7 days.

## How the Forecast Works 📊
The forecast is generated using a simple Linear Regression model:

- Historical stock data is used to create a linear regression model.
- The model then predicts future stock prices based on the historical trend.
- The next 7 days' forecasted prices are shown in red as dashed lines.

## Customization ✍️
- Add more stocks: The sample stock list can be customized to include more symbols. Update the sample_stock_list variable.
- Change forecast model: You can replace the linear regression model with a more advanced forecasting model if desired.
- Modify the time periods: You can add more time periods (e.g., 1 month) by updating the set_time_period function.

## Contributing 🤝
We welcome contributions! If you want to improve this tool or fix a bug, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or fix.
- Make your changes and commit them.
- Push your changes to your fork.
- Create a pull request to the main branch.

## Acknowledgements 💡
- CustomTkinter for an easy-to-use, modern GUI framework.
- yfinance for providing stock data.
- Matplotlib for powerful graphing and visualization.
- Statsmodels for statistical modeling and regression tools.






