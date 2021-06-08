# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime, time


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for line in self.move_line_ids:
            count = self.env['stock.move.line'].search_count([
                ('date', '<=',
                 datetime.combine(datetime.now(), time.max)),
                ('date', '>=',
                 datetime.combine(datetime.now(), time.min))])
            if not line.lot_name:
                line.lot_name = fields.datetime.now().strftime(
                    '%y%m%d') + '/' + str(count).zfill(3)
        return super(Picking, self).button_validate()
