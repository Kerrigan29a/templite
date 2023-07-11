A light-weight, fully functional, general purpose template-ing engine.

# The syntax

A template is just a text file where delimited blocks of Python code are evaluated.

There are three types of blocks:

* `{{` and `}}` delimit expression blocks.
  The expression is evaluated and the string representation of the result is written to the output.

  ```python
  >>> render = compile("The result is {{ 1 + 1 }}")
  >>> render()
  'The result is 2'
  ```
  
* `{%` and `%}` delimit statement blocks.
  The statement is executed.

  ```python
  >>> render = compile("Hi {% if True: %} good {% :end %} world!")
  >>> render()
  'Hi  good  world!'
  ```

* `{#` and `#}` delimit comment blocks.
  The comment is ignored.

  ```python
  >>> render = compile("Hi {# This is a comment #} world!")
  >>> render()
  'Hi  world!'
  ```

If you want to use the delimiters in the output, you can escape them with a backslash.

```python
>>> render = compile(r"This is not an expression block: \{{ \}}")
>>> render()
'This is not an expression block: {{ }}'
>>> render = compile(r"This is not a statement block: \{% \%}")
>>> render()
'This is not a statement block: {% %}'
>>> render = compile(r"This is not a comment block: \{# \#}")
>>> render()
'This is not a comment block: {# #}'
```

## Spacing

By default, all text between code blocks is copied verbatim to the output.
However most of the time, you will want to strip the whitespace before and after the code block.
Those spaces are there to make the template more readable, but you don't want them in the output.
In order to strip the whitespace, you can add a `-` and a whitespace to the delimiters.

In this example the whitespace before and after the expression block are unwanted.

```python
>>> render = render = compile("Hi {% if True: %} good {% :end %} world!")
>>> render()
'Hi  good  world!'
```

To strip the preceding whitespace, add `- ` to the beginning of the first delimiter.

```python
>>> render = compile("Hi {%- if True: %} good {% :end %} world!")
>>> render()
'Hi good  world!'
```

To strip the trailing whitespace, add ` -` to the end of the last delimiter.

```python
>>> render = compile("Hi {%- if True: %} good {% :end -%} world!")
>>> render()
'Hi good world!'
```

Alternatively, you can strip the whitespaces surrounding `good`.

```python
>>> render = compile("Hi {% if True: -%} good {%- :end %} world!")
>>> render()
'Hi good world!'
```

But if you strip them all, you will get something unexpected.

```python
>>> render = compile("Hi {%- if True: -%} good {%- :end -%} world!")
>>> render()
'Higoodworld!'
```

**REMEMBER:** Don't forget the space surrounding the `-`.

```python
>>> render = compile("Result: {{- 3}}")
>>> render()
'Result:3'
>>> render = compile("Result: {{-3}}")
>>> render()
'Result: -3'
```

## Statements and indentation

As you know, Python uses indentation to delimit regions of code.

    statement 1 outside if
    if condition:
        # This indentation is relevant
        statement 1 inside then
    else:
        statement 1 inside else
    statement 2 outside if

However, in templite, the indentation outside of code blocks is treated as data,
so, you cannot use indentation to declare the end of a region of code.
To solve this problem, templite provides a way to declare the end.

    {% statement 1 outside if %}
    {% if condition: %}
        {# This indentation is irrelevant #}
        {% statement 1 inside then %}
    {% :else: %}
        {% statement 1 inside else %}
    {% :end %}

In templite, the colons (`:`) are used to declare the beginning and end of a code region.

1. If the statement ends with a colon, the following lines are indented.
   Like in `if` or `for` statements.
2. If the statement starts and ends with a colon, the current line is unindented but the following lines are indented again.
   Like in `else` or `elif` statements.
3. If the statement starts (but not ends) with a colon, the current line is unindented.
   One additional thing to note is that the text after the colon is ignored.
   This is used to declare the end of a code region.
   In the example above, we use `:end`, but you can use any text you want, like `:endif`, `:fi` or even `:`.

## Built-ins

You can use the following variables and functions in your templates:

* `__file__`: The name of the template being compiled or `<string>`.
* `__cwd__`: The directory where the template is located if `__file__` is not `<string>`.
   Otherwise, the current working directory.
* `write(obj)`: Writes the string representation of `obj` to the output.
* `include(name)`: Includes another template.
* `relpath(path)`: Returns the `path` relative to `__cwd__`.
* `abspath(path)`: Returns the absolute path of `path` relative to `__cwd__`.

## Adding extra functions

You can add more functions to the templates by passing them to the `render` function.

~~~python
>>> def decorate(namespace):
...     def f(name):
...         return f"Mr. {name}"
...     return f
...
>>> render = compile(r"Hello {{ decorate('John') }}")
>>> render(decorate=decorate)
'Hello Mr. John'
~~~

# Usage
~~~
usage: __main__.py [-h] [-i FILE] [-o FILE] [-e ENCODING] [-D STRING]
                   [-c FILE]

A light-weight, fully functional, general purpose templating engine

options:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        Read template from this file. The default value is
                        stdin
  -o FILE, --output FILE
                        Write the generated text in this file. The default
                        value is stdout
  -e ENCODING, --encoding ENCODING
                        Encoding (default: utf-8)
  -D STRING, --define STRING
                        Argument passed to the template engine. The format
                        must follow the following syntax '<VAR>=<VALUE>'
  -c FILE, --code FILE  Write the generated code in this file.
~~~
# Package documentation
## Module [\_\_init\_\_](https://github.com/kerrigan29a/templite/blob/main/templite/__init__.py#L1)
It provide all the functionality.

### Function [\_\_init\_\_.compile](https://github.com/kerrigan29a/templite/blob/main/templite/__init__.py#L32)
```python
def compile(src, name=None, encoding=ENCODING, delimiters=DELIMITERS, tmpcode=None): ...
```
Compiles a template into a function.

#### Function [\_\_init\_\_.compile.render](https://github.com/kerrigan29a/templite/blob/main/templite/__init__.py#L145)
```python
def render(**external_ns): ...
```
Renders the template.

### Function [\_\_init\_\_.\_strip\_minus](https://github.com/kerrigan29a/templite/blob/main/templite/__init__.py#L217)
```python
def _strip_minus(block): ...
```
Strips the minus sign from the beginning and end of a block.

```python
>>> _strip_minus('- abc -')
(True, True, ' abc ')
>>> _strip_minus('- abc')
(True, False, ' abc')
>>> _strip_minus('abc -')
(False, True, 'abc ')
```

```python
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



## Module [\_\_main\_\_](https://github.com/kerrigan29a/templite/blob/main/templite/__main__.py#L1)
This is the entry point of the templite package.
It allows to call the templite compiler from the command line.



<!-- references -->
[__init__]: #module-__init__ "Module __init__"
[`__init__`]: #module-__init__ "Module __init__"
[__init__.compile]: #function-__init__-compile "Function compile"
[`__init__.compile`]: #function-__init__-compile "Function compile"
[__init__.compile.split]: #function-__init__-compile-split "Function split"
[`__init__.compile.split`]: #function-__init__-compile-split "Function split"
[__init__.compile.push]: #function-__init__-compile-push "Function push"
[`__init__.compile.push`]: #function-__init__-compile-push "Function push"
[__init__.compile.render]: #function-__init__-compile-render "Function render"
[`__init__.compile.render`]: #function-__init__-compile-render "Function render"
[__init__.compile.render.write]: #function-__init__-compile-render-write "Function write"
[`__init__.compile.render.write`]: #function-__init__-compile-render-write "Function write"
[__init__.compile.render._rstrip_prev]: #function-__init__-compile-render-_rstrip_prev "Function _rstrip_prev"
[`__init__.compile.render._rstrip_prev`]: #function-__init__-compile-render-_rstrip_prev "Function _rstrip_prev"
[__init__.compile.render._lstrip_next]: #function-__init__-compile-render-_lstrip_next "Function _lstrip_next"
[`__init__.compile.render._lstrip_next`]: #function-__init__-compile-render-_lstrip_next "Function _lstrip_next"
[__init__.compile.render.relpath]: #function-__init__-compile-render-relpath "Function relpath"
[`__init__.compile.render.relpath`]: #function-__init__-compile-render-relpath "Function relpath"
[__init__.compile.render.abspath]: #function-__init__-compile-render-abspath "Function abspath"
[`__init__.compile.render.abspath`]: #function-__init__-compile-render-abspath "Function abspath"
[__init__.compile.render.include]: #function-__init__-compile-render-include "Function include"
[`__init__.compile.render.include`]: #function-__init__-compile-render-include "Function include"
[__init__._strip_minus]: #function-__init__-_strip_minus "Function _strip_minus"
[`__init__._strip_minus`]: #function-__init__-_strip_minus "Function _strip_minus"
[__init__.parse_args]: #function-__init__-parse_args "Function parse_args"
[`__init__.parse_args`]: #function-__init__-parse_args "Function parse_args"
[__init__.try_open]: #function-__init__-try_open "Function try_open"
[`__init__.try_open`]: #function-__init__-try_open "Function try_open"
[__init__.run]: #function-__init__-run "Function run"
[`__init__.run`]: #function-__init__-run "Function run"
[__init__.main]: #function-__init__-main "Function main"
[`__init__.main`]: #function-__init__-main "Function main"
[__main__]: #module-__main__ "Module __main__"
[`__main__`]: #module-__main__ "Module __main__"
[tests]: #module-tests "Module tests"
[`tests`]: #module-tests "Module tests"
[tests.MarkdownTestParser]: #class-tests-markdowntestparser "Class MarkdownTestParser"
[`tests.MarkdownTestParser`]: #class-tests-markdowntestparser "Class MarkdownTestParser"
[tests.MarkdownTestParser.parse]: #function-tests-markdowntestparser-parse "Function parse"
[`tests.MarkdownTestParser.parse`]: #function-tests-markdowntestparser-parse "Function parse"
[tests.load_tests]: #function-tests-load_tests "Function load_tests"
[`tests.load_tests`]: #function-tests-load_tests "Function load_tests"
