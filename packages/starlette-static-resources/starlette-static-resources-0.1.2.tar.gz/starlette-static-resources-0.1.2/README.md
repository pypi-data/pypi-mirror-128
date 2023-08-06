# StaticResources for Starlette

Like [StaticFile](https://www.starlette.io/staticfiles/) but for [package resources](https://docs.python.org/3/library/importlib.html#module-importlib.resources).

Example:

```python
import uvicorn

from starlette.applications import Starlette
from starlette_static_resources import StaticResources
from importlib_resources import files


app = Starlette()
app.mount('/', StaticResources(resources=files('example.data')), name='static')

uvicorn.run(app, host='0.0.0.0', port=8008)
```

