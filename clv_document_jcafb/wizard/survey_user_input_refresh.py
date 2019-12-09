# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SurveyUserInputRefresh(models.TransientModel):
    _description = 'Survey User Input Refresh'
    _name = 'survey.user_input.refresh'

    def _default_survey_user_input_ids(self):
        return self._context.get('active_ids')
    survey_user_input_ids = fields.Many2many(
        comodel_name='survey.user_input',
        relation='survey_user_input_refresh_rel',
        string='Survey User Inputs',
        default=_default_survey_user_input_ids
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_survey_user_input_refresh(self):
        self.ensure_one()

        Document = self.env['clv.document']

        for survey_user_input in self.survey_user_input_ids:

            _logger.info(u'%s %s', '>>>>>', survey_user_input.token)

            if survey_user_input.state_2 in ['new', 'returned', 'checked']:

                survey_user_input.state_2 = 'checked'
                survey_user_input.document_code = False
                survey_user_input.person_code = False
                survey_user_input.family_code = False
                survey_user_input.address_code = False
                survey_user_input.notes = False
                survey_user_input.document_id = False

                document_code = False
                person_code = False
                family_code = False
                address_code = False

                for user_input_line in survey_user_input.user_input_line_ids:

                    question_parameter = user_input_line.question_id.parameter
                    value_text = user_input_line.value_text

                    # _logger.info(u'%s %s', '>>>>> (question_parameter):', question_parameter)
                    # _logger.info(u'%s %s', '>>>>> (value_text):', value_text)

                    if question_parameter == 'document_code':
                        document_code = value_text
                        survey_user_input.document_code = document_code

                    if question_parameter == 'person_code':
                        person_code = value_text
                        survey_user_input.person_code = person_code

                    if question_parameter == 'family_code':
                        family_code = value_text
                        survey_user_input.family_code = family_code

                    if question_parameter == 'address_code':
                        address_code = value_text
                        survey_user_input.address_code = address_code

                if document_code is not False:

                    document = Document.search([
                        ('code', '=', document_code),
                    ])

                    if document.code != document_code:
                        survey_user_input.state_2 = 'returned'
                        if survey_user_input.notes is False:
                            survey_user_input.notes = u'Erro: Código do Documento inválido!'
                        else:
                            survey_user_input.notes += u'\nErro: Código do Documento inválido!'

                    else:

                        survey_user_input.document_id = document.id

                        if person_code is not False:

                            if document.ref_id.code != person_code:
                                survey_user_input.state_2 = 'returned'
                                if survey_user_input.notes is False:
                                    survey_user_input.notes = u'Erro: Código da Pessoa inválido!'
                                else:
                                    survey_user_input.notes += u'\nErro: Código da Pessoa inválido!'
                        if family_code is not False:

                            if document.ref_id.code != family_code:
                                survey_user_input.state_2 = 'returned'
                                if survey_user_input.notes is False:
                                    survey_user_input.notes = u'Erro: Código da Família inválido!'
                                else:
                                    survey_user_input.notes += u'\nErro: Código da Família inválido!'
                        if address_code is not False:

                            if document.ref_id.code != address_code:
                                survey_user_input.state_2 = 'returned'
                                if survey_user_input.notes is False:
                                    survey_user_input.notes = u'Erro: Código do Endereço inválido!'
                                else:
                                    survey_user_input.notes += u'\nErro: Código ddo Endereço inválido!'

                else:

                    if survey_user_input.state_2 in ['new', 'returned', 'checked']:

                        survey_user_input.state_2 = 'new'
                        survey_user_input.document_code = False
                        survey_user_input.person_code = False
                        survey_user_input.family_code = False
                        survey_user_input.address_code = False
                        survey_user_input.notes = False
                        survey_user_input.document_id = False

        return True

    @api.multi
    def do_populate_all_survey_user_inputs(self):
        self.ensure_one()

        SurveyUserInput = self.env['survey.user_input']
        survey_user_inputs = SurveyUserInput.search([])

        self.survey_user_input_ids = survey_user_inputs

        return self._reopen_form()
