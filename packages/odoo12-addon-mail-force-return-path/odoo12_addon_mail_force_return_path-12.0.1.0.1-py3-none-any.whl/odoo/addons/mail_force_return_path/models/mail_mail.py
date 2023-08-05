from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval
import json

class MailMail(models.Model):
    """ Model holding RFC2822 email messages to send. This model also provides
        facilities to queue and send new email messages.  """
    _inherit = 'mail.mail'

    @api.multi
    def _send(self, auto_commit=False, raise_exception=False, smtp_session=None):
        for mail_id in self.ids:
            mail = self.browse(mail_id)
            if mail.headers:
                headers = safe_eval(mail.headers)
                headers['Return-Path'] = mail.email_from
            else:
                headers = {'Return-Path': mail.email_from}
            mail.headers = str(headers)
        return super()._send(auto_commit, raise_exception, smtp_session)


