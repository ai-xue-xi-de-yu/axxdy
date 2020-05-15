# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GroupsUser(models.Model):
    _inherit = 'res.users'
    department_ids = fields.Many2many('department.task', string='部门模型')
    warehouse_ids = fields.Many2many('warehouse.table', string='管理的仓库')

    def list_department(self):
        list_department = []
        for temp in self:
            for j in temp.department_ids:
                list_department.append(j.id)
        return list_department

    def list_warehouse_ids(self):
        list_warehouse_ids = []
        for temp in self:
            for j in temp.warehouse_ids:
                list_warehouse_ids.append(j.id)
        return list_warehouse_ids
