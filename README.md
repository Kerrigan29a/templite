# Templite

A light-weight, fully functional, general purpose templating engine.

# Example

``` python
from templite import Templite

template = r"""
This template demonstrates the usage of Templite.

Within the defined delimiters we can write pure Python code:
{%
    def say_hello(name):
        write('Hello %s!' % name)
%}
And now we call the function: {% say_hello('World') %}

Escaped starting delimiter: {\%
{% write('Escaped ending delimiter: %\}') %}
{% # this is a python comment %}

Also block statements are possible:
{% if x > 10: %}
x is greater than 10
{% :elif x > 5: %}
x is greater than 5
{% :else: %}
x is not greater than 5
{% :end-if / only the starting colon is essential to close a block %}
{% for i in range(x): %}
loop index is {% i %}
{% :end-for %}

As you can see the previous text is generating too much line-breaks. To avoid
this, you can skip them adding '\' at the end of the line. In general is a good
practice to skip line-breaks after control-flow statements. Like in the following example:

{% if x > 10: %}{% # skipped linebreak  %}\
x is greater than 10
{% :elif x > 5: %}{% # skipped linebreak  %}\
x is greater than 5
{% :else: %}{% # skipped linebreak  %}\
x is not greater than 5
{% :fi (it doesn't matter what you write here) %}
{% for i in range(x): %}{% # skipped linebreak  %}\
loop index is {% i %}
{% :rof >>>-(@_@)--> %}{% # skipped linebreak  %}\

Single variables and expressions starting with quotes are substituted
automatically:
Instead of {% write(x) %} you can write {% x %} or {% '%s' % x %} or {% "", x %}
You can also use prefixed strings: {% r"hi" %} or {% f"hi" %}
or {% fr"hi" %} or {% rf"hi" %}
Therefore standalone statements like break, continue or pass
must be enclosed by a semicolon: {\%continue;%\}

{% for i in range(x): %}\
{% if i > 2: %}\
{% break; %}\
{% : %}\
loop index is {% i %}
{% : %}\

To include another template, just call "include":
{% include('template.txt') %}

You can also use {% __file__ %} when calling Template with the filename
argument. Otherwise is None.

Finally, you can call "relpath" and "abspath" to get the relative and absolute
path of a file based on the parent directory of:
- the template file, when Templite is used with a file
- or the called script, when Templite is used with a string
"""
print(Templite(template).render(x=8))
```

This script generates the following output:

```
This template demonstrates the usage of Templite.

Within the defined delimiters we can write pure Python code:

And now we call the function: Hello World!

Escaped starting delimiter: {%
Escaped ending delimiter: %}


Also block statements are possible:

x is greater than 5


loop index is 0

loop index is 1

loop index is 2

loop index is 3

loop index is 4

loop index is 5

loop index is 6

loop index is 7


As you can see the previous text is generating too much line-breaks. To avoid
this, you can skip them adding '\' at the end of the line. In general is a good
practice to skip line-breaks after control-flow statements. Like in the following example:

x is greater than 5

loop index is 0
loop index is 1
loop index is 2
loop index is 3
loop index is 4
loop index is 5
loop index is 6
loop index is 7

Single variables and expressions starting with quotes are substituted
automatically:
Instead of 8 you can write 8 or 8 or 8
You can also use prefixed strings: hi or hi
or hi or hi
Therefore standalone statements like break, continue or pass
must be enclosed by a semicolon: {%continue;%}

loop index is 0
loop index is 1
loop index is 2

To include another template, just call "include":
This is the content of template.txt


You can also use None when calling Template with the filename
argument. Otherwise is None.

Finally, you can call "relpath" and "abspath" to get the relative and absolute
path of a file based on the parent directory of:
- the template file, when Templite is used with a file
- or the called script, when Templite is used with a string
```
