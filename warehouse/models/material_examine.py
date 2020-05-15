# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError


class MaterialExamine(models.Model):
    _name = 'material.examine'
    _description = '物料审批'
    apply_number = fields.Integer(string='申请数量')
    back_number = fields.Integer(string='归还数量')
    surplus_number = fields.Integer(string='剩余数量')
    is_back = fields.Integer(string='判断', default=1)
    serial_number = fields.Char(string='序列号', default='S/N')
    cargo_ids = fields.Many2many('cargo.store', string='申请详情')
    is_need_back = fields.Boolean(string='需要归还', default=False)
    code = fields.Char(string='物料编码', related='material_id.code')
    name = fields.Char(string=' 物料名称', related='material_id.name')
    material_id = fields.Many2one('material.manage', string='申请的物料')
    material_number = fields.Integer(string='库存数量', related='material_id.max_number')
    apply_user_ids = fields.Many2one('res.users', string='申请人', default=lambda self: self.env.user)
    department_id = fields.Many2many('department.task', string='部门', related='apply_user_ids.department_ids')
    lend_or_back = fields.Selection([('0', '默认'), ('1', '出借'), ('2', '归还')], string='出借或者归还', default='0')
    type = fields.Selection([
        ('0', '待审批'),
        ('1', '出库'),
        ('2', '入库'),
        ('3', '拒绝'),
        ('4', '完成'),
    ], string='审批状态', default='0')

    @api.constrains('back_number')
    def _constraint_back_number(self):
        if self.back_number > self.apply_number and self.back_number != 0:
            raise ValidationError('归还数量不能超过申请数量')

    @api.onchange('apply_number', 'material_number')
    def _onchange_surplus_number(self):
        if self.apply_number > self.material_number:
            raise ValidationError('申请数量不能超过库存')
        else:
            self.surplus_number = self.material_number - self.apply_number

    # 匹配序列号出库
    @api.multi
    def apply_examine(self):
        switch_serial_list = self.material_id.warehouse_ids.type_name_ids
        is_true = True
        is_true_list = []
        for temp in switch_serial_list:
            is_true_list.append(temp.switch_serial)
        if is_true in is_true_list:
            view_id = self.env.ref('warehouse.mutil_number_cargos_view_form').id
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mutil.number',
                'views': [(view_id, 'form')],
                'target': 'new',
                'context': {
                    'warehousename': self.material_id.name,
                    'apply_unmber': self.apply_number,
                    'material_id': self.material_id.id,
                    'examineid': self.id
                }
            }
        else:
            # 获取库存数
            for temp in range(len(self.material_id.cargo_ids)):
                if temp < self.apply_number:
                    self.cargo_ids += self.material_id.cargo_ids[temp]
            self.type = '1'
            self.lend_or_back = '0'

    @api.multi
    def button_tree(self):
        for temp in self:
            if temp.type == '1':
                view_id = self.env.ref('warehouse.material_examine_examine_lend_view_form').id
            else:
                view_id = self.env.ref('warehouse.material_examine_examine_back_view_form').id
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'material.examine',
                'views': [(view_id, 'form')],
                'target': 'new',
                'res_id': temp.id
            }

    # 出库申请通过
    def lend_pass_examine1(self):
        model_material_manage = self.env['material.manage'].search([('id', '=', self.material_id.id)]).browse(
            self.material_id.id)
        flag = self.apply_number
        cargo_length = len(model_material_manage.cargo_ids)

        # 判断申请数量超过出库数量拒绝出库
        if cargo_length < flag:
            self.lend_turn1()
        else:
            list_cargo_ids = []
            cargo_list = []

            # 获取到物料管理里面的库存
            for i in model_material_manage.cargo_ids:
                list_cargo_ids.append(i)
            # 获取申请的库存清单
            for i in self.cargo_ids:
                cargo_list.append(i)
            # 比较判断是否可以出库
            if set(cargo_list) <= set(list_cargo_ids):
                self.type = '4'
                self.lend_or_back = '2'
                self.is_need_back = True
                values_return = {
                    'code': self.code,
                    'name': self.name,
                    'unit_price': self.material_id.unit_price,
                    'lend_and_bock': '0',
                    'apply_number': self.apply_number,
                    'date_lend': fields.datetime.now(),
                    'lend_name_ids': self.apply_user_ids.id,
                    'warehouse_ids': self.material_id.warehouse_ids.id
                }
                model_warehouse_return = self.env['warehouse.return'].create(values_return)
                model_warehouse_return.warehouse_ids = self.material_id.warehouse_ids
                model_warehouse_return.lend_name_ids = self.apply_user_ids
                for temp in cargo_list:
                    model_material_manage.cargo_ids -= temp
                    model_warehouse_return.cargo_ids += temp
                    temp.write({
                        'is_lend': True,
                        'lend_name': self.apply_user_ids.name,
                    })
            else:
                self.cargo_ids = None
                self.lend_turn1()
            model_material_manage.write(
                {
                    'max_number': len(model_material_manage.cargo_ids)

                }
            )

    # 拒绝出库
    def lend_turn1(self):
        cargos_obj = self.env['cargo.store'].search([('is_lend_task', '=', True), ('examineid', '=', str(self.id))])
        for j in cargos_obj:
            j.write({
                'is_lend_task': False,
                'examineid': None,
            })
        self.cargo_ids = None
        self.type = '3'
        self.lend_or_back = '1'

    # 提示框
    def prompt_box(self):
        if self.serial_number == self.material_id.serial_number:
            self.lend_pass_examine1()
        else:
            self.lend_pass_examine1()
            view_id = self.env.ref('warehouse.peompt_box_view_form').id
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'peompt.box',
                'views': [(view_id, 'form')],
                'target': 'new',
            }

    # 提交申请
    def lend_submit1(self):
        self.type = '1'
        self.lend_or_back = '0'

    # 入库申请通过
    @api.multi
    def back_pass_examine(self):
        cargo_obj = self.env['cargo.store'].search(
            [('name', '=', self.name), ('code', '=', self.code), ('is_lend', '=', True),
             ('lend_name', '=', self.apply_user_ids.name)])
        print(cargo_obj)
        flag = self.back_number
        model_material_manage = self.env['material.manage'].search([('id', '=', self.material_id.id)])
        values_return = {
            'code': self.code,
            'name': self.name,
            'unit_price': self.material_id.unit_price,
            'lend_and_bock': '1',
            'apply_number': self.back_number,
            'date_lend': fields.datetime.now(),
            'lend_name_ids': self.apply_user_ids.id,
            'warehouse_ids': self.material_id.warehouse_ids.id
        }
        model_warehouse_return = self.env['warehouse.return'].create(values_return)
        model_warehouse_return.lend_name_ids = self.apply_user_ids
        for j in range(len(cargo_obj)):
            if j < flag:
                cargo_obj[j].is_lend = False
                cargo_obj[j].lend_name_ids = None
                self.cargo_ids -= cargo_obj[j]
                model_warehouse_return.cargo_ids += cargo_obj[j]
                model_material_manage.cargo_ids += cargo_obj[j]
                model_material_manage.max_number = len(model_material_manage.cargo_ids)
        # 改变库存改变申请数
        self.write({
            'apply_number': self.apply_number - self.back_number,
            'surplus_number': self.material_number,
            'back_number': 0
        })
        self.type = '4'
        self.lend_or_back = '2'
        if self.apply_number <= 0:
            self.lend_or_back = '0'
            self.is_need_back = False

    # 提交申请
    def lend_submit(self):
        if self.serial_number == self.material_id.serial_number:
            self.type = '1'
            self.lend_or_back = '0'
        else:
            raise ValidationError('序列号不匹配无法申请出库')

    # 归还
    @api.multi
    def apply_return(self):
        view_id = self.env.ref('warehouse.material_examine_back_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'material.examine',
            'views': [(view_id, 'form')],
            'target': 'new',
            'res_id': self.id
        }

    # 申请归还
    @api.multi
    def apply_back(self):
        self.type = '2'
        self.lend_or_back = '0'
        self.is_back = 1

    # 拒绝归还
    def back_turn(self):
        self.type = '3'
        self.lend_or_back = '2'
        self.is_back = 0
