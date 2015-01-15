class RegTemplate:
    def __init__(self, base_dir=None):
        self.base_dir  = base_dir
        self.var_start = '{{'
        self.var_end   = '}}'
        self.ignore_whitespace = True
        self.rule_dflt = '\S+'
        self.rules     = {
            'digits': '\d+',
            'word':   '\w+'
        }
        self._pos       = 0
        self._template  = ''
        self._reg       = ''
        self._compiled  = None
        """ :type : RegexObject """
        self._names     = []

    def parse_template_from_file(self, filename):
        with open(self.base_dir + '/' + filename) as f:
            self.parse_template(f.read())

    def parse_template(self, template):
        """
        :type template: str
        """
        self._template = template
        self._reg      = ''
        self._compiled = None
        self._names    = []
        self._pos      = 0

        if self.ignore_whitespace:
            self._template = self._template.strip()

        var_matches = re.finditer(re.escape(self.var_start), self._template)
        for var_match in var_matches:
            self._add_raw(self._template[self._pos:var_match.start()])
            self._pos = var_match.end()
            self._parse_var()

        if self._pos < len(self._template):
            self._add_raw(self._template[self._pos:len(self._template)-1])
        self._compiled = re.compile(self._reg)

    def match(self, string):
        if self.ignore_whitespace:
            string = string.strip()
            string = re.sub(r'\s+', ' ', string)

        matches = self._compiled.search(string)

        if not matches:
            return False

        result = {}
        for match,name in izip(matches.groups(), self._names):
            result[name] = match

        return result

    def match_all(self, string):
        if self.ignore_whitespace:
            string = string.strip()
            string = re.sub(r'\s+', ' ', string)

        matches = self._compiled.findall(string)

        result = []
        for match_list in matches:
            d = {}
            for match,name in izip(match_list, self._names):
                d[name] = match
            result.append(d)
        return result

    def _add_raw(self, raw):
        if self.ignore_whitespace:
            raw = re.sub(r'\s+', ' ', raw)
        self._reg += re.escape(raw)

    def _parse_var(self):
        m = re.compile(r'\s*(\w+)\s*').match(self._template, self._pos)
        if m:
            self._names.append(m.group(1))
            self._pos = m.end()
        else:
            raise Exception('Expected variable name, but got something else around: ' + str(self._pos))

        m = re.compile(r'\|\s*(\w+)\s*').match(self._template, self._pos)
        if m:
            rule = m.group(1)
            if not self.rules.has_key(rule):
                raise Exception('Unknown rule: ' + rule)

            self._reg += '(' + self.rules[m.group(1)] + ')'
            self._pos = m.end()
        else:
            self._reg += '(' + self.rule_dflt + ')'

        m = re.compile(re.escape(self.var_end)).match(self._template, self._pos)
        if m:
            self._pos = m.end()
        else:
            raise Exception('Expected end-of-variable token, but got something else')