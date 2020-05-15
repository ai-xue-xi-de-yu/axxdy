# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CargoStore(models.Model):
    _name = 'cargo.store'
    _description = '货物储存表'
    code = fields.Char(string='物料编码')
    name = fields.Char(string=u'货物名称')
    unit_price = fields.Float(string=u'单价')
    lend_name = fields.Char(string=u'借用人')
    examine_id = fields.Char(string='审批id')
    serial_number = fields.Char(string=u'序列号')
    is_lend = fields.Boolean(string='是否出借', default=False)
    is_lend_task = fields.Boolean(string='待出借', default=False)
    warehouse_ids = fields.Many2one('warehouse.table',string='所在仓库')
    date_create = fields.Datetime(string=u'入库时间', default=fields.Datetime.now())
