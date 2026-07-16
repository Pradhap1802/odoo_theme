# -*- coding: utf-8 -*-
import json
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IndustryThemeImportWizard(models.TransientModel):
    _name = 'industry.theme.import.wizard'
    _description = 'Import Industry Theme Wizard'

    file = fields.Binary(string='Theme File (.json)', required=True)
    file_name = fields.Char(string='File Name')
    category_id = fields.Many2one('industry.theme.category', string='Override Category')

    def action_import(self):
        self.ensure_one()
        if not self.file_name or not self.file_name.endswith('.json'):
            raise UserError(_("Please upload a valid JSON file."))
        
        try:
            content = base64.b64decode(self.file).decode('utf-8')
            data = json.loads(content)
        except Exception as e:
            raise UserError(_("Error parsing JSON file: %s") % str(e))

        # Recreate models
        palette_data = data.get('palette')
        palette = False
        if palette_data:
            palette = self.env['industry.theme.palette'].create({
                'name': palette_data.get('name', 'Imported Palette'),
                'primary_color': palette_data.get('primary_color'),
                'secondary_color': palette_data.get('secondary_color'),
                'accent_color': palette_data.get('accent_color'),
                'bg_color': palette_data.get('bg_color'),
            })

        layout_data = data.get('layout')
        layout = False
        if layout_data:
            layout = self.env['industry.theme.layout'].create({
                'name': layout_data.get('name', 'Imported Layout'),
                'border_radius': layout_data.get('border_radius'),
                'button_style': layout_data.get('button_style'),
                'card_style': layout_data.get('card_style'),
                'shadow_style': layout_data.get('shadow_style'),
                'animation_style': layout_data.get('animation_style'),
                'spacing_scale': layout_data.get('spacing_scale'),
            })

        font_data = data.get('font')
        font = False
        if font_data:
            font = self.env['industry.theme.font'].create({
                'name': font_data.get('name', 'Imported Font'),
                'font_family': font_data.get('font_family'),
                'font_url': font_data.get('font_url'),
            })

        category = self.category_id
        if not category and data.get('category'):
            category = self.env['industry.theme.category'].search([('name', '=', data.get('category'))], limit=1)
            if not category:
                category = self.env['industry.theme.category'].create({
                    'name': data.get('category'),
                    'code': data.get('category').lower().replace(' ', '_'),
                })

        new_theme = self.env['industry.theme'].create({
            'name': data.get('name', 'Imported Theme'),
            'code': data.get('code', 'imported_theme'),
            'category_id': category.id if category else False,
            'palette_id': palette.id if palette else False,
            'layout_id': layout.id if layout else False,
            'font_id': font.id if font else False,
            'header_layout': data.get('header_layout', 'default'),
            'footer_layout': data.get('footer_layout', 'default'),
            'shop_layout': data.get('shop_layout', 'default'),
            'product_grid': data.get('product_grid', '3_cols'),
            'product_card_style': data.get('product_card_style', 'default'),
            'category_card_style': data.get('category_card_style', 'default'),
            'blog_style': data.get('blog_style', 'default'),
            'newsletter_style': data.get('newsletter_style', 'default'),
            'whatsapp_enabled': data.get('whatsapp_enabled', True),
            'whatsapp_number': data.get('whatsapp_number', "+1234567890"),
            'back_to_top_enabled': data.get('back_to_top_enabled', True),
            'loading_animation_enabled': data.get('loading_animation_enabled', True),
            'hover_effects_style': data.get('hover_effects_style', 'none'),
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'industry.theme',
            'view_mode': 'form',
            'res_id': new_theme.id,
            'target': 'current',
        }
