from PyQt5.QtCore import QObject

class InsightsController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        
        # Connect signals from view to model
        self.view.refresh_prices_signal.connect(self.refresh_prices)
        self.view.generate_graph_signal.connect(self.generate_graph)
        
        # Connect signals from model to view
        self.model.prices_updated.connect(self.view.update_prices)
        self.model.error_occurred.connect(self.view.set_status)
        self.model.graph_generated.connect(self.on_graph_generated)
        
        # Initialize with current prices
        self.refresh_prices()
    
    def refresh_prices(self):
        self.view.set_status("Refreshing prices...")
        success = self.model.refresh_prices()
        if success:
            self.view.set_status("Prices updated successfully")
    
    def generate_graph(self, graph_type, from_date, to_date):
        self.view.set_status(f"Generating {graph_type} graph...")
        self.model.generate_graph(graph_type, from_date, to_date)
    
    def on_graph_generated(self, img, graph_type):
        # This implementation would depend on how you want to display the graph
        # For example, you might want to open a new window or update an existing widget
        self.view.set_status(f"{graph_type} graph generated successfully")
        # Display the graph (implementation details depend on your display strategy)