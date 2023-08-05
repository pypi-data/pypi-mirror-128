# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.pool import PoolMeta, Pool
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval, Or, Bool, Id


class Carrier(metaclass=PoolMeta):
    "Carrier"
    __name__ = 'carrier'

    services = fields.Many2Many(
        "carrier.carrier-service", "carrier", "service", "Services",
        domain=[
            ('carrier_cost_method', '=', Eval('carrier_cost_method'))
        ], depends=['carrier_cost_method']
    )
    package_types = fields.Many2Many(
        "carrier.carrier-stock.package.type", "carrier", "package_type",
        "Package Types",
        domain=['OR', [
            ('carrier_cost_method', '=', Eval('carrier_cost_method'))
        ], [
            ('carrier_cost_method', '=', None)
        ]], depends=['carrier_cost_method']
    )

    def get_sale_price(self):
        """
        Returns sale price for a carrier in following format:
            price, currency_id

        You can ignore the computation by passing `ignore_carrier_computation`
        variable in context, in that case it will always return sale price as
        zero.

        :Example:

        >>> with Transaction().set_context(ignore_carrier_computation=True):
        ...   sale.get_sale_price()
        Decimal('0'), 1
        """
        Company = Pool().get('company.company')

        if Transaction().context.get('ignore_carrier_computation'):
            company = Company(Transaction().context.get('company'))
            return Decimal('0'), company.currency.id
        return super(Carrier, self).get_sale_price()


class Service(ModelSQL, ModelView):
    "Carrier Service"
    __name__ = 'carrier.service'

    carrier_cost_method = fields.Selection(
        [], "Carrier Cost Method", required=True, select=True
    )
    name = fields.Char("Name", required=True, select=True)
    code = fields.Char("Code", required=True, select=True)

    @staticmethod
    def check_xml_record(records, values):
        return True


class CarrierService(ModelSQL):
    "Carrier - Service"
    __name__ = "carrier.carrier-service"

    carrier = fields.Many2One(
        "carrier", "Carrier", ondelete="CASCADE", required=True, select=True
    )
    service = fields.Many2One(
        "carrier.service", "Service", ondelete="CASCADE", required=True,
        select=True
    )


class CarrierPackageType(ModelSQL):
    "Carrier - Package Type"
    __name__ = "carrier.carrier-stock.package.type"

    carrier = fields.Many2One(
        "carrier", "Carrier", ondelete="CASCADE", required=True, select=True
    )
    package_type = fields.Many2One(
        "stock.package.type", "Package Type", ondelete="CASCADE", required=True,
        select=True
    )


class SaleChannelCarrier(ModelSQL, ModelView):
    """
    Shipping Carriers

    This model stores the carriers / shipping methods, each record
    here can be mapped to a carrier in tryton which will then be
    used for managing export of tracking info.
    """
    __name__ = 'sale.channel.carrier'
    _rec_name = 'name'

    name = fields.Char('Name')
    code = fields.Char("Code")
    carrier = fields.Many2One('carrier', 'Carrier')
    carrier_service = fields.Many2One(
        'carrier.service', 'Service', domain=[(
            ('id', 'in', Eval('available_carrier_services'))
        )],
        depends=['available_carrier_services']
    )
    available_carrier_services = fields.Function(
        fields.One2Many("carrier.service", None, 'Available Carrier Services'),
        getter="on_change_with_available_carrier_services"
    )
    channel = fields.Many2One(
        'sale.channel', 'Channel', readonly=True
    )

    @fields.depends('carrier')
    def on_change_with_available_carrier_services(self, name=None):
        if self.carrier:
            return [s.id for s in self.carrier.services]
        return []
