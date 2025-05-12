import pytest
from unittest.mock import MagicMock, patch
from controllers.transaction_entry_controller import TransactionEntryController

@patch("controllers.transaction_entry_controller.Asset.get_all_symbols", return_value=["BTC"])
@patch("controllers.transaction_entry_controller.Transaction")
@patch("controllers.transaction_entry_controller.fetch_price", return_value=100.0)
@patch("controllers.transaction_entry_controller.datetime")
def test_handle_submit_success(mock_datetime, mock_fetch_price, mock_transaction, mock_get_all_symbols):
    mock_datetime.now.return_value.strftime.return_value = "2024-01-01 12:00:00"

    mock_view = MagicMock()
    mock_view.symbol_input.text.return_value = "BTC"
    mock_view.type_input.currentText.return_value = "Buy"
    mock_view.amount_input.text.return_value = "1.5"
    mock_view.price_input.text.return_value = "25000"
    mock_view.use_market_prices_checkbox.isChecked.return_value = True
    mock_view.note_input.toPlainText.return_value = "Investment"
    mock_view.now_checkbox.isChecked.return_value = True

    controller = TransactionEntryController(mock_view)
    controller.handle_submit()

    mock_transaction.assert_called_once()
    mock_transaction.return_value.save.assert_called_once()
    mock_view.status_label.setText.assert_called_with("✅ Transaction added successfully!")

@patch("controllers.transaction_entry_controller.Asset.get_all_symbols", return_value=["BTC"])
def test_handle_submit_invalid_symbol(mock_get_all_symbols):
    mock_view = MagicMock()
    mock_view.symbol_input.text.return_value = "ETH"
    controller = TransactionEntryController(mock_view)
    controller.handle_submit()

    mock_view.status_label.setText.assert_called_with("❌ Error: This asset does not exist. Please add it first.")
