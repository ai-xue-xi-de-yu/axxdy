# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api


class WarehouseReturn(models.Model):
    _name = 'warehouse.return'
    _description = '物料借还明细'
    code = fields.Char(string='物料编码')
    name = fields.Char(string=u'货物名称')
    unit_price = fields.Float(string=u'单价')
    apply_number = fields.Integer(string='申请数量')
    lend_name_ids = fields.Many2one('res.users',string=u'申请人')
    cargo_ids = fields.Many2many('cargo.store', string='出借物料')
    warehouse_ids = fields.Many2one('warehouse.table',string='仓库')
    date_lend = fields.Datetime(string='记录时间', default=fields.Datetime.now())
    lend_and_bock = fields.Selection([('0', '出借'), ('1', '归还')], string='属性')

