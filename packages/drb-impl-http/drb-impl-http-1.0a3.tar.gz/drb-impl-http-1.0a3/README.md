# Http & Https Implementation
This drb-impl-http module implements http and https protocol access with DRB data model. It is able to get read object using the http protocol or the https protocol.

## Http Factory and Http Node
The module implements the basic factory model defined in DRB in its node resolver. Based on the python entry point mechanism, this module can be dynamically imported into applications.

The entry point group reference is `drb.impl`.<br/>
The implementation name is `http`.<br/>
The factory class is encoded into `drb_impl_http.drb_impl_http`.<br/>

The HttpNode can be instantiated from an uri. The `ParsedPath` class provided in drb core module can help to manage these inputs.

## Using this module
To include this module into your project, the `drb-impl-http` module shall be referenced into `requirement.txt` file, or the following pip line can be run:

```commandline
pip install drb-impl-http
```
## Access Data

You can access a data on a http server with it's uri.
```
from drb_impl_http import DrbHttpNode

node = DrbHttpNode(URI)
```

## Authentication

To access a protected server you can user one of the following method:

### Basic Auth

To user basic auth you have to create an HTTPBasicAuth object
```
from requests.auth import HTTPBasicAuth
from drb_impl_http import DrbHttpNode

auth = HTTPBasicAuth(USER, PWD)
node = DrbHttpNode(URI, auth= auth)
```
We also support the digest authentication (```HTTPDigestAuth(USER, PWD)```) 
and the OAuth 1 authentication (```OAuth1(YOUR_APP_KEY, YOUR_APP_SECRET, USER_OAUTH_TOKEN, USER_OAUTH_TOKEN_SECRET)```)

### Bearer Token

To access a server with a token you have to create a Bearer object
```
from drb_impl_http import DrbHttpNode
from drb_impl_http.Bearer import Bearer

auth = Bearer(TOKEN)
node = DrbHttpNode(URI, auth= auth)
```

##Limitation

The current version doesn't manage the refresh token operation when you are using one.