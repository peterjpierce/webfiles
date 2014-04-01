PATTERNS = [
        {
            'regex': '^Makefile_(20\d{6})',
            'display_name': 'Our uber doober Make file',
            'strptime_pattern': '%Y%m%d',
            'date_regex_group': 1,
        },
        {
            'regex': '^neonova_viasat_accounts_(20\d{6})\.(\d+)\..*',
            'display_name': 'Active Accounts',
            'strptime_pattern': '%Y%m%d',
            'date_regex_group': 1,
            'revision_group': 2,
        },
        {
            'regex': '^LICENSE_(20\d{6})\.(\d+)\..*',
            'display_name': 'Monthly Churn Summary',
            'strptime_pattern': '%Y%m%d',
            'date_regex_group': 1,
            'revision_group': 2,
        },
]
