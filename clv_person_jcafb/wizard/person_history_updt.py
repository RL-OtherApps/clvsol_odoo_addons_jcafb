# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import logging

from odoo import api, models
from odoo import exceptions

_logger = logging.getLogger(__name__)


class PersonHistoryUpdate(models.TransientModel):
    _inherit = 'clv.person.history_updt'

    @api.multi
    def do_person_history_updt(self):
        self.ensure_one()

        PersonHistory = self.env['clv.person.history']

        for person in self.person_ids:

            if self.sign_out_date is False:
                raise exceptions.ValidationError('The "Sign out date" has not been defined!')
                return self._reopen_form()

            if self.sign_in_date is False:
                raise exceptions.ValidationError('The "Sign in date" has not been defined!')
                return self._reopen_form()

            _logger.info(u'%s %s', '>>>>>', person.name)

            if person.global_marker_id.id is not False:

                person_history = PersonHistory.search([
                    ('person_id', '=', person.id),
                    ('global_marker_id', '=', person.global_marker_id.id),
                    ('sign_out_date', '=', False),
                ])

                if person_history.id is False:

                    person_history_2 = PersonHistory.search([
                        ('person_id', '=', person.id),
                        ('sign_out_date', '=', False),
                    ])
                    if person_history_2.id is not False:
                        person_history_2.sign_out_date = self.sign_out_date
                        _logger.info(u'%s %s %s %s %s', '>>>>>>>>>>', person_history_2.global_marker_id.name,
                                                        person_history_2.sign_in_date,
                                                        person_history_2.sign_out_date,
                                                        person_history_2.state)

                    m2m_list = []
                    for category_id in person.category_ids:
                        m2m_list.append((4, category_id.id))
                    category_ids = m2m_list
                    values = {
                        'person_id': person.id,
                        'category_ids': category_ids,
                        'state': person.state,
                        'sign_in_date': self.sign_in_date,
                        'global_marker_id': person.global_marker_id.id,
                    }
                    person_history = PersonHistory.create(values)
                    _logger.info(u'%s %s %s %s %s', '>>>>>>>>>>', person_history.global_marker_id.name,
                                                    person_history.sign_in_date,
                                                    person_history.sign_out_date,
                                                    person_history.state)

                else:
                    m2m_list = []
                    for category_id in person.category_ids:
                        m2m_list.append((4, category_id.id))
                    m2m_list_2 = []
                    for category_id in person_history.category_ids:
                        m2m_list_2.append((4, category_id.id))
                    if m2m_list != m2m_list_2:
                        person_history.category_ids = m2m_list
                    if person_history.state != person.state:
                        person_history.state = person.state
                    _logger.info(u'%s %s %s %s %s', '>>>>>>>>>>', person_history.global_marker_id.name,
                                                    person_history.sign_in_date,
                                                    person_history.sign_out_date,
                                                    person_history.state)

            else:

                person_history = PersonHistory.search([
                    ('person_id', '=', person.id),
                    ('sign_out_date', '=', False),
                ])

                if person_history.id is not False:
                    person_history.sign_out_date = self.sign_out_date
                    _logger.info(u'%s %s %s %s', '>>>>>>>>>>', person_history.global_marker_id.name,
                                                 person_history.sign_in_date,
                                                 person_history.sign_out_date)

        return True
        # return self._reopen_form()
