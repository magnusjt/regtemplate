from regtemplate.regtemplate import RegTemplate

template = RegTemplate()

template.parse_template(r"""
Displaying numbers from index {{ index_name|word }}
Number of interesting events: {{ num_events|digits }}
Number of pages: {{ num_pages|digits }}
""")

matches = template.match(r"""
Displaying numbers from index SuperIndex
Number of interesting events: 45678
Number of pages: 9876
""")

print matches