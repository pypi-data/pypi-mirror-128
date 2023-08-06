# jelastic-client

A Jelastic API python library.

# Installation

```bash
pip3 install jelastic-client --extra-index-url https://__token__:<your_personal_token>@gitlab.hidora.com/api/v4/projects/198/packages/pypi/simple
```
In that case, the gitlab access token needs to have `read_api` scope.

You can also install the package from [pypi](http://pypi.org):

```bash
pip3 install jelastic-client
```

# Usage

At the root of this repository, you can run

```python
import jelastic_client

api_url = "https://[hoster-api-host]/1.0/"
api_token = "your-private-access-token"

factory = jelastic_client.JelasticClientFactory(api_url, api_token)
jps_client = factory.create_jps_client()
env_name = "my-jelastic-client-test"
jps_client.install_from_file("./test/data/valid_manifest.jps", env_name)
control_client = factory.create_control_client()
env_info = control_client.get_env_info(env_name)
assert env_info.is_running() is True
```
