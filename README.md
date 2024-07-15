# Live Trading Strategy with Fyers API

## Overview
This project demonstrates live trading using a strategy. The strategy connects to the Fyers API via WebSocket to receive real-time market data and executes trades based on predefined Conditions.

## Main Goal
The primary goal of this project is to provide a comprehensive example of a live trading strategy that connects to the Fyers API, monitors market conditions, and executes trades based on a predefined strategy.

## Key Features
- **Live Execution**: Establishes a WebSocket connection with the Fyers API to facilitate real-time data streaming and immediate trade execution.
- **Customizable Strategy**: Provides an example trading strategy based on RSI, which users can customize and expand to create their own trading algorithms.
- **Automated Trade Management**: Monitors trades continuously, adjusting positions based on RSI signals and predefined rules for target profit, stop loss, and time-based exits.
- **Comprehensive Logging**: Logs detailed trade activities and outcomes for thorough analysis and strategy optimization.

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Pip package manager

### Installation
1. Clone the repository:
   ```bash
    git clone <repository_url>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```


### Configuration
1. Create a `user.json` file in the root directory with your Fyers API credentials:

    **Note**: Replace `your_app_id` and `your_access_token` with your Fyers API credentials.
```json
{
  "user": {
    "app_id": "your_app_id",
    "access_token": "your_access_token"
  }
}
```

### Running the Strategy
Execute the strategy.py script to start the live trading strategy:
```bash
python strategy.py
```
This command initiates the strategy, establishes a WebSocket connection with Fyers, and begins live trading based on the configured RSI strategy.

### Directory Structure
#### core/:
Contains essential modules like WebSocket handler and utility functions.
#### LogFiles/: 
Stores detailed logs of trade activities and system events.
#### TradeBooks/:
Archives trade history in CSV format for record-keeping and analysis.

### Notes
Adhere to market trading hours and regulatory guidelines applicable to your trading jurisdiction.
Customize strategy parameters such as RSI period, target profit, and stop loss to align with your risk management and trading objectives.

## Tutorial
### Introduction
This tutorial guides you through setting up and executing the live trading strategy using the provided example implementation.

#### Step-by-Step Instructions

Clone the repository and install necessary dependencies as outlined in the setup instructions.
Configure the user.json file with your Fyers API credentials for authentication.
Running the Strategy

Launch the strategy execution by running strategy.py.
Observe real-time trade activities and system logs displayed in the console.
Monitoring Trades

Learn how the strategy dynamically evaluates RSI conditions to initiate and manage trades.
Follow trade execution based on predefined profit targets, stop losses, and time-based exit strategies.
Reviewing Results

Access trade history and performance metrics stored in the TradeBooks/ directory.
Analyze detailed logs in LogFiles/ to evaluate strategy effectiveness and identify areas for improvement.

### Conclusion
Congratulations on successfully implementing and running a live trading strategy using the RSI indicator with the Fyers API. Explore further customization options and enhancements to optimize your trading experience and achieve your financial goals.

### Next Steps
1. Experiment with adjusting strategy parameters and thresholds to fine-tune performance.
2. Explore advanced logging techniques and integrate additional technical indicators for enhanced trading strategies.
3. Extend the strategy to different financial instruments or timeframes to diversify trading opportunities.

## Resources
- [Fyers API Documentation](https://developers.fyers.in/)
- [Python Programming Language](https://www.python.org/)
- [Technical Analysis Library in Python (TA-Lib)](https://technical-analysis-library-in-python.readthedocs.io/en/latest/)
- 