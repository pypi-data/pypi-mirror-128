Simple health checks takes a modular plugin based approach to provide health checks that are right for you.

# Example response from health checks endpoint

```json
{"serviceName": "myProject", "requestUrl": "localhost:8000/health/1/", "datetime": "2021-11-19T11:53:26ZUTC", "components": ["Database", "RabbitMQ"], "status": "OK", "version": "1.5.0", "simpleHealthChecksVersion": "1.0.0"}
```

## Setup

### Environment variables

The following environment variables should be set up:

- `SETTINGS_FILE_FOR_DYNACONF` - Can be used to point to a config file to load the environment variables listed below,
 check the [dynaconf documentation](https://dynaconf.readthedocs.io/en/docs_223/guides/usage.html#the-settings-files)
- `HEALTH_CHECKS_RESOURCES` - all resources available for health check, 
    * for env vars it should be set in the following format `@json ["resource1", "resource2"]`
    * for ini files it can be set as `=resource1,resource2` without quotations
- `HEALTH_CHECKS_CRITICAL` - same format required as `HEALTH_CHECKS_RESOURCES`
 resource file names (the same as you use in `HEALTH_CHECKS`) that are critical for the 
application and will result in a DOWN status, they should also be present in `HEALTH_CHECKS`
- `HEALTH_CHECKS_TIMEOUT` - seconds until timeout, default 10
- `HEALTH_CHECKS_CACHE_SECONDS` - seconds to cache health check results, default 5
- `HEALTH_CHECKS_SERVICE_NAME` - name of the service you're adding this to (this should 
match the filename of the resource if a health check exists for the service)
- `HEALTH_CHECKS_SERVICE_VERSION` - the current version of the service hosting this package
- `HEALTH_CHECKS_MAX_WORKERS` - Number of workers to run processes in parallel, default 2

If using the `django_views` plugin:

- `HEALTH_CHECKS_TOKEN` - token required to access health of dependencies

If using the `rabbitmq` plugin:

- `HEALTH_CHECKS_RABBITMQ_BROKER_URL` - the broker url used by rabbitmq


### Installing for local development

Move to the `src/` directory
Run `pip install .`

To install plugins run: `pip install plugins/<folder containing setup.py>` from the `src/` directory


### Setting up a new resource

Notes: can_skip - does the resource you are adding support `?skip=` parameter - if not we should not send it (can_skip should be False) as 
external dependencies can be sensitive to unknown query parameters


### Plugins

Plugins can be created by following the directory structure shown in the existing plugins. They should mirror the structure of `simple_health_checks`
You can extend config by providing a file that adds [dynaconf](https://github.com/rochacbruno/dynaconf) validators. This file should exist in `additional_configs/`
directory within your plugin, should contain `config` in the filename and should define a list called validators containing your dynaconf `Validator`'s

You'll need both a `VERSION` file and a `MANIFEST.in` file containing `include VERSION`.

Add the plugin's setup.py to the `build_and_publish_pypi` stage in [.gitlab-ci.yml](.gitlab-ci.yml) and adding the version in to your `VERSION` file

Add the plugin's `pip install` command to the `.py` stage using the path to your plugins `setup.py`

Ensure that you add any modules that you wish to exist in `simple_health_checks` to your `setup.py` under `packages=` 
an example is shown below for the `django_views` plugin

```python
setup(
    name="simple_health_checks_django_views",
    version="0.0.0",
    description="Django views plugin for simple-health-checks,"
    " adds endpoints for ping and health checks",
    packages=[
        "simple_health_checks.views",
        "simple_health_checks.serializers",
    ],
    install_requires=[
        "simple_health_checks",
        "Django",
        "djangorestframework",
    ],
)
```

Notice this package adds two new modules, `views` and `serializers` to `simple_health_checks`. If you wish to add a new file to an existing module, for example
adding a new resource to `resources` you would add `packages=["simple_health_checks.resources"]`

You should avoid making any config required and instead use a default value, preferring `is_configured` on the resource to define whether a resource has been
correctly configured. Another reason for this is that we initialise `HealthCheck` within `simple_health_checks.health_checks` which will be problematic for testing.
