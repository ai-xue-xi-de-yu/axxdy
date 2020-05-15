# -*- coding: utf-8 -*-
import random
from odoo import models, fields, api


class MaterialManage(models.Model):
    _name = 'material.manage'
    _description = '物料管理表'
    name = fields.Char(string='物料名称')
    unit_price = fields.Float(string='单价')
    total_price = fields.Float(string='总金额')
    max_number = fields.Integer(string='库存数量')
    cargo_ids = fields.Many2many('cargo.store', string='物料')
    is_write = fields.Boolean(string='是否可修改', default=False)
    warehouse_ids = fields.Many2one('warehouse.table', string='所在仓库')
    code = fields.Char(string='物料编码', default=lambda self: self.random_code())
    serial_number = fields.Char(string='序列号', default=lambda self: self.random_sequence_number())

    @api.constrains('name')
    def _constraint_name(self):
        for temp in self:
            temp.is_write = True
            if temp.name:
                cargos_obj = self.env['cargo.store'].search([('name', '=', temp.name), ('code', '=', temp.code)])
                for tp in cargos_obj:
                    temp.cargo_ids += tp

    @api.constrains('cargo_ids')
    def _constrains_max_number(self):
        flag = len(self.cargo_ids)
        self.write({
            'max_number': flag,
            'total_price': flag * self.unit_price
        })

    @api.onchange('unit_price', 'max_number')
    def _onchange_total_price(self):
        self.total_price = self.unit_price * self.max_number

    @api.multi
    def random_code(self):
        rand = random.randint(1000, 10000)
        str_code = 'SZPDC' + str(rand)
        mat_obj = self.search([('code', '=', str_code)])
        if mat_obj.id:
            self.random_code()
        else:
            return str_code

    @api.multi
    def random_sequence_number(self):
        rand = random.randint(0, 100)
        str_up = 'S/N' + str(rand)
        mat_obj = self.search([('serial_number', '=', str_up)])
        if mat_obj.id:
            self.random_serial_number()
        else:
            return str_up

    @api.model
    @api.multi
    def create(self, values_list):
        for j in range(values_list.get('max_number')):
            if 1 == len(str(j)):
                number = values_list.get('serial_number') + '0000' + str(j + 1)
            elif 2 == len(str(j)):
                number = values_list.get('serial_number') + '000' + str(j + 1)
            elif 3 == len(str(j)):
                number = values_list.get('serial_number') + '00' + str(j + 1)
            elif 4 == len(str(j)):
                number = values_list.get('serial_number') + '0' + str(j + 1)
            else:
                number = values_list.get('serial_number') + str(j + 1)
            cargo_vals = {
                'name': values_list.get('name'),
                'unit_price': values_list.get('unit_price'),
                'date_create': fields.Datetime.now(),
                'serial_number': number,
                'code': values_list.get('code'),
                'warehouse_ids': values_list.get('warehouse_ids')
            }
            obj = self.env['cargo.store'].create(cargo_vals)
            obj.warehouse_ids = values_list.get('warehouse_ids')
            self.env.cr.commit()
        return super().create(values_list)
