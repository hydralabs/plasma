# Copyright (c) The Plasma Project.
# See LICENSE.txt for details.

"""
This module contains pattern matching code for the LIKE expression.
"""

_TOKEN_ANYCHAR = 1     # match any single character
_TOKEN_ANYRANGE = 2    # match any number of characters

class Matcher(object):
    def __init__(self, source, pattern, escapechar):
        self.srcpos = 0
        self.srclen = len(source)
        self.patternpos = 0
        self.patternlen = len(pattern)
        self.source = source
        self.pattern = pattern
        self.escapechar = escapechar

    def nexttoken(self):
        escape = False
        buffer = u''
        while self.patternpos < self.patternlen:
            char = self.pattern[self.patternpos]
            if char in (u'_', u'%'):
                if not escape:
                    if buffer:
                        return buffer
                    self.patternpos += 1
                    if char == u'_':
                        return _TOKEN_ANYCHAR
                    return _TOKEN_ANYRANGE
                escape = False

            # Insert escape character if nothing was escaped
            if escape:
                buffer += self.escapechar
                escape = False

            if char == self.escapechar:
                escape = True
            else:
                buffer += char
            self.patternpos += 1

        # Insert escape character if nothing was escaped
        if escape:
            buffer += self.escapechar

        return buffer

    def matches(self):
        """
        Matches `source` against `pattern`.

        :return: `True` if all of `source` matched the `pattern`,
                 `False` otherwise
        """
        token = self.nexttoken()
        while token and self.srcpos <= self.srclen:
            if token == _TOKEN_ANYCHAR:
                # Match any character
                self.srcpos += 1
                token = self.nexttoken()
            elif token == _TOKEN_ANYRANGE:
                token = self.nexttoken()
                if not token:
                    # Anything that is left in the source is matched
                    return True
                elif isinstance(token, basestring):
                    # Match everything up to the next segment of text
                    pos = self.source.find(token, self.srcpos)
                    if pos == -1:
                        return False
                    self.srcpos += (pos - self.srcpos)
            else:
                # Got a text segment -- match it exactly with the source
                length = len(token)
                if self.source[self.srcpos:self.srcpos + length] != token:
                    return False
                self.srcpos += length
                token = self.nexttoken()

        return self.srcpos == self.srclen
