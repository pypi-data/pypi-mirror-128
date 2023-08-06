# DNAstack Client Library
`dnastack` (formerly `clippe` (RIP 2021-2021)) is the command line interface and Python library for DNAstack products

This project is written in Python and uses the [Click](https://click.palletsprojects.com/en/7.x/). The documentation is really nice so make sure to have a look if you're running into any problems developing.

## Getting Started

### Running the CLI locally
1. Run `pip3 install -r requirements.txt` to download all the dependencies
2. From the command line run `python3 -m dnastack ...`

#### Examples
```
python3 -m dnastack --help

python3 -m dnastack config set data-connect-url https://collection-service.publisher.dnastack.com/collection/library/search/

python3 -m dnastack dataconnect tables list

python3 -m dnastack dataconnect tables get covid.cloud.variants

python3 -m dnastack dataconnect query "SELECT drs_url FROM covid.cloud.files LIMIT 10"
```

### Using the CLI as a Python library
The CLI can also be imported as a Python library. It is hosted on PyPi here: https://pypi.org/project/dnastack/

You can simply install it as a dependency with `pip3 install dnastack-client-library` or through other traditional `pip` ways (e.g. `requirements.txt`)

To use the `dnastack-client-library` library in Jupyter Notebooks and other Python code, simply import the PublisherClient object

`from dnastack import PublisherClient`

#### Example

```python
from dnastack import PublisherClient

publisher_client = PublisherClient(dataconnect_url='[DATACONNECT_URL]')


# get tables
tables = publisher_client.dataconnect.list_tables()

# get table schema
schema = publisher_client.dataconnect.get_table('[TABLE_NAME]')

# query
results = publisher_client.dataconnect.query('SELECT * FROM ...')

# load a drs resource into a DataFrame
drs_df = publisher_client.load(['[DRS_URL]'])

# download a DRS resource into a file
publisher_client.download(['[DRS_URL]'])
```

## Distributing the CLI/Python library

### Versioning

The versioning for `dnastack-client-library` is done through the `bumpversion` utility.

For "patch" version updates (e.g. 1.0.0 to 1.0.1),
this process is done automatically by a git hook which updates the version in the project to the
next patch if it is not already a future version.

For minor (1.0.0 to 1.1.0) or major (1.0.0 to 2.0.0) version updates, the update has to be
done manually. This can be done by setting the value of `__version__` in [dnastack/__init__.py](dnastack/__init__.py)
to the (future) version of choice.


### CI/CD Pipeline

In it's current state, the CI/CD pipeline for the dnastack-client-library:

1. Builds the *Linux* excutable of the CLI (Windows and Mac executables need to be built manually)
2. Publishes the available executables (i.e. the ones in the `dist` folder) to Github Releases
3. Builds and publishes the PyPI package.

These processes are all triggered after every push to the `main` branch of the repo.
You should not need to do any of the above manually.

The [cloudbuild.yaml](./cloudbuild.yaml) file in the root directory specifies the steps to be run by Google Cloud Build

#### Adding secrets to the bootstrap workspace

In order to add a secret to be made available by the steps

1. Make sure your are on the `cloud-build-webhook` project on gcloud and have signed in.
2. Encrypt your secrets using
```bash
gcloud kms encrypt --plaintext-file=.env --ciphertext-file=.env.enc --location=global --keyring=cloud-build-webhook --key=secret_key`,
```
replacing with your file name and encrypted file name (i.e. same name but followed by a `.enc`)
3. Pull the [cloud-build-webhook-service](https://github.com/DNAstack/cloud-build-webhook-service) repo
and add your secrets to the
[bootstrap-workspaces/dnastack/dnastack-client-library](https://github.com/DNAstack/cloud-build-webhook-service/tree/master/bootstrap-workspaces/dnastack/dnastack-client-library)
directory and push your changes
4. Bundle the contents of the `bootstrap-workspaces/dnastack`
folder into a tar file called `bootstrap-workspace.tar.gz` using
the following command run from the `bootstrap-workspaces/dnastack` folder
```bash
tar -czf bootstrap-workspace.tar.gz --exclude=bootstrap-workspace.tar.gz .
```
5. Add a code snippet similar to the below to the `setup` step of `cloudbuild.yaml`, replacing with proper file names
```bash
gcloud kms decrypt --ciphertext-file=.env.enc --plaintext-file=.env --location=global --keyring=cloud-build-webhook --key=secret_key
cp .env /root/
rm .env
chmod 600 /root/pypi
```
6. The secret (stored in the file you specified) will be available at
`/root/[your-filename]` for all step of the cloudbuild

### Distributing through the Command Line

#### Installing `pyenv-virtualenv`

In order to standardize the build environment for the CLI, we use the `pyenv-virtualenv` command line tool.

To install, follow the instructions listed [here](https://github.com/pyenv/pyenv-virtualenv)

To create the environment to build:

```bash
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.9.0
pyenv virtualenv 3.9.0 dnastack-cli
```

To use the environment, run `pyenv activate dnastack-cli`.

To exit the environment, run `pyenv deactivate`

**Note**: The build scripts already make calls to the `activate` and `deactivate` commands sp they should only be used for manual builds.

#### Distributing as a CLI
For convenience, we have added scripts in the `scripts` directory to automate all of the distribution.

To build and/or publish the CLI,
1. If you are creating or pushing to a release, you must set the `GITHUB_TOKEN` environment variable to your Github Account token (instructions for creating a token are [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)).
2. Run the following command based on the build
```bash
./build-cli.sh
\  --help / -h
\  --mac / -m              [Build the Mac Executable]
\  --windows / -w          [Build the Windows Executable]
\  --linux / -l            [Build the Linux Executable]
\  --release / -r          [Release to Github Releases]
\      --release-version=[RELEASE VERSION] (Required for release)
\      --release-title=[RELEASE TITLE]
\      --release-desc=[RELEASE DESCRIPTION]
```

More detailed instructions on the CLI distribution can be found [here](docs/distribution.md)

#### Distributing as a Python Library

The python library is distributed on PyPI, a package manager for Python. Like the CLI, we have provided a script to build and deploy the library.

To deploy to PyPI:
1. Set the `PYPI_API_TOKEN` environment variable to your PyPI account's personal access token (information on getting a PyPI token [here](https://pypi.org/help/#apitoken))
2. Run `./scripts/deploy-pip.sh`

More detailed instructions on the CLI distribution can be found [here](docs/pypi.md)

## API References

**Note:** These references are not complete and very much a work in progress.

CLI: [CLI Reference](docs/reference/cli.md)


## Authorization

In the CLI, we use Wallet clients in order to authorize users to access Data Connect, DRS, and WES functionality.

### Passport
In order to log in to get an access token:

1. Make sure the client is correctly configured. You need to log in with the Wallet instance
associated with the service you are trying to gain access for. Information on creating a client and exisitng
configurations can be found [here](docs/clients.md). In order to set this configuration, run:
```bash
dnastack config set wallet-url [WALLET-URL]
dnastack config set client-id [CLIENT-ID]
dnastack config set client-secret [CLIENT-SECRET]
dnastack config set client-redirect-uri [REDIRECT-URI]
```
2. Log in using `dnastack auth login`. This will open a tab in your browser where you may login, then allow/deny access
to certain permissions. If allowed, a new token will be created and you will be able to access services.

### Refresh Token

Since the above requires user interaction to authenticate, it cannot be used in headless environements such as scripts.
The way that users should log in is through an OAuth refresh token.

In order to get an access token in a headless environment.
1. Get a refresh token manually by setting your auth parameters and running `dnatack auth login`.
2. Find your refresh token by running `dnastack config get oauth_token`. The refresh token is under the
`refresh_token` key and add it to your run environment.
3. In your script, when log in is required, run `dnastack config set oauth_token.refresh_token [TOKEN]`
4. Log in using `dnastack auth refresh`


## Testing

There are e2e-tests set up for the CLI. Instructions to run can be found [here](docs/e2e-tests.md)
