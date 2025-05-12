import pytest
from unittest.mock import MagicMock, patch
from controllers.asset_entry_controller import AssetEntryController

@patch("controllers.asset_entry_controller.Asset")
def test_add_asset_success(mock_asset):
    mock_view = MagicMock()
    mock_view.symbol_input.text.return_value = "BTC"
    mock_view.data_source_input.text.return_value = "CoinGecko"
    mock_view.source_symbol_input.text.return_value = "bitcoin"
    
    controller = AssetEntryController(mock_view)
    controller.add_asset()

    mock_asset.assert_called_once_with("BTC", "CoinGecko", "bitcoin")
    mock_asset.return_value.save.assert_called_once()
    mock_view.status_label.setText.assert_called_with("✅ Asset added successfully.")
    mock_view.clear_inputs.assert_called_once()

@patch("controllers.asset_entry_controller.Asset")
def test_add_asset_missing_symbol(mock_asset):
    mock_view = MagicMock()
    mock_view.symbol_input.text.return_value = ""
    controller = AssetEntryController(mock_view)
    controller.add_asset()

    mock_asset.assert_not_called()
    mock_view.status_label.setText.assert_called_with("❌ Symbol is required.")
