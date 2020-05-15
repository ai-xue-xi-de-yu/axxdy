# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class warehouse(models.TransientModel):
    _name = 'warehouse.warehouse'

    @api.multi
    def all_pass(self):
        context = dict(self._context or {})
        ids = context.get('ids')
        # 拿到一个ids
        for i in ids:
            # 拿到每一条记录
            me_obj = self.env['material.examine'].search([('id', '=', i)])
            if me_obj.type == '1':
                me_obj.lend_pass_examine1()
            elif me_obj.type == '2':
                me_obj.back_pass_examine()
            else:
                pass

    @api.multi
    def all_trun(self):
        context = dict(self._context or {})
        ids = context.get('ids')
        for i in ids:
            me_obj = self.env['material.examine'].search([('id', '=', i)])
            if me_obj.type == '1':
                me_obj.lend_turn1()
            elif me_obj.type == '2':
                me_obj.back_turn()
            else:
                pass


class PromptBox(models.TransientModel):
    _name = 'peompt.box'

    def confirm_button(self):
        pass


class PromptNumber(models.TransientModel):
    _name = 'peompt.bumber'

    def pass_button(self):
        context = dict(self._context or {})
        mutil_number_id = context.get('mutil_number_ids')

        view_id = self.env.ref('warehouse.mutil_number_cargos_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mutil.number',
            'views': [(view_id, 'form')],
            'target': 'new',
            'res_id': int(mutil_number_id)
        }


class Mutil_Number(models.TransientModel):
    _name = 'mutil.number'
    sup_number = fields.Char(string='序列号', default='S/N')
    cargo_ids = fields.Many2many('cargo.store', string='申请详情')
    cargos_name = fields.Char(string='名字', default=lambda self: self.apply_name())
    apply_number = fields.Char(string='申请数量', default=lambda self: self.apply_Apply_Unmber())

    def apply_Apply_Unmber(self):
        context = dict(self._context or {})
        return context.get('apply_unmber')

    def apply_name(self):
        context = dict(self._context or {})
        return context.get('warehousename')

    @api.multi
    def all_mil_pass(self):
        context = dict(self._context or {})
        lengths = context.get('apply_unmber')
        material_id = context.get('material_id')
        examineid = context.get('examineid')
        if lengths != len(self.cargo_ids) and lengths < len(self.cargo_ids):
            raise ValidationError('选择的物料数大于申请数量')
        elif lengths != len(self.cargo_ids) and lengths > len(self.cargo_ids):
            raise ValidationError('选择的物料数小于申请数量')
        else:
            cargo_list = []
            unmatched = False
            pass_list = []
            obj = self.env['material.manage'].search([('id', '=', int(material_id))])
            for temp in obj.cargo_ids:
                cargo_list.append(temp)
            for temp in self.cargo_ids:
                if temp in cargo_list:
                    pass_list.append(temp)
                else:
                    unmatched = True
                    self.cargo_ids -= temp
            print(cargo_list)
            print(pass_list)
            print(unmatched)
            if unmatched:
                view_id = self.env.ref('warehouse.peompt_bumber_view_form').id
                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'peompt.bumber',
                    'views': [(view_id, 'form')],
                    'target': 'new',
                    'context': {
                        'mutil_number_ids': self.id
                    },
                }
            else:
                # 做相关添加操作
                examine_obj = self.env['material.examine'].search([('id', '=', int(examineid))])
                for temp in pass_list:
                    examine_obj.cargo_ids += temp
                    examine_obj.serial_number = obj.serial_number
                    examine_obj.lend_submit()

    def button_cancel(self):
        pass
