# functionwords
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](
https://creativecommons.org/licenses/by-nc-sa/4.0/)

The `functionwords` package aims at providing **curated** Chinese and English function words.

For now, it supports four function word lists: modern Chinese ([`chinese_simplified_modern`][1]), classical Chinese
([`chinese_classical_naive`][2] and [`chinese_classical_comprehensive`][3]),
and modern English ([`english`][4]). Chinese function words are only available in simplified form.

The `FunctionWords` class does the heavy lifting.
Initiate it with the desired function word list `name`.
The instance has two methods `transform()` and `get_feature_names()`) and
three attributes (`name`, `function_words`, and `description`).

|Name      |# of function words| &nbsp; &nbsp; &nbsp; &nbsp;Description &nbsp; &nbsp; &nbsp; &nbsp;|
|:----:|:----:|:----|
| `chinese_simplified_modern`      |  819 |compiled from the [dictionary][1]     |
| `chinese_classical_naive`        |  32  |harvested from the [platforms][2]     |
| `chinese_classical_comprehensive`|  466 |compiled from the [dictionary][3]     |
| `english`                        |  512 |found in  [software][4]               |

For more details, see FunctionWords instance's attribute `description`.

## Installation

```bash
pip install -U functionwords
```

## Getting started


```python
from functionwords import FunctionWords

raw = "The present King of Singapore is bald."

# to instantiate a FunctionWords instance
# `name` can be either 'chinese_classical_comprehensive', 
# 'chinese_classical_naive', 'chinese_simplified_modern', or 'english'
fw = FunctionWords(name='english')

# to count function words accordingly
# returns a list of counts
fw.transform(raw)

# to list all function words given `name`
# returns a list
fw.get_feature_names(raw)

```

## Requirements

Only python 3.8+ is required.

## Important links

- Source code: https://github.com/Wang-Haining/functionwords
- Issue tracker: https://github.com/Wang-Haining/functionwords/issues

## Licence

This package is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

## To do

- Finish the tests.

## References
[1]: Ziqiang, W. (1998). Modern Chinese Dictionary of Function Words. Shanghai Dictionary Press.

[2]: https://baike.baidu.com/item/%E6%96%87%E8%A8%80%E8%99%9A%E8%AF%8D and 
https://zh.m.wikibooks.org/zh-hans/%E6%96%87%E8%A8%80/%E8%99%9B%E8%A9%9E

[3]: Hai, W., Changhai, Z., Shan, H., Keying, W. (1996). Classical Chinese Dictionary of Function Words. Peking University Press.

[4]: [Jstylo](https://github.com/psal/jstylo/blob/master/src/main/resources/edu/drexel/psal/resources/koppel_function_words.txt).

