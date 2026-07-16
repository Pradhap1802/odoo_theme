# -*- coding: utf-8 -*-
import json
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IndustryThemeCategory(models.Model):
    _name = 'industry.theme.category'
    _description = 'Industry Theme Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Category Code', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)


class IndustryThemePalette(models.Model):
    _name = 'industry.theme.palette'
    _description = 'Industry Theme Color Palette'

    name = fields.Char(string='Palette Name', required=True)
    primary_color = fields.Char(string='Primary Color', default='#000000', required=True)
    secondary_color = fields.Char(string='Secondary Color', default='#666666', required=True)
    accent_color = fields.Char(string='Accent Color', default='#FF0000', required=True)
    bg_color = fields.Char(string='Background Color', default='#FFFFFF', required=True)


class IndustryThemeFont(models.Model):
    _name = 'industry.theme.font'
    _description = 'Industry Theme Typography'

    name = fields.Char(string='Font Name', required=True)
    font_family = fields.Char(string='Font Family CSS', required=True, help="e.g. 'Outfit', sans-serif")
    font_url = fields.Char(string='Google Fonts URL', help="Stylesheet Link to load Google Fonts")


class IndustryThemeLayout(models.Model):
    _name = 'industry.theme.layout'
    _description = 'Industry Theme Layout Settings'

    name = fields.Char(string='Layout Name', required=True)
    border_radius = fields.Char(string='Border Radius CSS', default='4px', required=True)
    button_style = fields.Selection([
        ('flat', 'Flat'),
        ('rounded', 'Rounded'),
        ('pill', 'Pill'),
        ('shadowed', 'Shadowed')
    ], string='Button Style', default='rounded', required=True)
    card_style = fields.Selection([
        ('minimal', 'Minimalist'),
        ('boxed', 'Boxed'),
        ('bordered', 'Bordered'),
        ('shadowed', 'Shadowed')
    ], string='Card Style', default='bordered', required=True)
    shadow_style = fields.Char(string='Shadow CSS', default='none', required=True)
    animation_style = fields.Selection([
        ('none', 'None'),
        ('fade', 'Fade In'),
        ('slide', 'Slide Up'),
        ('zoom', 'Subtle Zoom')
    ], string='Animation Style', default='fade', required=True)
    spacing_scale = fields.Selection([
        ('compact', 'Compact Spacing'),
        ('normal', 'Normal Spacing'),
        ('loose', 'Loose Spacing')
    ], string='Spacing Scale', default='normal', required=True)


class IndustryThemeBanner(models.Model):
    _name = 'industry.theme.banner'
    _description = 'Industry Theme Hero/Offer Banner'

    name = fields.Char(string='Banner Name', required=True)
    banner_type = fields.Selection([
        ('hero', 'Hero Banner'),
        ('offer', 'Offer Banner'),
        ('collections', 'Collections Banner')
    ], string='Banner Type', default='hero', required=True)
    title = fields.Char(string='Title', required=True)
    subtitle = fields.Text(string='Subtitle')
    bg_image = fields.Binary(string='Background Image')
    cta_text = fields.Char(string='CTA Button Text')
    cta_url = fields.Char(string='CTA Button URL')


class IndustryThemeBlock(models.Model):
    _name = 'industry.theme.block'
    _description = 'Industry Theme Reusable Block'

    name = fields.Char(string='Block Name', required=True)
    block_type = fields.Selection([
        ('why_choose_us', 'Why Choose Us'),
        ('features', 'Features Grid'),
        ('blog', 'Blog Posts'),
        ('faq', 'FAQ Accordion'),
        ('testimonials', 'Testimonials Carousel')
    ], string='Block Type', required=True)
    content_html = fields.Html(string='HTML Content')


class IndustryThemePreview(models.Model):
    _name = 'industry.theme.preview'
    _description = 'Theme Visual Preview'

    name = fields.Char(string='Preview Label', required=True)
    theme_id = fields.Many2one('industry.theme', string='Theme', ondelete='cascade')
    preview_type = fields.Selection([
        ('desktop', 'Desktop View'),
        ('tablet', 'Tablet View'),
        ('mobile', 'Mobile View'),
        ('thumbnail', 'Live Thumbnail')
    ], string='Preview Target', required=True)
    screenshot = fields.Binary(string='Screenshot / Image', required=True)


class IndustryTheme(models.Model):
    _name = 'industry.theme'
    _description = 'Industry Specific Theme'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Theme Name', required=True, tracking=True)
    code = fields.Char(string='Theme Code', required=True, tracking=True)
    category_id = fields.Many2one('industry.theme.category', string='Business Category', required=True, tracking=True)
    palette_id = fields.Many2one('industry.theme.palette', string='Color Palette', required=True)
    layout_id = fields.Many2one('industry.theme.layout', string='Layout Styling', required=True)
    font_id = fields.Many2one('industry.theme.font', string='Typography Font', required=True)
    banner_ids = fields.Many2many('industry.theme.banner', string='Banners')
    block_ids = fields.Many2many('industry.theme.block', string='Reusable Blocks')
    preview_ids = fields.One2many('industry.theme.preview', 'theme_id', string='Previews')
    active = fields.Boolean(default=True, tracking=True)

    # Layout Selections
    header_layout = fields.Selection([
        ('default', 'Default Header'),
        ('centered', 'Centered Navigation'),
        ('transparent', 'Transparent overlay')
    ], string='Header Layout', default='default', required=True)

    footer_layout = fields.Selection([
        ('default', 'Default Simple'),
        ('multi_column', 'Multi-Column Directory'),
        ('dark', 'Minimalist Dark')
    ], string='Footer Layout', default='default', required=True)

    shop_layout = fields.Selection([
        ('default', 'Default Shop'),
        ('grid', 'Clean Product Grid'),
        ('sidebar', 'Grid with Sidebar Filters')
    ], string='Shop Layout', default='default', required=True)

    product_grid = fields.Selection([
        ('3_cols', '3 Columns Grid'),
        ('4_cols', '4 Columns Grid')
    ], string='Product Grid Scale', default='3_cols', required=True)

    product_card_style = fields.Selection([
        ('default', 'Default Card'),
        ('clean', 'Clean Borderless'),
        ('badge', 'Prominent Offer Badge'),
        ('hover_zoom', 'Hover Image Zoom')
    ], string='Product Card Style', default='default', required=True)

    category_card_style = fields.Selection([
        ('default', 'Default Box'),
        ('circular', 'Circular Cards'),
        ('square', 'Minimalist Squares')
    ], string='Category Card Style', default='default', required=True)

    blog_style = fields.Selection([
        ('default', 'Default list'),
        ('grid', 'Modern Editorial Grid'),
        ('masonry', 'Masonry Column list')
    ], string='Blog Style', default='default', required=True)

    newsletter_style = fields.Selection([
        ('default', 'Default Banner'),
        ('minimalist', 'Minimal Single Line'),
        ('card', 'Boxed Card newsletter')
    ], string='Newsletter Block Style', default='default', required=True)

    # Floating Features
    whatsapp_enabled = fields.Boolean(string='Floating WhatsApp Widget', default=True)
    whatsapp_number = fields.Char(string='WhatsApp Number', default='+1234567890')
    back_to_top_enabled = fields.Boolean(string='Back To Top Button', default=True)
    loading_animation_enabled = fields.Boolean(string='Loading Page Animation', default=True)
    hover_effects_style = fields.Selection([
        ('none', 'None'),
        ('lift', 'Lift Card on Hover'),
        ('scale', 'Subtle Scale'),
        ('glow', 'Soft Glow border')
    ], string='General Hover Effect', default='none', required=True)

    def action_duplicate(self):
        self.ensure_one()
        copied_theme = self.copy({
            'name': f"{self.name} (Copy)",
            'code': f"{self.code}_copy",
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'industry.theme',
            'view_mode': 'form',
            'res_id': copied_theme.id,
            'target': 'current',
        }

    def action_export_theme(self):
        self.ensure_one()
        data = {
            'name': self.name,
            'code': self.code,
            'category': self.category_id.name,
            'palette': {
                'name': self.palette_id.name,
                'primary_color': self.palette_id.primary_color,
                'secondary_color': self.palette_id.secondary_color,
                'accent_color': self.palette_id.accent_color,
                'bg_color': self.palette_id.bg_color,
            } if self.palette_id else None,
            'layout': {
                'name': self.layout_id.name,
                'border_radius': self.layout_id.border_radius,
                'button_style': self.layout_id.button_style,
                'card_style': self.layout_id.card_style,
                'shadow_style': self.layout_id.shadow_style,
                'animation_style': self.layout_id.animation_style,
                'spacing_scale': self.layout_id.spacing_scale,
            } if self.layout_id else None,
            'font': {
                'name': self.font_id.name,
                'font_family': self.font_id.font_family,
                'font_url': self.font_id.font_url,
            } if self.font_id else None,
            'header_layout': self.header_layout,
            'footer_layout': self.footer_layout,
            'shop_layout': self.shop_layout,
            'product_grid': self.product_grid,
            'product_card_style': self.product_card_style,
            'category_card_style': self.category_card_style,
            'blog_style': self.blog_style,
            'newsletter_style': self.newsletter_style,
            'whatsapp_enabled': self.whatsapp_enabled,
            'whatsapp_number': self.whatsapp_number,
            'back_to_top_enabled': self.back_to_top_enabled,
            'loading_animation_enabled': self.loading_animation_enabled,
            'hover_effects_style': self.hover_effects_style,
        }
        json_data = json.dumps(data, indent=4)
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.code}_theme_export.json",
            'type': 'binary',
            'datas': base64.b64encode(json_data.encode('utf-8')),
            'mimetype': 'application/json',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def action_reset(self):
        self.ensure_one()
        defaults = {
            'vegetables': {
                'primary_color': '#2E7D32',
                'secondary_color': '#81C784',
                'accent_color': '#FF9800',
                'bg_color': '#F1F8E9',
                'font_family': "'Outfit', sans-serif",
                'font_url': "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap",
                'border_radius': '12px',
                'shadow_style': '0 4px 12px rgba(46,125,50,0.15)',
            },
            'fashion': {
                'primary_color': '#111111',
                'secondary_color': '#8D6E63',
                'accent_color': '#D4AF37',
                'bg_color': '#FFFFFF',
                'font_family': "'Playfair Display', serif",
                'font_url': "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;600&display=swap",
                'border_radius': '0px',
                'shadow_style': 'none',
            },
            'manufacturing': {
                'primary_color': '#0D47A1',
                'secondary_color': '#546E7A',
                'accent_color': '#FFB300',
                'bg_color': '#ECEFF1',
                'font_family': "'Roboto', sans-serif",
                'font_url': "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
                'border_radius': '4px',
                'shadow_style': '0 2px 4px rgba(0,0,0,0.1)',
            },
            'restaurant': {
                'primary_color': '#BF360C',
                'secondary_color': '#3E2723',
                'accent_color': '#FFB300',
                'bg_color': '#FFF8E1',
                'font_family': "'Lora', serif",
                'font_url': "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Comfortaa:wght@400;600&display=swap",
                'border_radius': '16px',
                'shadow_style': '0 8px 24px rgba(191,54,12,0.15)',
            },
            'pharmacy': {
                'primary_color': '#00897B',
                'secondary_color': '#0288D1',
                'accent_color': '#E53935',
                'bg_color': '#E0F2F1',
                'font_family': "'Inter', sans-serif",
                'font_url': "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
                'border_radius': '8px',
                'shadow_style': '0 4px 10px rgba(0,137,123,0.1)',
            }
        }
        
        code = self.code
        if code in defaults:
            vals = defaults[code]
            if self.palette_id:
                self.palette_id.write({
                    'primary_color': vals['primary_color'],
                    'secondary_color': vals['secondary_color'],
                    'accent_color': vals['accent_color'],
                    'bg_color': vals['bg_color'],
                })
            if self.font_id:
                self.font_id.write({
                    'font_family': vals['font_family'],
                    'font_url': vals['font_url'],
                })
            if self.layout_id:
                self.layout_id.write({
                    'border_radius': vals['border_radius'],
                    'shadow_style': vals['shadow_style'],
                })
        return True
