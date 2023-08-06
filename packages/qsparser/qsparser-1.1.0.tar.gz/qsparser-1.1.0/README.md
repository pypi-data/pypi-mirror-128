qsparser
===========
Query string parser with nested structure supported.

## Usage

### Stringify

```python
from qsparser import stringify

# simple object
stringify({'a': '5', 'b': 'c'}) # a=5&b=c

# nested object
stringify({'a': {'b': 'c'},'d': {'e': 'f'}}) # a[b]=c&d[e]=f
```

### Parse

```python
from qsparser import parse

# simple string
parse('a=5&b=c') # {'a': '5', 'b': 'c'}

# multiple string
parse('a[b]=c&d[e]=f') # {'a': {'b': 'c'},'d': {'e': 'f'}}
```

### Installation

```sh
pip install qsparser
```

### Changelog

#### 1.1.0
* Rigid rules on string with null representing content.
* Use private function names.

### Author

`qsparser` is authored by Victor Teo and Chun Tse.

### License

MIT License

Copyright (c) 2021 Fillmula Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
