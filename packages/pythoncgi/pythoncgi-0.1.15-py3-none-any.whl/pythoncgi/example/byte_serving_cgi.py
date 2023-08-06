#!/usr/bin/python3
from pythoncgi import (
    _SERVER, _GET, _POST, _SESSION, _COOKIE, _HEADERS,
    set_status, set_header, generate_range_headers,
    execute, print, print_file, flush, main,
    log, log_construct,
    should_return_304,
    basic_authorization, parse_authorization, set_authenticate_response,
)
import os


# for apache:
# #
# # <FilesMatch \.py$>
# #    	SetEnv no-gzip 1
# #    	SetEnv dont-vary 1
# #	</FilesMatch>
# try GET http://127.0.0.1/byte_serving_cgi.py?get=/test.png
# Header: "Range: bytes=0-1023"

DOCUMENT_ROOT = _SERVER["DOCUMENT_ROOT"]


def get_fp(what):
    return os.path.join(DOCUMENT_ROOT, *(what.split("/")[1:]))


# you can do it with post
@execute(
    method="get"
)
def get():
    if "get" in _GET:
        # this method will help setup headers regarding the partial content, filename and guessed MIME type
        fo, range = generate_range_headers(
            fp=get_fp(_GET["get"]),
            disposition="attachment"
        )
        # simply use set_header to overwrite the preset headers
        # must be done before print_file
        print_file(fo=fo, range=range)


@execute(
    method="head"
)
def head():
    if "get" in _GET:
        # same as above
        generate_range_headers(fp=get_fp(_GET["get"]))


if __name__ == '__main__':
    main()

