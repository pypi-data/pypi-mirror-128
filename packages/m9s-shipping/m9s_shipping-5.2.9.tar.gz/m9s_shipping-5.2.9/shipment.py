# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

from .mixin import ShipmentCarrierMixin


class ShipmentOut(ShipmentCarrierMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @property
    def carrier_cost_moves(self):
        return [m for m in self.outgoing_moves
            if (m.state != 'cancel' and m.quantity)]

    def on_change_inventory_moves(self):
        with Transaction().set_context(ignore_carrier_computation=True):
            super(ShipmentOut, self).on_change_inventory_moves()

    @classmethod
    def get_weight(cls, records, name=None):

        res = {}
        for shipment in records:
            weight_uom = shipment.weight_uom

            if shipment.packages or (shipment.state in ('packed', 'done')):
                res.update(super(ShipmentOut, cls).get_weight([shipment], name))
                continue

            inventory_moves = [m for m in shipment.inventory_moves
                if (m.state != 'cancel' and m.quantity)]
            res[shipment.id] = sum([
                move.get_weight(weight_uom, silent=True)
                for move in inventory_moves
            ])

        return res

    @classmethod
    def pack(cls, shipments):
        for shipment in shipments:
            if not shipment.packages:
                # No package, create a default package
                shipment._create_default_package()
        super(ShipmentOut, cls).pack(shipments)
