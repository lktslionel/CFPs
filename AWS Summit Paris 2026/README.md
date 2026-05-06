# AWS Meetup

## 01 Setup env

```sh
uv init --package awsmeetup # creating a package app
uv venv && source .venv/bin/activate
```

Tools

```sh
uv add boto3

uv tool install ty ruff
```

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

## 01 Testing 101 & Unit testing

- Sandy Metz principles : https://gist.github.com/Integralist/7944948
  - ref: youtube.com/watch?v=URSWYvyc42M
-

## 02 Pytest & Test Doubles

## 03 Demo: Setup project w/ AWS SDK (Boto3) x Pytest

## 04 Case study: certificate-renewal-operator

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
