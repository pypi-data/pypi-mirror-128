# Timeseer.AI

Timeseer is a Flask web application that can run data quality analyses on time series data.

![Timeseer components](diagrams/components.svg)

## Running

First, install Python and `npm`.

Then create a virtualenv for Python and install dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ make deps
```

Then generate the NPM libraries:

```bash
$ make npm
```

Then start Timeseer:

```bash
$ make run
```

Timeseer is now listening on http://localhost:5000.

Timeseer Bus needs to be started separately:

```bash
$ make run-bus
```

Timeseer Bus is listening on http://localhost:8081.

## Configuration

See the [Admin docs](docs/admin/admin.asciidoc).

## Client

See [Timeseer client](timeseer_client/README.md).

### Release

To release a new timeseer client package to PyPI, tag the appropriate commit with `client-<version_number>`.

example:
```bash
git tag -a client-0.0.1
```

## Windows

First generate the documentation:

```
> docker run --rm -v $pwd\docs\source:/documents/source -v $pwd\timeseer\web\templates\docs:/documents/timeseer/out asciidoctor/docker-asciidoctor asciidoctor -r asciidoctor-diagram --destination-dir timeseer/out --no-header-footer source/*.asciidoc -a allow-uri-read
> docker run --rm -v $pwd\docs\admin\:/documents/admin -v $pwd\timeseer\web\static\images\docs:/documents/timeseer/out/images -v $pwd\timeseer\web\templates\docs\:/documents/timeseer/out asciidoctor/docker-asciidoctor asciidoctor -r asciidoctor-diagram --destination-dir timeseer/out --no-header-footer admin/admin.asciidoc
```

Then ensure the version number in `setup_windows.py` is correct.

Package Timeseer as a Windows `.exe` by running:

```
> python .\setup_windows.py bdist_msi
```

This generates an MSI Installer in `dist/`.

For quick testing during development,
a Windows Sandbox configuration is available in `windows/sandbox-timeseer.wsb`.

First configure Timeseer by providing a `Timeseer.toml` configuration file.
A `Timeseer-example.toml` file is provided to be copied.

Note that by default, Timeseer is configured on Windows to launch only one worker.
This is a safe default for systems with limited memory.
If not enough memory is available, the Windows Event Viewer will show that the service crashed
with a DEP (Data Execution Prevention) exception.
This probably happens because a `malloc()` returns `NULL` and this is not checked,
causing a `0x0` pointer dereference.

## Development

Install all dependencies:

```bash
(venv) $ make deps dev-deps unix-deps
```

You might need to install additional dependencies for [xmlsec](https://pypi.org/project/xmlsec/).

Format Python code using [black](https://github.com/psf/black):

```bash
(venv) $ make format
```

Lint (and autoformat JS):

```bash
(venv) $ make lint
```

To lint only Python code:

```bash
(venv) $ make lint-python
```

To lint only JS code:

```bash
$ make lint-js
```

Test:

```bash
(venv) $ make test
```

Run the docker container locally:

```bash
$ make run-docker
```

This will start Timeseer at http://localhost:8080.

The examples and example configuration will be volume mapped in the container.

Run a Timeseer bus instance locally:

```bash
$ make run-docker-bus
```

This will start Timeseer Bus at http://localhost:8081.

The examples and example configuration will be volume mapped in the container.

While developing, the `timeseer` module will not be found in tests or modules in VS Code.
To solve this, install the package:

```
(venv) $ pip install -e .
```

Update the VS Code settings to add the current path to the `pylint` path:

```json
    "python.linting.pylintArgs": ["--init-hook", "'import sys; sys.path.append(\".\")'"],
```

To enable 'hot' reload for the react files run:

```bash
(venv) $ make npm-dev
```

Finally,
to remove any generated output (javascript and documentation),
use:

```bash
$ make clean
```


### Timeseer Client

To run and test a timeseer client locally

Create a new build of the timeseer client

``` bash
(venv) $ python3 timeseer_client/setup_client.py install
```

Create the distributions

``` bash
(venv) $ python3 timeseer_client/setup_client.py sdist bdist_wheel
```

Create a new empty venv to load in your distributions and test

```bash
$ python -m venv venv-new
$ source venv-new/bin/activate
```

Copy the unzipped `timeseer-0.0.0.tar.gz` files into the `venv-new/lib` to start testing.

### E2E Testing

Timeseer uses [cypress](https://www.cypress.io/) to run E2E tests.

E2E tests rely on the ['TSAI Antwerp' data source](https://demo-data.dev.timeseer.ai).

The E2E tests expect Timeseer to be available on port 8080.

Start Timeseer with:

```
$ python -m timeseer.server
```

on Mac start with:

```
$ python -m windows.server_windows
```

To run the E2E tests, use:

```
$ npm run cypress:run
```

During development, use:

```
$ npm run cypress:open
```

### Windows

On Windows, the usual Unix tooling is not available.
Install Python and NPM (Node.js).

Install the npm packages:

```
PS > npm ci
PS > npm run build
```

Create the virtual environment:

```
PS > python -m venv venv
```

To be able to enter the virtual environment, allow running unsigned scripts.
This can be done for the current session only:

```
PS > Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```

Alternatively, launch Powershell with the `-ExecutionPolicy Unrestricted` flag.
This can be configured in the Windows Terminal profile.

Enter the virtual environment:

```
PS > .\venv\Scripts\activate
(venv) PS >
```

Set the environment variables required by Flask to start:

```
(venv) PS > $Env:FLASK_APP = "timeseer.web"
(venv) PS > $Env:FLASK_ENV = "development"
```

Then start Timeseer:

```
(venv) PS > python -m flask run
```

### Configuration

The default configuration contains an include for `data/*.toml`.
Store the configuration for development sources in `data/`.
This prevents them to be overwritten by updates and does not require them to be stashed away when rebasing.

To start Timeseer (on http://localhost:8080) with only one customer configuration loaded, use:

```bash
(venv) $ python -m timeseer.server --config-file data/<customer>.toml
```

To start both the web server (on http://localhost:8080) and the flight interface (on localhost:8080),
create `data/flight.toml`:

```
[flight]
enable = true
authentication = false
```

Now start Timeseer with:

```bash
$ python -m timeseer.server
```

This will not automatically reload the web server when files change.
Use `make` and `make run-bus` separately to achieve that.

### Database Migrations

Timeseer uses [Yoyo](https://ollycope.com/software/yoyo/latest/) for database migrations.
There is one subdirectory of `timeseer/repository/migrations` per database.

Individual migrations follow the `<number>__<name>.(sql|py)` naming conventions.
Dependencies between migrations are not automatically inferred from the naming,
but need to be explicitly declared in the migrations itself.

For example, in `002__index.sql`:

```sql
-- depends: 001__create
```

Observe that there is no extension in the name of the migration.

### Update NPM packages

Timeseer uses `npm` and webpack to manage NPM packages.
Webpack generates static include files in `timeseer/web/static/dist/` from 'libraries' in `src/`.

Update NPM packages in `package.json`.
Then run:

```bash
$ npm run build
```

### Update diagrams

Install [PlantUML](https://plantuml.com/), then run:

```bash
$ make docs
```

### Internal documentation

Internal documentation is written in [AsciiDoc](https://asciidoctor.org/docs/asciidoc-syntax-quick-reference/) in the [docs/](docs/) directory.

Build and run the container locally:

```bash
$ make run-dev-docs
```

The documentation will be available at http://localhost:8082.

### Product documentation

Data source and admin documentation can be generated using:

```bash
$ make source-docs
$ make admin-docs
```

To generate a standalone PDF of the Admin Guide, use:

```bash
$ make standalone-admin-docs
```

### License compliance

To generate a license compliance report, Fossa is used.

Download the fossa plugin

```bash
$ curl -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/fossas/fossa-cli/master/install.sh | bash
```

and run the analysis with your [Fossa api key](https://app.fossa.com/account/settings/integrations/api_tokens)

```bash
$ FOSSA_API_KEY=<YOUR_FOSSA_API_KEY> make fossa
```

To generate a report make sure your Fossa api key is of all types (opposed to push-only)

```bash
$ FOSSA_API_KEY=<YOUR_FOSSA_API_KEY> make fossa-report
```

This will generate a basic report in `compliance/NOTICE.txt`

To include the complete license report a couple of manual steps needs to be completed:

1. Go to (https://app.fossa.com/projects)[https://app.fossa.com/projects] and select the Timeseer.AI project
2. Go to the 'Reports' tab, select html format and download the report.
3. Rename the downloaded file to `license-report.html` and remove the `head`-tag
4. Make the date in `header`-tag unambiguous by using 'Month Year' e.g: `March 2021`
5. Place the `license-report.html` file in the `timeseer/web/templates/compliance` folder

## Release to demo

To release a new version to the demo server, tag the commit with `v<version>`

```bash
$ git tag -a v1.0.0
```

This will tag the latest docker image with a `stable` tag and deployed to the demo server.
