# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import ir
from . import carrier
from . import channel
from . import party
from . import shipment
from . import stock
from . import sale
from . import configuration
from . import manifest
from . import location
from . import package
from . import tracking

__all__ = ['register']


def register():
    Pool.register(
        configuration.PartyConfiguration,
        carrier.Carrier,
        carrier.Service,
        carrier.CarrierService,
        carrier.CarrierPackageType,
        ir.Cron,
        party.Address,
        tracking.ShipmentTracking,
        manifest.ShippingManifest,
        stock.StockMove,
        package.Package,
        package.PackageType,
        sale.Sale,
        sale.SaleLine,
        sale.ApplyShippingStart,
        sale.ApplyShippingSelectRate,
        shipment.ShipmentOut,
        party.AddressValidationMsg,
        party.AddressValidationSuggestionView,
        location.Location,
        module='shipping', type_='model')
    Pool.register(
        channel.SaleChannel,
        carrier.SaleChannelCarrier,
        depends=['sale_channel'],
        module='shipping', type_='model')
    Pool.register(
        party.AddressValidationWizard,
        sale.ReturnSale,
        sale.ApplyShipping,
        module='shipping', type_='wizard')
