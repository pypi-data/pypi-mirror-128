```
Made with Python3
(C) @FayasNoushad
Copyright permission under MIT License
License -> https://github.com/FayasNoushad/Hashtags-Extract/blob/main/LICENSE
```

---

## Installation

```
pip install Hashtags-Extract
```

---

## Usage

```py
import hashtags_extract

string = "Hello, #SupportOpensource"

# with #
print(hashtags_extract.hashtags(string))
# => ["#SupportOpensource"]

# without #
print(hashtags_extract.hashtags(string, hash=False))
# => ["SupportOpensource"]
```

---

## Credits

- [Fayas Noushad](https://github.com/FayasNoushad)

---
