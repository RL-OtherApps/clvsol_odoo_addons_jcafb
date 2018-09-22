# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Person(models.Model):
    _inherit = 'clv.person'

    _lab_test_request_ids = fields.One2many(
        string='Lab Test Requests',
        comodel_name='clv.lab_test.request',
        compute='_compute_lab_test_request_ids_and_count',
    )
    _count_lab_test_requests = fields.Integer(
        compute='_compute_lab_test_request_ids_and_count',
    )

    @api.multi
    def _compute_lab_test_request_ids_and_count(self):
        for record in self:
            lab_test_requests = self.env['clv.lab_test.request'].search([
                ('ref_id', '=', self._name + ',' + str(record.id)),
            ])
            record._count_lab_test_requests = len(lab_test_requests)
            record._lab_test_request_ids = [(6, 0, lab_test_requests.ids)]

    _lab_test_result_ids = fields.One2many(
        string='Lab Test Results',
        comodel_name='clv.lab_test.result',
        compute='_compute_lab_test_result_ids_and_count',
    )
    _count_lab_test_results = fields.Integer(
        compute='_compute_lab_test_result_ids_and_count',
    )

    @api.multi
    def _compute_lab_test_result_ids_and_count(self):
        for record in self:
            lab_test_results = self.env['clv.lab_test.result'].search([
                ('ref_id', '=', self._name + ',' + str(record.id)),
            ])
            record._count_lab_test_results = len(lab_test_results)
            record._lab_test_result_ids = [(6, 0, lab_test_results.ids)]

    _lab_test_report_ids = fields.One2many(
        string='Lab Test Reports',
        comodel_name='clv.lab_test.report',
        compute='_compute_lab_test_report_ids_and_count',
    )
    _count_lab_test_reports = fields.Integer(
        compute='_compute_lab_test_report_ids_and_count',
    )

    @api.multi
    def _compute_lab_test_report_ids_and_count(self):
        for record in self:
            lab_test_reports = self.env['clv.lab_test.report'].search([
                ('ref_id', '=', self._name + ',' + str(record.id)),
            ])
            record._count_lab_test_reports = len(lab_test_reports)
            record._lab_test_report_ids = [(6, 0, lab_test_reports.ids)]
