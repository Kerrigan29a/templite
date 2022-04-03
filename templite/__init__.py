# Copyright (c) 2022 Javier Escalada Gómez
# All rights reserved.
#
# Based on Templite+ by Thimo Kraemer <thimo.kraemer@joonis.de>
# Copyright (c) 2009 joonis new media
# From: http://www.joonis.de/de/code/templite
#
# Based on Templite by Tomer Filiba
# From: http://code.activestate.com/recipes/496702/
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import re
import argparse


__version__ = '0.0.1'


class Templite(object):
    
    autowrite = re.compile('(^[\'\"])|(^[a-zA-Z0-9_\[\]\'\"]+$)')
    delimiters = ('{%', '%}')
    cache = {}

    def __init__(self, text=None, filename=None, encoding='utf-8',
            delimiters=None, caching=False, generated_code=None):
        """Loads a template from string or file."""
        
        # Set defaults
        if filename:
            filename = os.path.abspath(filename)
            mtime = os.path.getmtime(filename)
            self.file = key = filename
        elif text is not None:
            self.file = mtime = None
            key = hash(text)
        else:
            raise ValueError('either text or filename required')
        
        # Set attributes
        self.encoding = encoding
        self.caching = caching
        self.generated_code = generated_code
        if delimiters:
            start, end = delimiters
            if len(start) != 2 or len(end) != 2:
                raise ValueError('each delimiter must be two characters long')
            self.delimiters = delimiters

        # Check cache
        cache = self.cache
        if caching and key in cache and cache[key][0] == mtime:
            self._code = cache[key][1]
            return

        # Compile code
        if text is None:
            with open(filename, "r", encoding=encoding) as fh:
                text = fh.read()
        self._code = self._compile(text)
        if caching:
            cache[key] = (mtime, self._code)
    
    def _compile(self, source):
        offset = 0
        tokens = ['# -*- coding: %s -*-' % self.encoding]
        start, end = self.delimiters
        escaped = (re.escape(start), re.escape(end))
        code_regex = re.compile('%s(.*?)%s' % escaped, re.DOTALL)
        skip_newline_regex = re.compile(r'\\(\r\n|\r|\n)[ \t]*')

        for i, part in enumerate(code_regex.split(source)):
            part = part.replace('\\'.join(start), start)
            part = part.replace('\\'.join(end), end)
            if i % 2 == 0:
                if not part:
                    continue
                part = skip_newline_regex.sub("", part)
                part = part.replace('\\', '\\\\').replace('"', '\\"')
                part = '\t' * offset + 'write("""%s""")' % part
            else:
                original_part = str(part)
                part = part.rstrip()
                if not part:
                    continue
                part_stripped = part.lstrip()
                if part_stripped.startswith(':'):
                    if not offset:
                        raise SyntaxError('no block statement to terminate: %s%s%s' % (
                            self.delimiters[0], original_part, self.delimiters[1]))
                    offset -= 1
                    part = part_stripped[1:]
                    if not part.endswith(':'):
                        continue
                elif self.autowrite.match(part_stripped):
                    part = 'write(%s)' % part_stripped
                lines = part.splitlines()
                margin = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
                part = '\n'.join('\t' * offset + l[margin:] for l in lines)
                if part.endswith(':'):
                    offset += 1
            tokens.append(part)
        if offset:
            raise SyntaxError('%i block statement(s) not terminated' % offset)
        
        generated_code = '\n'.join(tokens)
        if self.generated_code is not None:
            print(generated_code, file=self.generated_code)
        return compile(generated_code, '<generated code>', 'exec')

    def render(self, **namespace):
        """Renders the template according to the given namespace."""
        stack = []
        namespace['__file__'] = self.file

        if self.file:
            base = os.path.dirname(self.file)
        else:
            base = os.path.dirname(sys.argv[0])
        
        # add relpath method
        def relpath(file):
            if os.path.isabs(file):
                return os.path.relpath(file, base)
            return file
        namespace['relpath'] = relpath

        # add abspath method
        def abspath(file):
            if os.path.isabs(file):
                return file
            return os.path.join(base, file)
        namespace['abspath'] = abspath

        # add write method
        def write(*args):
            for value in args:
                stack.append(str(value))
        namespace['write'] = write

        # add include method
        def include(file):
            stack.append(Templite(None, abspath(file), self.encoding,
                    self.delimiters,self.caching, self.generated_code)
                .render(**namespace))
        namespace['include'] = include
        
        # execute template code
        exec(self._code, namespace)
        return "".join(stack)


def parse_args():
    parser = argparse.ArgumentParser(description='A light-weight, fully functional, general purpose templating engine')
    parser.add_argument("-i", "--input", metavar="FILE",
                        help="Read template from this file. The default value is stdin")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Write the generated text in this file. The default value is stdout")
    parser.add_argument("-e", "--encoding", metavar='ENCODING', default="utf-8",
                        help="Encoding (default: %(default)s)")
    parser.add_argument("-D", "--define", metavar="STRING", action="append",
                        help="Argument passed to the template engine. The format must follow the following syntax '<VAR>=<VALUE>'")
    args = parser.parse_args()
    if args.define:
        args.__dict__["define"] = dict(definition.split("=") for definition in args.define)
    return args


def run(args):
    # Read template
    if args.input:
        with open(args.input, "r", encoding=args.encoding) as f:
            text = f.read()
        filename=args.input
    else:
        text = sys.stdin.read()
        filename=None

    t = Templite(text, filename, args.encoding)

    # Run template
    if args.define:
        txt = t.render(**args.define)
    else:
        txt = t.render()

    # Write generated text
    if args.output:
        with open(args.output, "w") as f:
            f.write(txt)
    else:
        sys.stdout.write(txt)
        
    return 0


def main():
    try:
        exit(run(parse_args()))
    except Exception as e:
        import traceback
        print(f"ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
    exit(1)

if __name__ == "__main__":
    main()
