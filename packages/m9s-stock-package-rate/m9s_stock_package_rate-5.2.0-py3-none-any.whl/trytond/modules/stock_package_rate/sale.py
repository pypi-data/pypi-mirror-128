# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json
from decimal import Decimal

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Not, Bool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.rpc import RPC
from babel.numbers import format_currency

from trytond.i18n import gettext
from trytond.exceptions import UserError


class Sale(metaclass=PoolMeta):
    "Sale"
    __name__ = 'sale.sale'

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

    volume = fields.Function(
        fields.Float(
            "Volume", digits=(16, Eval('volume_digits', 2)),
            depends=['volume_digits'],
        ),
        'get_volume'
    )
    volume_uom = fields.Function(
        fields.Many2One('product.uom', 'Volume UOM'),
        'get_volume_uom'
    )
    volume_digits = fields.Function(
        fields.Integer('Weight Digits'), 'on_change_with_volume_digits'
    )
    carrier_cost_method = fields.Function(
        fields.Char('Carrier Cost Method'),
        "on_change_with_carrier_cost_method"
    )

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._buttons.update({
            'apply_shipping': {
                "invisible": ~Eval('state').in_([
                    'draft', 'quotation', 'confirmed'
                ])
            }
        })
        cls.__rpc__.update({
            'apply_shipping_rate': RPC(instantiate=0)
        })

    @classmethod
    @ModelView.button_action('stock_package_rate.wizard_sale_apply_shipping')
    def apply_shipping(cls, sales):
        pass

    @fields.depends("carrier")
    def on_change_with_carrier_cost_method(self, name=None):
        if self.carrier:
            return self.carrier.carrier_cost_method

    def on_change_lines(self):
        """Pass a flag in context which indicates the get_sale_price method
        of carrier not to calculate cost on each line change
        """
        with Transaction().set_context({'ignore_carrier_computation': True}):
            super(Sale, self).on_change_lines()

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2

    def get_weight_uom(self, name):
        """
        Returns weight uom for the sale
        """
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_gram')

    def get_weight(self, name):
        """
        Returns sum of weight associated with each line
        """
        return sum(
                [line.get_weight(self.weight_uom, silent=True)
                    for line in self.lines])
        return self.weight_uom.round(
            sum(
                [line.get_weight(self.weight_uom, silent=True)
                    for line in self.lines]))

    @fields.depends('volume_uom')
    def on_change_with_volume_digits(self, name=None):
        if self.volume_uom:
            return self.volume_uom.digits
        return 2

    def get_volume_uom(self, name):
        """
        Returns volume uom for the sale
        """
        ModelData = Pool().get('ir.model.data')

        return ModelData.get_id('product', 'uom_liter')

    def get_volume(self, name):
        """
        Returns sum of volume associated with each line
        """
        return self.volume_uom.round(
            sum(
                [line.get_volume(self.volume_uom, silent=True)
                    for line in self.lines]))

    def add_shipping_line(self, shipment_cost, description, carrier=None):
        """
        This method takes shipping_cost and description as arguments and writes
        a shipping line. It deletes any previous shipping lines which have
        a shipment_cost.
        :param shipment_cost: The shipment cost calculated according to carrier
        :param description: Shipping line description
        """
        Sale = Pool().get('sale.sale')

        self.untaxed_amount_cache = self.tax_amount_cache = \
            self.total_amount_cache = None
        self.set_shipment_cost()
        self.save()

        # reset the order total cache
        if self.state not in ('draft', 'quote'):
            Sale.store_cache([self])

    def _get_carrier_context(self):
        "Pass sale in the context"
        context = super(Sale, self)._get_carrier_context()
        context = context.copy()
        context['sale'] = self.id
        return context

    def apply_shipping_rate(self, rate):
        """
        This method applies shipping rate. Rate is a dictionary with following
        minimum keys:

            {
                'display_name': Name to display,
                'carrier_service': carrier.service active record,
                'cost': cost,
                'cost_currency': currency.currency active record,
                'carrier': carrier active record,
            }

        It also creates a shipment line by deleting all existing ones.

        The rate could optionally have integer ids of service, carrier and
        currency.
        """
        pool = Pool()
        Currency = pool.get('currency.currency')
        Carrier = pool.get('carrier')

        if isinstance(rate['carrier'], int):
            self.carrier = Carrier(rate['carrier'])
        else:
            self.carrier = rate['carrier']
        self.save()

        if isinstance(rate['cost_currency'], int):
            cost_currency = Currency(rate['cost_currency'])
        else:
            cost_currency = rate['cost_currency']
        shipment_cost = cost_currency.round(rate['cost'])
        if self.currency != cost_currency:
            shipment_cost = Currency.compute(
                cost_currency, shipment_cost, self.currency)

        self.add_shipping_line(shipment_cost, rate['display_name'],
            carrier=self.carrier)

    def get_shipping_rates(self, carriers=None, silent=False):
        """
        Gives a list of rates from carriers provided. If no carriers provided,
        return rates from all the carriers.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'carrier_service': carrier.service active record,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Carrier = Pool().get('carrier')

        if carriers is None:
            carriers = Carrier.search([])

        rates = []
        for carrier in carriers:
            rates.extend(self.get_shipping_rate(carrier, silent=silent))
        return rates

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        """
        Gives a list of rates from provided carrier and carrier service.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'carrier_service': carrier.service active record,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Company = Pool().get('company.company')

        if carrier.carrier_cost_method == 'product':
            currency = Company(Transaction().context['company']).currency
            rate_dict = {
                'carrier_service': carrier_service,
                'cost': carrier.carrier_product.list_price,
                'cost_currency': currency,
                'carrier': carrier,
            }
            display_name = carrier.rec_name
            rate_dict['display_name'] = display_name
            return [rate_dict]

        return []

    #@classmethod
    #def get_allowed_carriers_domain(cls):
    #    """This method returns domain to seach allowed carriers

    #    Downstream modules can inherit and update customize this domain.
    #    """
    #    return []

    def create_shipment(self, shipment_type):
        with Transaction().set_context(ignore_carrier_computation=True):
            shipments = super(Sale, self).create_shipment(shipment_type)

        if shipment_type == 'out' and shipments:
            for shipment in shipments:
                if shipment.carrier:
                    continue
                shipment.carrier = self.carrier
                shipment.save()

        return shipments


class SaleLine(metaclass=PoolMeta):
    'Sale Line'
    __name__ = 'sale.line'

    def get_weight(self, weight_uom, silent=False):
        """
        Returns weight as required for carriers

        :param weight_uom: Weight uom used by carriers
        :param silent: Raise error if not silent
        """
        ProductUom = Pool().get('product.uom')

        if not self.product or self.quantity <= 0 or \
                self.product.type == 'service':
            return 0

        if not self.product.weight:
            if silent:
                return 0
            raise UserError(gettext('stock_package_rate.weight_required',
                    self.product.name,
                    ))

        # Find the quantity in the default uom of the product as the weight
        # is for per unit in that uom
        if self.unit != self.product.default_uom:
            quantity = ProductUom.compute_qty(
                self.unit,
                self.quantity,
                self.product.default_uom
            )
        else:
            quantity = self.quantity

        weight = self.product.weight * quantity

        # Compare product weight uom with the weight uom used by carrier
        # and calculate weight if both are not same
        if self.product.weight_uom != weight_uom:
            weight = ProductUom.compute_qty(
                self.product.weight_uom,
                weight,
                weight_uom,
            )

        return weight

    def get_volume(self, volume_uom, silent=False):
        """
        Returns volume as required for carriers

        :param volume_uom: Weight uom used by carriers
        :param silent: Raise error if not silent
        """
        ProductUom = Pool().get('product.uom')

        if not self.product or self.quantity <= 0 or \
                self.product.type == 'service':
            return 0

        if not self.product.volume:
            if silent:
                return 0
            raise UserError(gettext('stock_package_rate.volume_required',
                    self.product.name,
                    ))

        # Find the quantity in the default uom of the product as the volume
        # is for per unit in that uom
        if self.unit != self.product.default_uom:
            quantity = ProductUom.compute_qty(
                self.unit,
                self.quantity,
                self.product.default_uom
            )
        else:
            quantity = self.quantity

        volume = self.product.volume * quantity

        # Compare product volume uom with the volume uom used by carrier
        # and calculate volume if botth are not same
        if self.product.volume_uom != volume_uom:
            volume = ProductUom.compute_qty(
                self.product.volume_uom,
                volume,
                volume_uom,
            )

        return volume


class ReturnSale(metaclass=PoolMeta):
    __name__ = 'sale.return_sale'

    def do_return_(self, action):
        Sale = Pool().get('sale.sale')
        action, data = super(ReturnSale, self).do_return_(action)

        Sale.write(Sale.browse(data['res_id']), {
            'carrier': None,
        })

        return action, data


class ApplyShippingStart(ModelView):
    "Apply Shipping"
    __name__ = "sale.sale.apply_shipping.start"

    carrier = fields.Many2One("carrier", "Carrier")
    weight = fields.Float("Weight", required=True)
    volume = fields.Float("Volume", required=True)


class ApplyShippingSelectRate(ModelView):
    'Select Rate'
    __name__ = 'sale.sale.apply_shipping.select_rate'

    rate = fields.Selection([], 'Rate', required=True, sort=False)

    @classmethod
    def default_rate(cls):
        # Fill the first selection value
        return cls.rate.selection and cls.rate.selection[0][0] or None


class ApplyShipping(Wizard):
    "Apply Shipping"
    __name__ = "sale.sale.apply_shipping"
    start_state = 'check'

    check = StateTransition()
    start = StateView(
        'sale.sale.apply_shipping.start',
        'stock_package_rate.apply_shipping_start_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Choose Rate', 'get_rates', 'tryton-go-next', default=True),
        ]
    )
    get_rates = StateTransition()
    select_rate = StateView(
        'sale.sale.apply_shipping.select_rate',
        'stock_package_rate.apply_shipping_select_rate_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Apply', 'apply_rate', 'tryton-go-next', default=True),
        ]
    )
    apply_rate = StateTransition()

    def default_start(self, data):
        return {
            "carrier": self.sale.carrier and self.sale.carrier.id,
            "weight": self.sale.weight,
            "volume": self.sale.volume,
        }

    @property
    def sale(self):
        Sale = Pool().get('sale.sale')
        return Sale(Transaction().context.get('active_id'))

    def transition_check(self):
        if self.sale.state not in ('draft', 'quotation', 'confirmed'):
            raise UserError(gettext('stock_package_rate.wrong_sale_state'))
        return 'start'

    def transition_get_rates(self):
        if self.start.carrier:
            rates = self.sale.get_shipping_rate(
                self.start.carrier, silent=True
            )
        else:
            rates = self.sale.get_shipping_rates(silent=True)

        sorted_rates = sorted(rates, key=lambda r: Decimal("%s" % r['cost']))
        result = []
        for rate in sorted_rates:
            key = json.dumps({
                'display_name': rate['display_name'],
                'cost_currency': rate['cost_currency'].id,
                'cost': str(rate['cost']),
                'carrier': rate['carrier'].id,
            })
            display_name = "%s %s" % (rate['display_name'], format_currency(
                rate['cost'], rate['cost_currency'].code,
                locale=Transaction().language
            ))
            result.append((key, display_name))
        self.select_rate.__class__.rate.selection = result

        return "select_rate"

    def transition_apply_rate(self):
        pool = Pool()
        Currency = pool.get('currency.currency')
        Carrier = pool.get('carrier')

        # Build rate object
        rate = json.loads(self.select_rate.rate)
        rate['cost'] = Decimal(rate['cost'])
        rate['cost_currency'] = Currency(rate['cost_currency'])
        rate['carrier'] = Carrier(rate['carrier'])

        self.sale.apply_shipping_rate(rate)
        return 'end'
