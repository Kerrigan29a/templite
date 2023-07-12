# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
It provide all the functionality.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.4.1"
__license__ = "BSD 3-Clause Clear License"

import argparse
import os
import re
from builtins import compile as _compile
import sys
from contextlib import contextmanager


DELIMITERS = ('{%', '%}', '{{', '}}', '{#', '#}')
ENCODING = 'utf-8'
INDENT = ' ' * 4

_RSTRIP_PREV = object()
_LSTRIP_NEXT = object()


def compile(src, name=None, encoding=ENCODING, delimiters=DELIMITERS, tmpcode=None):
    """Compiles a template into a function."""
    
    if hasattr(src, 'read'):
        src = src.read()

    begs, ends, bege, ende, begc, endc = delimiters
    beg_pattern = rf'{begs}|{bege}|{begc}'
    end_pattern = rf'{ends}|{ende}|{endc}'
    depth = 0
    code = [f'# -*- coding: {encoding} -*-']

    def split(src):
        i = 0
        for m in re.finditer(fr'({beg_pattern})(.*?)({end_pattern})', src, flags=re.DOTALL):
            yield True, "", src[i:m.start()], ""
            yield False, m.group(1), m.group(2), m.group(3)
            i = m.end()
        yield True, "", src[i:], ""

    def push(line):
        code.append(INDENT * depth + line)
    
    # Replace escaped delimiters
    src = src.replace(f'\\{begs}', "\\".join(begs))
    src = src.replace(f'\\{ends}', "\\".join(ends))
    src = src.replace(f'\\{bege}', "\\".join(bege))
    src = src.replace(f'\\{ende}', "\\".join(ende))
    src = src.replace(f'\\{begc}', "\\".join(begc))
    src = src.replace(f'\\{endc}', "\\".join(endc))
    

    # Process blocks
    for is_data, beg, block, end in split(src):
        # Replace escaped delimiters
        block = block.replace("\\".join(begs), begs)
        block = block.replace("\\".join(ends), ends)
        block = block.replace("\\".join(bege), bege)
        block = block.replace("\\".join(ende), ende)
        block = block.replace("\\".join(begc), begc)
        block = block.replace("\\".join(endc), endc)

        # Process data blocks
        if is_data:
            if not block:
                continue
            push(f'write(r"""{block}""")')
        
        # Process code blocks
        else:            
            # Discard comments
            if beg[-1] == '#':
                if end[0] != '#':
                    raise SyntaxError(f"Unclosed comment block: {beg}{block}{end}")
                continue
                        
            strip_prev, strip_next, block = _strip_minus(block)

            # Discard empty blocks
            if not block.strip():
                continue

            # Handle strip prev
            if strip_prev:
                push("_rstrip_prev()")

            # Handle block
            if beg[-1] == '{':
                if end[0] != '}':
                    raise SyntaxError(f"Unclosed expression block: {beg}{block}{end}")
                push(f'write({block.strip()})')
            elif beg[-1] == '%':
                if end[0] != '%':
                    raise SyntaxError(f"Unclosed statement block: {beg}{block}{end}")
                
                # Handle depth decrease
                if block.lstrip().startswith(':'):
                    if depth == 0:
                        raise SyntaxError(f"Unexpected indentation: {beg}{block}{end}")
                    depth -= 1
                    block = block.lstrip()[1:]
                    # Skip closing colon
                    if not block.rstrip().endswith(':'):

                        # Handle strip next
                        if strip_next:
                            push("_lstrip_next()")

                        continue

                lines = block.splitlines()
                prefix = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
                for line in lines:
                    push(line[prefix:])
                
                # Handle depth increase
                if block.rstrip().endswith(':'):
                    depth += 1
            else:
                raise SyntaxError(f"Unknown block type: {beg}{block}{end}")
            
            # Handle strip next
            if strip_next:
                push("_lstrip_next()")
        
    # Compile code
    code = "\n".join(code)
    if tmpcode is not None:
        tmpcode.write(code)
    file = name or "<string>"
    code = _compile(code, file, 'exec')
    
    # Render function
    def render(**external_ns):
        """Renders the template."""
        buffer = []
        if name is not None:
            cwd = os.path.dirname(name)
        else:
            cwd = os.getcwd()

        def write(s):
            buffer.append(str(s))
        
        def _rstrip_prev():
            buffer.append(_RSTRIP_PREV)
        
        def _lstrip_next():
            buffer.append(_LSTRIP_NEXT)

        def relpath(path):
            if os.path.isabs(path):
                return os.path.relpath(path, cwd)
            return path
        
        def abspath(path):
            if os.path.isabs(path):
                return path
            return os.path.join(cwd, path)
    
        def include(path):
            with open(abspath(path), encoding=encoding) as f:
                render = compile(f, name=relpath(path), delimiters=delimiters, encoding=encoding)
                buffer.append(render(**external_ns))
        
        internal_ns = {
            'write': write,
            '_rstrip_prev': _rstrip_prev,
            '_lstrip_next': _lstrip_next,
            'relpath': relpath,
            'abspath': abspath,
            'include': include,
            '__cwd__': cwd,
            '__file__': file,
        }

        # Inject external
        for k, v in external_ns.items():
            external_ns[k] = v({**external_ns, **internal_ns})
        
        # Execute code
        exec(code, {**external_ns, **internal_ns})

        # Strip chunks
        chunks = []
        lstrip = False
        for chunk in buffer:
            if chunk is _RSTRIP_PREV:
                prev = chunks.pop().rstrip()
                if prev:
                    chunks.append(prev)
            elif chunk is _LSTRIP_NEXT:
                lstrip = True
            elif lstrip:
                chunk = chunk.lstrip()
                if chunk:
                    chunks.append(chunk)
                lstrip = False
            else:
                chunks.append(chunk)
        return "".join(chunks)
    
    return render


def _strip_minus(block):
    """ Strips the minus sign from the beginning and end of a block.

    ```python
    >>> _strip_minus('- abc -')
    (True, True, ' abc ')
    >>> _strip_minus('- abc')
    (True, False, ' abc')
    >>> _strip_minus('abc -')
    (False, True, 'abc ')

    >>> _strip_minus('-  abc  -')
    (True, True, '  abc  ')
    >>> _strip_minus('-  abc')
    (True, False, '  abc')
    >>> _strip_minus('abc  -')
    (False, True, 'abc  ')
    ```

    Is mandatory to have a space around the minus sign.

    ```python
    >>> _strip_minus('-3')
    (False, False, '-3')
    >>> _strip_minus('3-')
    (False, False, '3-')
    >>> _strip_minus('- -3 -')
    (True, True, ' -3 ')
    >>> _strip_minus('- -3')
    (True, False, ' -3')
    >>> _strip_minus('-3 -')
    (False, True, '-3 ')
    ```
    """
    strip_prev = strip_next = False
    if re.search(r'^-\s+', block):
        block = block[1:]
        strip_prev = True
    if re.search(r'\s+-$', block):
        block = block[:-1]
        strip_next = True
    return strip_prev, strip_next, block

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
    parser.add_argument("-c", "--code", metavar="FILE",
                        help="Write the generated code in this file.")
    args = parser.parse_args()
    args.__dict__["define"] = dict(definition.split("=") for definition in args.define)if args.define else {}
    return args


@contextmanager
def try_open(file_name, mode, encoding, default=None):
    if file_name:
        with open(file_name, mode=mode, encoding=encoding) as f:
            yield f, file_name
    else:
        yield default, None


def run(args):
    with try_open(args.input, "r", args.encoding, sys.stdin) as (f, filename), \
            try_open(args.code, "w", args.encoding) as (tmpcode, _):
        render = compile(f, name=filename, encoding=args.encoding, tmpcode=tmpcode)
        txt = render(**args.define)
    with try_open(args.output, "w", args.encoding, sys.stdout) as (f, _):
        f.write(txt)


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
