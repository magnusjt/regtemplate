from regtemplate.regtemplate import RegTemplate

template = RegTemplate()

template.parse_template(r"""
Card {{ card_name }}: {{ cpu|float }}%
""")

matches = template.match_all(r"""
--- CPU Table ---
Card 1-1: 45.6%
Card 1-2: 43.6%
Card 2-1: 13.56%
Card 2-2: 99.0%
""")

print matches