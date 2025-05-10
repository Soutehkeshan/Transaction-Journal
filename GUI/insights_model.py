import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal
import io
from datetime import datetime
import requests
from PIL import Image

class InsightsModel(QObject):
    prices_updated = pyqtSignal(float, float, str)
    graph_generated = pyqtSignal(object, str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, transaction_model):
        super().__init__()
        self.transaction_model = transaction_model
        self.gold_price = 0.0
        self.btc_price = 0.0
        self.last_updated = "Never"
    
    def refresh_prices(self):
        try:
            # Replace with your actual API endpoints for gold and BTC prices
            gold_response = requests.get("https://api.example.com/gold/price")
            btc_response = requests.get("https://api.example.com/btc/price")
            
            if gold_response.status_code == 200 and btc_response.status_code == 200:
                self.gold_price = float(gold_response.json()["price"])
                self.btc_price = float(btc_response.json()["price"])
                self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.prices_updated.emit(self.gold_price, self.btc_price, self.last_updated)
                return True
            else:
                self.error_occurred.emit("Failed to fetch current prices")
                return False
        except Exception as e:
            self.error_occurred.emit(f"Error refreshing prices: {str(e)}")
            return False
    
    def generate_graph(self, graph_type, from_date, to_date):
        try:
            # Get transaction data from the transaction model
            transactions_df = self.transaction_model.get_transactions_df()
            
            if transactions_df.empty:
                self.error_occurred.emit("No transaction data available")
                return False
            
            # Convert QDate objects to Python dates
            from_date_py = from_date.toPyDate()
            to_date_py = to_date.toPyDate()
            
            # Filter transactions by date range
            filtered_df = transactions_df[
                (pd.to_datetime(transactions_df['date']).dt.date >= from_date_py) &
                (pd.to_datetime(transactions_df['date']).dt.date <= to_date_py)
            ]
            
            if filtered_df.empty:
                self.error_occurred.emit("No transactions in selected date range")
                return False
            
            # Create the specified graph type
            plt.figure(figsize=(10, 6))
            
            if graph_type == "Portfolio Value Over Time":
                self._generate_portfolio_value_graph(filtered_df)
            elif graph_type == "Asset Distribution":
                self._generate_asset_distribution_graph(filtered_df)
            elif graph_type == "Profit/Loss Analysis":
                self._generate_profit_loss_graph(filtered_df)
            elif graph_type == "Transaction History":
                self._generate_transaction_history_graph(filtered_df)
            
            # Convert plot to image
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)
            
            self.graph_generated.emit(img, graph_type)
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Error generating graph: {str(e)}")
            return False
    
    def _generate_portfolio_value_graph(self, df):
        # Implementation for portfolio value over time graph
        # This is a placeholder - implement based on your data structure
        pass
    
    def _generate_asset_distribution_graph(self, df):
        # Implementation for asset distribution graph
        # This is a placeholder - implement based on your data structure
        pass
    
    def _generate_profit_loss_graph(self, df):
        # Implementation for profit/loss analysis graph
        # This is a placeholder - implement based on your data structure
        pass
    
    def _generate_transaction_history_graph(self, df):
        # Implementation for transaction history graph
        # This is a placeholder - implement based on your data structure
        pass