# Snugthon

Snug for python3.

## See Also

- [Snug Standarts](https://github.com/aiocat/snug)
- [Snugthon PyPi Page](https://pypi.org/project/snugthon/)

## Installation (Pip)

`pip install snugthon`

## Example(s)

### Parse Snug

#### From File (Dictionary)

```py
import snugthon

data = snugthon.load("test.snug") # File name
print(data) # Output the converted object
```

#### From Source (Dictionary)

```py
import snugthon

data = snugthon.loads("users [(? name \"aiocat\" id 0) (? name \"john\" id 1)]") # Snug source
print(data) # Output the converted object
```

#### From File (JSON)

```py
import snugthon

data = snugthon.load_as_json("test.snug") # File name
print(data) # Output the transpiled JSON object
```

#### From Source (JSON)

```py
import snugthon

data = snugthon.loads_as_json("users [(? name \"aiocat\" id 0) (? name \"john\" id 1)]") # Snug source
print(data) # Output the transpiled JSON object
```

### Create Snug

```py
import snugthon

data = snugthon.dumps({ # Dictionary -> Snug converter
    "users": [
        { "id": 0, "name": "aiocat" }
    ]
})
# Or you can use:
data = snugthon.dump({ # Dictionary -> Snug converter
    "users": [
        { "id": 0, "name": "aiocat" }
    ]
}, "test.snug") # Path to save

print(data)
```

## Found a bug? Got an error?

Please create a new issue on gitlab repository.

## Contributing

If you want to contribute to this project:

- Please do not something useless.
- Use autopep8 for formatting.

## Authors

- [Aiocat](https://gitlab.com/aiocat)

## License

This project is distributed with [MIT](/LICENSE) license
