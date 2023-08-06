# Python CGI

<badges>[![version](https://img.shields.io/pypi/v/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)
[![license](https://img.shields.io/pypi/l/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)
[![pyversions](https://img.shields.io/pypi/pyversions/pythoncgi.svg)](https://pypi.org/project/pythoncgi/)  
[![powered](https://img.shields.io/badge/Say-Thanks-ddddff.svg)](https://saythanks.io/to/foxe6)
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://www.jetbrains.com/pycharm/)
</badges>

<i>Extremely simple Python CGI framework for Apache 2.</i>

# Hierarchy

```
pythoncgi
|---- _SERVER
|---- _GET
|---- _POST
|---- _SESSION
|---- _COOKIE
|---- _HEADERS
|---- set_status()
|---- set_header()
|---- generate_range_headers()
|---- execute()
|---- print()
|---- print_file()
|---- flush()
|---- main()
|---- log()
|---- log_construct()
|---- should_return_304()
|---- basic_authorization()
|---- parse_authorization()
'---- set_authenticate_response()
```

# Example

See [pythoncgi/example](pythoncgi/example).
