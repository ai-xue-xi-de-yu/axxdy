{
    'name': "warehouse",

    'summary': """
        仓库管理""",

    'description': """
        物料的入库归还
        """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/groups_category.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'views/warehouse_views.xml',
        'views/warehouse_menus.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/tree_button.xml',
    ]
}
# -*- coding: utf-8 -*-
