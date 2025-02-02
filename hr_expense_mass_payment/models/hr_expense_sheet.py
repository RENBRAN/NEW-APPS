# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Aysha Shalin (doo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import models, _
from odoo.exceptions import ValidationError


class HrExpenseSheet(models.Model):
    """This class extends the 'hr.expense.sheet' model to add a new method
    and override an existing method."""
    _inherit = 'hr.expense.sheet'

    def action_post_entries(self):
        """This method posts accounting entries for the approved expense(s).
        It checks if the expenses are in the 'approve' state and sets the
        account_id for each expense.Then, it calls the
        'action_sheet_move_create' method to create the accounting entries.
        """
        if any(rec.state != 'approve' for rec in self):
            raise ValidationError(
                _("You can only generate accounting entries for the approved "
                  "expense(s)."))
        for rec in self:
            for line in rec.expense_line_ids:
                if not line.account_id:
                    line.account_id = self.env['account.account'].search(
                        [('account_type', '=', 'expense')])[0]
            rec.action_sheet_move_post()
