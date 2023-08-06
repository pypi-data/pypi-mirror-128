# WikiFeet

WikiFeet (The collaborative celebrity feet website) crawler.

### Example

```py
from wikifeet import WikiFeet

feet = WikiFeet("Karla Souza")
print("Karla Souza feet pic: " + feet.image())
print("Karla Souza shoe size: " + feet.shoe_size())
print("Karla Souza feet rating: " + feet.rating())

# Output:
# Karla Souza feet pic: https://pics.wikifeet.com/Karla-Souza-Feet-6104875.jpg
# Karla Souza shoe size: 6.5 US
# Karla Souza feet rating: beautiful
```

### Documentation

* [pdoc](https://sloppydaddy.github.io/wikifeet-py)