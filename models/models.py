# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime, time


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for line in self.move_line_ids:
            if line.product_id.tracking == 'lot':
                count = self.env['stock.move.line'].search_count([
                    ('date', '<=',
                     datetime.combine(datetime.now(), time.max)),
                    ('date', '>=',
                     datetime.combine(datetime.now(), time.min))])
                if not line.lot_id:
                    serial = datetime.now().strftime(
                        '%y%m%d') + '/' + str(count).zfill(3)
                    line.lot_id = self.env['stock.production.lot'].create({
                        'name': serial,
                        'product_id': line.product_id.id,
                        'company_id': line.company_id.id}).id
        return super(Picking, self).button_validate()
