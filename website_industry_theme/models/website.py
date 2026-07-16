# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    industry_theme_id = fields.Many2one('industry.theme', string='Industry Theme', ondelete='set null')
    industry_theme_code = fields.Char(related='industry_theme_id.code', store=True)
    recommended_theme_id = fields.Many2one('industry.theme', string='Recommended Theme', compute='_compute_recommended_theme_id')

    @api.depends('industry_theme_id')
    def _compute_recommended_theme_id(self):
        for website in self:
            # Analyze products and categories to recommend theme
            products = self.env['product.template'].search([('sale_ok', '=', True)])
            if not products:
                website.recommended_theme_id = False
                continue

            veg_keywords = ['vegetable', 'fruit', 'organic', 'farm', 'salad', 'green', 'berry', 'tomato', 'potato', 'grocery']
            fashion_keywords = ['fashion', 'dress', 'shirt', 'clothing', 'shoes', 'wear', 'jewelry', 'jewel', 'gold', 'silver', 'ring', 'cosmetics', 'luxury']
            manufacturing_keywords = ['machine', 'industrial', 'tool', 'steel', 'metal', 'valve', 'manufacturing', 'factory', 'parts']
            restaurant_keywords = ['food', 'dish', 'burger', 'pizza', 'restaurant', 'cafe', 'menu', 'bake', 'bakery', 'meal', 'beverage']
            pharmacy_keywords = ['medicine', 'pill', 'pharmacy', 'health', 'doctor', 'clinic', 'tablet', 'capsule', 'drug']

            counts = {
                'vegetables': 0,
                'fashion': 0,
                'manufacturing': 0,
                'restaurant': 0,
                'pharmacy': 0,
            }

            for p in products:
                name_lower = (p.name or '').lower()
                cat_lower = (p.categ_id.name or '').lower()
                
                # Check vegetables
                if any(k in name_lower or k in cat_lower for k in veg_keywords):
                    counts['vegetables'] += 1
                # Check fashion
                if any(k in name_lower or k in cat_lower for k in fashion_keywords):
                    counts['fashion'] += 1
                # Check manufacturing
                if any(k in name_lower or k in cat_lower for k in manufacturing_keywords):
                    counts['manufacturing'] += 1
                # Check restaurant
                if any(k in name_lower or k in cat_lower for k in restaurant_keywords):
                    counts['restaurant'] += 1
                # Check pharmacy
                if any(k in name_lower or k in cat_lower for k in pharmacy_keywords):
                    counts['pharmacy'] += 1

            # Find the highest count theme
            recommended_code = max(counts, key=counts.get)
            if counts[recommended_code] > 0:
                recommended_theme = self.env['industry.theme'].search([('code', '=', recommended_code)], limit=1)
                website.recommended_theme_id = recommended_theme.id if recommended_theme else False
            else:
                # Default fallback recommendation
                fallback = self.env['industry.theme'].search([('code', '=', 'vegetables')], limit=1)
                website.recommended_theme_id = fallback.id if fallback else False
