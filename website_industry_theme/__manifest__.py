# -*- coding: utf-8 -*-
{
    'name': 'Intelligent Industry Theme Engine',
    'version': '19.0.1.0.0',
    'category': 'Website/Theme',
    'summary': 'Modular, dynamic industry-specific theme engine for Odoo Website',
    'description': """
        An intelligent Odoo 19 Website Theme Engine that switches typography, layouts,
        colors, blocks, and snippets based on the selected industry category.
        
        Includes live Desktop/Tablet/Mobile previews, smart theme recommendations based on product catalog,
        and custom theme-specific snippets.
    """,
    'author': 'Antigravity',
    'website': 'https://www.google.com',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/theme_import_wizard_views.xml',
        'views/industry_theme_views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
        'views/snippets.xml',
        'data/industry_theme_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_industry_theme/static/src/scss/theme_base.scss',
            '/website_industry_theme/static/src/js/frontend_actions.js',
        ],
        'web.assets_backend': [
            '/website_industry_theme/static/src/js/theme_settings_action.js',
            '/website_industry_theme/static/src/xml/theme_settings_action.xml',
        ],
        # Dynamic theme-specific asset bundles called on demand
        'website_industry_theme.theme_vegetables': [
            '/website_industry_theme/static/src/scss/themes/theme_vegetables.scss',
        ],
        'website_industry_theme.theme_fashion': [
            '/website_industry_theme/static/src/scss/themes/theme_fashion.scss',
        ],
        'website_industry_theme.theme_manufacturing': [
            '/website_industry_theme/static/src/scss/themes/theme_manufacturing.scss',
        ],
        'website_industry_theme.theme_restaurant': [
            '/website_industry_theme/static/src/scss/themes/theme_restaurant.scss',
        ],
        'website_industry_theme.theme_pharmacy': [
            '/website_industry_theme/static/src/scss/themes/theme_pharmacy.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
