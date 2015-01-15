# regtemplate
Python class for parsing a template into a regex, used for matching into name-value pairs.

## Usage

See also examples in the examples folder.

### Basic usage example:
````
template = RegTemplate('some/dir')

# Parse a template from a file inside the base directory
template.parse_template_from_file('file_inside_some_dir.txt')

# Or parse from a string:
# template.parse('template string here')

# Match an output string against the template. Name/value pairs are returned.
pairs = template.match('some output text')

# Match all. If the regex matches several times, return a list of list of pairs:
list_of_pairs = template.match_all('some output text some output text')
````

### Example of a template:
````
Displaying numbers from index {{ index_name|word }}
Number of interesting events: {{ num_events|digits }}
Number of pages: {{ num_pages|digits }}
````

### Adding custom rules:
````
template.rules['digits'] = '\d+'

# Default rule if no rule is given in the template
template.rule_dflt = '\S+'
````

### Ignoring whitespace (on by default):
````
template.ignore_whitespace = True
````

### Setting custom variable tags:
````
template.var_start = '{{'
template.var_end = '}}'
````