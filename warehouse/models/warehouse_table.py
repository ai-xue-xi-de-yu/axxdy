# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WarehouseTable(models.Model):
    _name = 'warehouse.table'
    _description = '仓库表'
    name = fields.Char(string=u'仓库名')
    type_name_ids = fields.Many2many('warehouse.category', string='分类')
    material_id = fields.One2many('material.manage', 'warehouse_ids', string='仓库库存')
    admin_ids = fields.Many2many('res.users', string='管理员', default=lambda self: self.env.user)
