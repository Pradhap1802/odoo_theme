# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    industry_theme_id = fields.Many2one(
        related='website_id.industry_theme_id',
        readonly=False,
        string='Industry Theme'
    )
    recommended_theme_id = fields.Many2one(
        related='website_id.recommended_theme_id',
        string='Recommended Theme',
        readonly=True
    )

    def action_apply_recommended_theme(self):
        self.ensure_one()
        if self.recommended_theme_id:
            self.industry_theme_id = self.recommended_theme_id
        return True
