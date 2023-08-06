# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    is_present = fields.Boolean('Present Today', compute='_compute_leave_status', search='_search_present_employee')

    @api.multi
    def _search_present_employee(self, operator, value):
        holidays = self.env['hr.leave'].sudo().search([
            ('employee_id', '!=', False),
            ('state', 'not in', ['cancel', 'refuse']),
            ('date_from', '<=', datetime.datetime.utcnow()),
            ('date_to', '>=', datetime.datetime.utcnow())
        ])
        return [('id', 'not in', holidays.mapped('employee_id').ids)]

