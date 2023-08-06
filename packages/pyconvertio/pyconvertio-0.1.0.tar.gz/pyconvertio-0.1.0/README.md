# Convertio-py
A python library to use https://convertio.co/ API to convert your files.

### Installation
```
pip install pyconvertio
```
### Current functions:

```Python
from pyconvertio import Convert
API_KEY = "YOUR_API_KEY"
convert_io = Convert()
convert_io.local_file(api_key=API_KEY, file="filename", output_format="format", verbose=True)
```