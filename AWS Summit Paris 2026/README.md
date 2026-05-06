# AWS Meetup



## 02 Typings

## Botocore Stubber

```py

def test_with_id_and_tags_included(
        self,
        acm_session: ACMClient,
        dummy_sectigo_id: str,
        fake_acm_list_certificates_respones,
        monkeypatch: pytest.MonkeyPatch,
    ):
        with Stubber(acm_session) as stubber:
            stubber.add_response(
                "list_tags_for_certificate",
                {
                    "Tags": [
                        {
                            "Key": CertificateTagKeys.SECTIGO_CERTMANAGER_ID.value,
                            "Value": dummy_sectigo_id,
                        },
                    ]
                },
                {"CertificateArn": ANY},
            )

            repository = AcmCertificateRepository(session=acm_session)

            fake_paginator = mock.MagicMock(spec=ListCertificatesPaginator)
            fake_paginator.paginate.return_value = fake_acm_list_certificates_respones

            monkeypatch.setattr(
                acm_session,
                "get_paginator",
                lambda operation_name: fake_paginator,
                raising=False,
            )

            expected_response = random.choice(fake_acm_list_certificates_respones)
            expected_summary = random.choice(
                expected_response.get("CertificateSummaryList")
            )
            requested_id = expected_summary.get("CertificateArn")

            certificate = repository.find_by_id(
                requested_id,
                include_tags=True,
            )

            stubber.assert_no_pending_responses()

        assert certificate is not None
        assert certificate.tags is not None
        assert (
            certificate.tags.get(CertificateTagKeys.SECTIGO_CERTMANAGER_ID)
            == dummy_sectigo_id
        )

```

## 01 Testing 101 & Pytest

Testing is the practice our ensuring our software solutions is/stays fit for purpose and fit for use.

### Fallacies of Software Testing

Testing Pyramid is wrong:
- It is misleading, in fact, we use the terms type of testing to express concepts that are conceptually and semantically different:

1. Display Testing Pyramid
2. Show that there those testing concepts are fundamentally different
3. Explain different testing dimensions
	1. Why are we testing = Test Purpose
	2. What aspect = Test Objective
	3. At which level of granularity = Test Scope
	4. When is it run ? = Test Trigger Method
		1. Initiated by By Human or System? = Manually-Initiated 
		2. On a timer ? = Scheduled
		3. On an Event occurring? = Event-driven
	5. How is it run or executed ? 
		1. Require human interaction or not? = Test Execution Method (Manual / Automated)
		2. Requires code be run or not? = Test Execution Mode
			Static / Dynamic
	6. Where in runs = Test Exec Env
		1. Env Mode: Non-prod / Prod
		2. Env Type: Localhost, Sandbox, QA, Live, Specialized Env


Pytest : Python Testing framework
- Writing the expected outcome as a result of your intent encode in Python
	- Organized modules & classes/functions
	- Test Fixtures
	- Static/Dynamic configuration though pytest.ini or pyproject.toml and conftest.py
	- Rich plugin architecture and +1000 available plugins
	- Full coverage of every testing scopes
	- Flexibility of organize your tests at your will
	- Auto-discovery of test modules and functions

Core features:
- Built-in and Custom Fixtures
	- monkeypatch: Temporarily modify classes, functions, dictionaries, os.environ, and other objects.
	- tmp_path: Provide a pathlib.Path object to a temporary directory which is unique to each test function.
	- tmpdir : Provide a py.path.local object to a temporary directory which is unique to each test function; replaced by tmp_path.

		Custom:
		- @pytest.fixture(scope="function|class|module|package|session")
		Autoload:
		- @pytest.fixture(autouse=True)
- Hooks: special functions that allow you to **intercept, extend, or modify** pytest’s behavior at various stages of the test lifecycle.
- Conftest.py: Autoload by directory
- Assertions
	- assert
- Mocking
	- unittest.mock.Mock(spec=...)
	- unittest.mock.MagicMock()
- Markers
	- @pytest.mark.skip(reason="...")
	- @pytest.mark.skipif(...)
	- @pytest.mark.xfail(reason="...")
	- @pytest.mark.parametrize(...)
	- @pytest.mark.timeout(seconds)
	- @pytest.mark.<custom>
	  pytest -v -m <custom> tests/test_*.py 



## 02 Unit Testing & Test Double


- Explain the core of unit testing

- Sandy Metz principles : https://gist.github.com/Integralist/7944948
  - ref: youtube.com/watch?v=URSWYvyc42M
-
- Test Double: [TDD Course w/ Uncle Bob](https://gist.github.com/lktslionel/0fbd7f05879c5b5e86119b17221f9c63)

## 03 Demo: Setup project w/ AWS SDK (Boto3) x Pytest

Organizing Python project for testing
```
+---------------------+     +-------+    +----------+   +----------+   +-----------+   +-----------+   +---------+
| Execution Method    | --> | Mode  | -> |  Scope   |-> | Objective|-> |  Purpose  |-> | Environment|-> | Trigger |
+---------------------+     +-------+    +----------+   +----------+   +-----------+   +-----------+   +---------+
```
Setup env

```sh
uv init --package awsmeetup # creating a package app
uv venv && source .venv/bin/activate
```

Tools

```sh
uv add boto3

uv tool install ty ruff
```

## 04 Case study: certificate-renewal-operator

Share the project

## 05 Advanced Unit testing Concepts w/ Pytest

- Faker lib
- Pytest markers anf hooks
- pytest-socket

```py
# conftest.py
from pytest_socket import disable_socket

def pytest_runtest_setup():
    disable_socket()
```

- Others

```py
@mock.patch.dict(
    os.environ,
    {
        EnvNames.AUTH_LOGIN: stubs.login,
        EnvNames.AUTH_CUSTOMER_URI: stubs.customer_uri,
        EnvNames.BASE_URL: stubs.base_url,
        EnvNames.TIMEOUT_IN_S: stubs.timeout_in_s,
    },
    clear=True,
)
```

````py
AUTH_CONFIGS = [
    None,
    UserLoginViaPasswordAuthConfig.model_validate(
        {
            "login": "x",
            "password": "x",
            "customer_uri": "x",
        }
    ),
    UserLoginViaCertificateAuthConfig.model_validate(
        {
            "login": "x",
            "customer_uri": "x",
        }
    ),
    DeveloperLoginAuthConfig.model_validate(
        {
            "email": "x",
            "password": "x",
            "customer_uri": "x",
        }
    ),
]

- Pytest hooks

| Hook                            | Signature (inputs)                                            | Description                     | Example                                          |
| ------------------------------- | ------------------------------------------------------------- | ------------------------------- | ------------------------------------------------ |
| `pytest_addoption`              | `(parser: pytest.Parser, pluginmanager: PytestPluginManager)` | Add CLI options                 | `parser.addoption("--env", action="store")`      |
| `pytest_configure`              | `(config: pytest.Config)`                                     | Called after config is ready    | `config.my_flag = True`                          |
| `pytest_sessionstart`           | `(session: pytest.Session)`                                   | Start of test session           | `print("Session started")`                       |
| `pytest_sessionfinish`          | `(session: pytest.Session, exitstatus: int)`                  | End of session                  | `print(exitstatus)`                              |
| `pytest_collection_modifyitems` | `(session, config, items: list[Item])`                        | Modify collected tests          | `items[:] = sorted(items, key=lambda x: x.name)` |
| `pytest_ignore_collect`         | `(collection_path: Path, config)`                             | Skip collecting files/dirs      | `return collection_path.name == "skip.py"`       |
| `pytest_runtest_setup`          | `(item: pytest.Item)`                                         | Before test runs                | `print("setup", item.name)`                      |
| `pytest_runtest_call`           | `(item: pytest.Item)`                                         | Executes test body              | *(rarely overridden)*                            |
| `pytest_runtest_teardown`       | `(item, nextitem)`                                            | After test                      | `print("teardown")`                              |
| `pytest_runtest_makereport`     | `(item, call: CallInfo)`                                      | Create test report              | `if call.excinfo: print("failed")`               |
| `pytest_runtest_logreport`      | `(report: TestReport)`                                        | Process test result             | `print(report.outcome)`                          |
| `pytest_exception_interact`     | `(node, call, report)`                                        | Handle exceptions interactively | Debug/log failures                               |
| `pytest_fixture_setup`          | `(fixturedef, request)`                                       | Customize fixture creation      | `return fixturedef._fixturefunc()`               |
| `pytest_generate_tests`         | `(metafunc: Metafunc)`                                        | Parametrize dynamically         | `metafunc.parametrize("x", [1,2])`               |
| `pytest_make_parametrize_id`    | `(config, val, argname)`                                      | Customize param IDs             | `return f"{argname}-{val}"`                      |
| `pytest_report_header`          | `(config, start_path, startdir)`                              | Add header output               | `return "My Test Suite"`                         |
| `pytest_terminal_summary`       | `(terminalreporter, exitstatus, config)`                      | Final summary output            | `terminalreporter.write("Done")`                 |
| `pytest_warning_recorded`       | `(warning_message, when, nodeid, location)`                   | Capture warnings                | `print(warning_message.message)`                 |
| `pytest_cmdline_main`           | `(config)`                                                    | Override main execution         | `return 0`                                       |
| `pytest_cmdline_parse`          | `(pluginmanager, args)`                                       | Customize CLI parsing           | Modify args                                      |
| `pytest_plugin_registered`      | `(plugin, manager)`                                           | When plugin is loaded           | `print(plugin)`                                  |


- Example:

```py
import pytest
from pytest_socket import disable_socket, enable_socket

SCOPES = ("unit", "integration", "system", "e2e")

def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--scope",
        action="store",
        choices=SCOPES,
        help="Run tests for a given scope: unit, integration, system, e2e",
    )

def pytest_configure(config: pytest.Config):
    # register markers (avoids warnings)
    for scope in SCOPES:
        config.addinivalue_line("markers", f"{scope}: mark test as {scope} test")

def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    selected_scope = config.getoption("--scope")

    if not selected_scope:
        return

    for item in items:
        # If running with --scope=X:
        # - keep tests marked with X
        # - skip others
        if selected_scope in item.keywords:
            continue
        else:
            item.add_marker(pytest.mark.skip(reason=f"not a {selected_scope} test"))

def pytest_runtest_setup(item: pytest.Item):
    # Disable network only for unit tests
    if "unit" in item.keywords:
        disable_socket()

def pytest_runtest_teardown(item: pytest.Item, nextitem):
    # Re-enable after each test
    if "unit" in item.keywords:
        enable_socket()
````

> disable_socket() is global (not automatically reverted per test).
> So once you disable it, it stays disabled unless you explicitly re-enable it.

```sh
pytest --scope=unit

pytest -m unit
```

OR Using fixtures

```py
@pytest.fixture(autouse=True)
def no_network(request):
    if "unit" in request.keywords:
        disable_socket()
        yield
        enable_socket()
    else:
        yield
```

# References

1. https://github.com/tsklabs/scm-sdk-python
2. https://github.com/lktslionel/certificate-renewal-operator/tree/main
3. https://github.com/youtype/types-boto3
4. https://github.com/miketheman/pytest-socket
5. https://github.com/getsentry/responses
6. https://gist.github.com/lktslionel/3468e6d0a920e9a49c6f9d6fca14f6a4

```

```
