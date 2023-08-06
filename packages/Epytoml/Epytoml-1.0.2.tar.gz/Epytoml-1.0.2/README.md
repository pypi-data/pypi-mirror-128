# Epytoml

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub Repository](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Z1aaan/Epytoml)
[![GitHub Release Version](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/Z1aaan/Epytoml/releases)
[![PyPi](https://img.shields.io/badge/PyPi-PyPi-brightgreen)](https://pypi.org/project/Epytoml/)
[![MIT License](https://img.shields.io/github/license/Z1aaan/PackCollatzer.svg)](https://github.com/Z1aaan/Epytoml/blob/master/LICENSE.md)

Epytomil (The Epitome of Python to Markup Language), is a python package that converts plain text into a specified markup language using python.

<h5><details><summary><b>Basic Info<b></summary>
Created by: Zhean Ganituen <a href="https://github.com/Z1aaan">Z1aaan</a>

Last Updated: November , 2021

Latest Release Version: 1.0.12

GitHub Repo: <a href="https://github.com/Z1aaan/Epytoml">GitHub Repository</a>

Python Package Index: <a href="https://pypi.org/project/Epytoml/">PyPi</a>

License: <a href="https://github.com/Z1aaan/Epytoml/blob/master/LICENSE.md">MIT License</a>

</details>
</h5>

## Installation

### `pip install Epytoml`

System requirements:

- <a href="https://www.python.org/">Python 3.6 or higher</a>
- <a href="https://wkhtmltopdf.org">wkhtmltopdf</a>
- <a href="https://pdfkit.org">PDFKit</a>

## Using Epytoml

### Supported Markup Languages

- HTML
- Markdown
- Marp (Markdown Presentation Ecosystems)
- Notaker (A note-taking HTML formatter)

#### Notaker

- First import `EpyBake` and `Notaker`

  > ```
  > from Epytoml import EpyBake
  > from Epytoml.Notaker import Notaker
  > ```

- Then begin your `.py` file with `Notaker.ntkGen("Foo")`

- And remember to end your `.py` file with `Notaker.ntkShut("Bar")` and `EpyBake.ntkBake("Foo", Notaker.ntk_ContWhole)`
  > ## `Sample File`
  >
  > ```
  > from Epytoml import EpyBake
  > from Epytoml.Notaker import Notaker
  >
  > Notaker.ntkGen("Foo")
  > >>
  > >>
  > >>
  > Notaker.ntkShut("Bar")
  > EpyBake.ntkBake("Baz", Notaker.ntk_ContWhole)
  > ```

## License

This project falls under the [MIT license](https://github.com/Z1aaan/PackCollatzer/blob/main/LICENSE).
