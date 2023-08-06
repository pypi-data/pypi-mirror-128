# Helios OpenTelemetry SDK

This page describes the Helios OpenTelemetry SDK implementation.

## Requirements
Unless otherwise noted, all published artifacts support Python 3.6 or higher.

## Getting started

### Setting the environment

1. Make sure all the required packages are installed in the environment
2. Set the `HS_ACCESS_TOKEN` env variable with your Helios access token (another option is to provide it within the code when calling to the `initialize` function)
3. If you wish to disable the instrumentation set the `HS_DISABLED` env var to `true`


### Manually instrument your code

To fully instrument your code, just import the `initialize` function from the SDK and run it in the beginning of your code

Here is an example of instrumenting a flask server:

```python
import flask
from helios import initialize

hs = initialize(service_name='my_service_name')

app = flask.Flask('my_app')

@app.route('/', methods=['GET'])
def home():
    return "OK"


app.run()
```

The Helios SDK will automatically check all the supported packages, and instrument every package that is installed on the environment

In our example, assuming the `flask` module is installed in the env, it will be instrumented, together with every other supported module that is installed in the env


### Running instrumented test
In case we don't want to manually instrument the code, but want to run instrumented test we can use the `hstest` plugin for `pytest`:

```bash
pytest -p hstest ./tests
```

This command will run all the tests in `./tests` directory using `pytest`, instrumenting all the supported packages that are installed in the environment


## Installing
The SDK package is available on the Python Package Index (PyPI). You can install it via pip with the following commands:

`pip install helios-opentelemetry-sdk`

## Testing

- install `nox`:

`pip install nox`

- run all tests using the command `nox` from the main directory
- you can list all available tests by running: `nox --list`
- you can run a single test by runnong: `nox --sessions <TEST_NAME>`

## Releasing
Follow the [releasing instructions](https://github.com/heliosphere-io/python-sdk/blob/main/RELEASING.md)






