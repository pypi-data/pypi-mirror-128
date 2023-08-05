#!/usr/bin/python3
from pythoncgi import (
    _SERVER, _GET, _POST, _SESSION, _COOKIE, _HEADERS,
    set_status, set_header, generate_range_headers,
    execute, print, print_file, flush, main,
    log, log_construct,
    should_return_304,
    basic_authorization, parse_authorization, set_authenticate_response,
)
from omnitools import crc32hd, dt2rfc822gmt, rfc822gmt2dt
import datetime
import pickle
import math
import os


# try GET http://127.0.0.1/caching_101.py?get=test.html
# refresh to test 304
# and then edit test.html
# try GET again



def get_cache_fp():
    # find a way to turn URL to an os friendly filename
    # # if the client request binds to a user session
    # # you need to append those info to the hash
    return os.path.join("_cache", crc32hd(_GET["get"])+".cache")


def should_read_from_cache_file():
    if os.path.isfile(get_cache_fp()):
        # it depends on how you code write_to_cache_file, typically reversing it
        cache = pickle.loads(open(get_cache_fp(), "rb").read())
        if "Last-Modified" in cache["headers"]:
            # parse last modified value of cached response
            # this simulates client requesting with an if modified since header
            # rfc822gmt2dt converts RFC822 GMT string to UTC epoch and to datetime with no tzinfo
            ims = rfc822gmt2dt(cache["headers"]["Last-Modified"])
            if ims:
                lastmodified = math.floor(os.path.getmtime(_GET["get"]))
                lastmodified = datetime.datetime.fromtimestamp(lastmodified)
                # as long as file modified time is older
                if ims >= lastmodified:
                    # print the cached response
                    # and return True
                    # then execute wrapper will flush everything to response stream
                    # the wrapped get method will not be executed
                    # so you want to setup and print the cache here
                    set_status(cache["status_code"])
                    for k, v in cache["headers"].items():
                        set_header(k, v)
                    print(cache["cache"], end="")
                    return True
    return False


def write_to_cache_file(cache):
    # cache is a dict containing status code, headers and response body
    fp = get_cache_fp()
    try:
        os.makedirs(os.path.dirname(fp))
    except:
        pass
    try:
        open(fp, "wb").write(pickle.dumps(cache))
    except:
        pass


@execute(
    method="get",
    # you must not cache large files
    # otherwise this will consume disk space and memory
    cacheable=True,
    # when to and not to return 304 status
    # in this case should be comparing
    # "if modified since" value and "modified time" of the get file
    # # you need to implement this method if client request binds to a user session
    # # for serving static files, simply wrap this method under your custom norm method
    cache_norm=should_return_304(_GET["get"]),
    # when to and not to return the cached response
    # in this case should be comparing
    # "last modified" value of the cached response and "modified time" of the get file
    # # do not use this field if you just want 304 effect
    cache_strat=should_read_from_cache_file,
    # dump the response to file if there is no cached response or ims value to compare with modified time of the get file
    # # do not use this field if you just want 304 effect
    cache_store=write_to_cache_file,
)
def get():
    if "get" in _GET:
        # let's say you want to cache some generated HTML code for the public
        # and you do not want to generate it each time different clients request it
        print(open("template.html", "rb").read().decode().format(open(_GET["get"], "rb").read().decode()), end="")


if __name__ == "__main__":
    main()

