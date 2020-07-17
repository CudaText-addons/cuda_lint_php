"""This module exports the PHP plugin class."""

from cuda_lint import Linter, util


class PHP(Linter):
    """Provides an interface to php -l."""

    syntax = ('PHP', 'PHP_')
    cmd = 'php -l -n -d display_errors=On -d log_errors=Off'
    regex = (
        r'^(?:Parse|Fatal) (?P<error>error):(\s*(?P<type>parse|syntax) error,?)?\s*'  # nopep8
        r'(?P<message>(?:unexpected \'(?P<near>[^\']+)\')?.*) in .+? on line (?P<line>\d+)')  # nopep8
    error_stream = util.STREAM_STDOUT

    def split_match(self, match):
        """Return the components of the error."""
        split_match = super(PHP, self).split_match(match)
        match, line, col, error, warning, message, near = split_match
        # message might be empty, we have to supply a value
        if match and match.group('type') == 'parse' and not message:
            message = 'parse error'

        return match, line, col, error, warning, message, near
