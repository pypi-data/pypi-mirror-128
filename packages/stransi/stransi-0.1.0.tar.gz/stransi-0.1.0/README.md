[![Python package](https://github.com/getcuia/stransi/actions/workflows/python-package.yml/badge.svg)](https://github.com/getcuia/stransi/actions/workflows/python-package.yml)

# [stransi](https://github.com/getcuia/stransi#readme) 🖍️

<div align="center">
    <img class="hero" src="https://github.com/getcuia/stransi/raw/main/banner.jpg" alt="stransi" width="33%" />
</div>

> I see a `\033[31m` door, and I want it painted `\033[30m`.

stransi is a lightweight parser for
[ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code). It
implements a string-like type that is aware of its own ANSI escape sequences,
and can be used to parse most of the common escape sequences used in terminal
output manipulation.

## Features

-   ✨ [Good support of ANSI escape sequences](FEATURES.md)
-   🎨 Focus on coloring and styling
-   🛡️ Unsupported `CSI` escape sequences are emitted as tokens
-   🏜️ Only one dependency: [ochre](https://github.com/getcuia/ochre)
-   🐍 Python 3.8+

## Credits

[Photo](https://github.com/getcuia/stransi/raw/main/banner.jpg) by
[Tien Vu Ngoc](https://unsplash.com/@tienvn3012?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
on
[Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
