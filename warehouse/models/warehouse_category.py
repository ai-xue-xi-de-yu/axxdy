# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WarehouseCategory(models.Model):
    _name = 'warehouse.category'
    _description = '物料分类'
    name = fields.Char(string='分类名称')
    switch_serial = fields.Boolean(string='序列号开关')
