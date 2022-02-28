import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api

class ImportPrestashopShipping(models.TransientModel):
    _name = "import.prestashop.shipping"
    _inherit = "import.operation"
    _description = "Import Prestashop Shipping"

    def import_now(self):
        data_list = []
        prestashop = self._context.get("prestashop")
        channel_id = self._context.get("channel_id")
        prestashop_object_id = self._context.get("prestashop_object_id")
        if prestashop_object_id:
            vals = self.get_shipping_vals(channel_id, prestashop, prestashop_object_id)
            if isinstance(vals,dict):
                data_list.append(vals)
        else:
            data_list = self.get_shipping_all(prestashop, channel_id)
        return data_list

    def get_shipping_all(self,prestashop ,channel_id):
        vals_list = []
        try:
            shipping_data = prestashop.get("carriers")
        except Exception as e:
            _logger.info("ShippingError ======> %r",str(e))
        else:
            shipping_ids = shipping_data.get("carriers",{}).get("carrier")
            if isinstance(shipping_ids,list):
                _logger.info("shipping_Data =======> %r",shipping_data)
                vals_list = list(map(lambda x: self.get_shipping_vals(channel_id,prestashop,x.get("attrs",{}).get("id")),shipping_ids))
        return vals_list

    def get_shipping_vals(self, channel_id, prestashop, shipping_id):
        if shipping_id:
            try:
                shipping_data = prestashop.get("carriers",shipping_id)
            except Exception as e:
                _logger.info("Shipping Error ==========> %r",str(e))
            else:
                return {
                    "name": shipping_data["carrier"].get("name"),
                    "store_id": shipping_data["carrier"].get("id"),
                    "shipping_carrier": shipping_data["carrier"].get("name"),
                    "channel_id": channel_id.id,
                    "channel": channel_id.channel,
                    "description": shipping_data["carrier"].get("description",False)
                    }   
