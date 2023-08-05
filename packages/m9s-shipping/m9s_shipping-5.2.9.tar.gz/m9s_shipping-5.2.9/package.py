# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool, Id
from trytond.transaction import Transaction


class Package(metaclass=PoolMeta):
    __name__ = 'stock.package'

    tracking_number = fields.Function(
        fields.Many2One('shipment.tracking', 'Tracking Number'),
        'get_tracking_number', searcher="search_tracking_number"
    )

    weight = fields.Function(
        fields.Float(
            "Weight", digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits'],
        ),
        'get_weight'
    )
    weight_uom = fields.Function(
        fields.Many2One('product.uom', 'Weight UOM'),
        'get_weight_uom'
    )
    weight_digits = fields.Function(
        fields.Integer('Weight Digits'), 'on_change_with_weight_digits'
    )

    computed_weight = fields.Function(
        fields.Float(
            "Computed Weight", digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits'],
        ),
        'get_computed_weight'
    )

    override_weight = fields.Float(
        "Override Weight", digits=(16, Eval('weight_digits', 2)),
        depends=['weight_digits'],
    )

    override_weight_uom = fields.Many2One(
        'product.uom', 'Override Weight UOM', domain=[
            ('category', '=', Id('product', 'uom_cat_weight'))
        ], states={
            'required': Bool(Eval('override_weight')),
        }, depends=['override_weight']
    )

    available_package_types = fields.Function(
        fields.One2Many("stock.package.type", None, "Available Package Types"),
        getter="on_change_with_available_package_types"
    )

    @classmethod
    def __setup__(cls):
        super().__setup__()
        type_domain = ('id', 'in', Eval('available_package_types'))
        if type_domain not in cls.type.domain:
            cls.type.domain.append(type_domain)
        type_depends = 'available_package_types'
        if type_depends not in cls.type.depends:
            cls.type.depends.append(type_depends)

    @fields.depends('shipment')
    def on_change_with_available_package_types(self, name=None):
        Carrier = Pool().get('carrier')

        carrier = None
        if self.shipment:
            carrier = self.shipment.carrier
        elif Transaction().context.get('carrier'):
            carrier = Carrier(Transaction().context.get('carrier'))

        if carrier is not None:
            return list(map(int, carrier.package_types))
        return []

    def _process_raw_label(self, data, **kwargs):
        "Downstream modules can use this method to process label image"
        return data

    def get_tracking_number(self, name):
        """
        Return first tracking number for this package
        """
        Tracking = Pool().get('shipment.tracking')

        tracking_numbers = Tracking.search([
            ('origin', '=', '%s,%s' % (self.__name__, self.id)),
            ('state', '!=', 'cancelled'),
        ], limit=1)

        return tracking_numbers and tracking_numbers[0].id or None

    @classmethod
    def search_tracking_number(cls, name, clause):
        Tracking = Pool().get('shipment.tracking')

        tracking_numbers = Tracking.search([
            ('origin', 'like', 'stock.package,%'),
            ('tracking_number', ) + tuple(clause[1:])
        ])
        return [
            ('id', 'in', [x.origin.id for x in tracking_numbers])
        ]

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2

    def get_weight_uom(self, name):
        """
        Returns weight uom for the package from shipment
        """
        return self.shipment.weight_uom.id

    def get_weight(self, name):
        """
        Returns package weight if weight is not overriden
        otherwise returns overriden weight
        """
        UOM = Pool().get('product.uom')
        if self.override_weight:
            return UOM.compute_qty(
                self.override_weight_uom,
                self.override_weight,
                self.weight_uom
            )
        return self.get_computed_weight()

    def get_computed_weight(self, name=None):
        """
        Returns sum of weight associated with each move line
        """
        return sum([move.get_weight(self.weight_uom, silent=True) for move in self.moves])

    @staticmethod
    def default_type():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id(
            'shipping', 'shipment_package_type'
        )

    @staticmethod
    def default_override_weight_uom():
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id(
            'product', 'uom_pound'
        )


class PackageType(metaclass=PoolMeta):
    __name__ = 'stock.package.type'

    #: Same as `carrier.carrier_cost_method`.
    carrier_cost_method = fields.Selection([(None, '')], 'Carrier Cost Method')

    #: Code of the box.
    code = fields.Char('Code', readonly=True)
