from chisel.views import Controller

# Set the global macros asset
Controller.macros_assets = (
    "chisel:templates/macros.pt",
    "propfinder:templates/macros.pt",
)
Controller.process_center_notifications = True

from .backofficelistingview import BackOfficeListingView
from .backofficeeditview import BackOfficeEditView

