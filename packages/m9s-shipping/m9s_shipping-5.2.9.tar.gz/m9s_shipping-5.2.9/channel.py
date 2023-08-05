# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelView, fields
from trytond.pyson import Eval

from trytond.i18n import gettext
from trytond.exceptions import UserError


class SaleChannel(metaclass=PoolMeta):
    __name__ = 'sale.channel'

    shipping_carriers = fields.One2Many(
        'sale.channel.carrier', 'channel', 'Shipping Carriers'
    )

    @classmethod
    def __setup__(cls):
        super(SaleChannel, cls).__setup__()
        cls._buttons.update({
            'import_shipping_carriers': {},
        })

    @classmethod
    def view_attributes(cls):
        invisible = Eval('source').in_(['manual', 'pos'])
        return super(SaleChannel, cls).view_attributes() + [
            ('//page[@id="shipping_carriers"]', 'states', {
                    'invisible': invisible,
                    })
            ]

    @classmethod
    @ModelView.button
    def import_shipping_carriers(cls, channels):
        """
        Create shipping carriers by importing data from external channel.

        Since external channels are implemented by downstream modules, it is
        the responsibility of those channels to reuse this method or call super.

        :param instances: Active record list of magento instances
        """
        raise NotImplementedError("This feature has not been implemented.")

    def get_shipping_carrier(self, code, name, silent=False):
        """
        Search for an existing carrier by matching code and channel.
        If found, return its active record else raise_user_error.
        """
        pool = Pool()
        SaleCarrierChannel = pool.get('sale.channel.carrier')

        try:
            carrier, = SaleCarrierChannel.search([
                ('code', 'ilike', code),
                ('channel', '=', self.id),
            ], limit=1)
            # limit=1 is done to handle concurrency issue
        except ValueError:
            if silent:
                return None
            raise UserError(gettext('sale_channel.no_carriers_found',
                    code,))
        else:
            return carrier

    def get_shipping_carrier_service(self, code, silent=False):
        """
        Search for an existing carrier service by matching code and channel.
        If found, return its active record else raise_user_error.
        """
        pool = Pool()
        SaleCarrierChannel = pool.get('sale.channel.carrier')

        try:
            carrier, = SaleCarrierChannel.search([
                ('code', 'ilike', code),
                ('channel', '=', self.id),
            ], limit=1)
        except ValueError:
            if silent:
                return None
            raise UserError(gettext('shipping.no_carriers_found',
                    code))
        else:
            return carrier.carrier_service
