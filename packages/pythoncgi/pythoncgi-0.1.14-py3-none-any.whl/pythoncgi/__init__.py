__version__ = "0.1.14"
__keywords__ = ["python cgi apache stream file cache server proxy http cors"]


# if not __version__.endswith(".0"):
#     import re
#     print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
#     print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
#     import os
#     os._exit(1)


from .core import (
    _SERVER, _GET, _POST, _SESSION, _COOKIE, _HEADERS,
    set_status, set_header, generate_range_headers,
    execute, print, print_file, flush, main,
    log, log_construct,
    should_return_304,
    basic_authorization, parse_authorization, set_authenticate_response,
)

