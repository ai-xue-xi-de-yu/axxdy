# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepartmentTask(models.Model):
    _name = 'department.task'
    _description = '部门表'
    name = fields.Char(string='部门名称')
    parent_department_ids = fields.Many2one('department.task', string='上级部门')
    user_ids = fields.Many2many('res.users', string='用户')
