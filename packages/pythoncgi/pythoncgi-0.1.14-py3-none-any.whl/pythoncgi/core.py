import os
import re
import sys
import json
import math
import datetime
import mimetypes
import email.utils
import traceback as _traceback
from dateutil.tz import tzoffset, tzlocal
import http.client
from http.cookies import SimpleCookie
from cgi import FieldStorage
from omnitools import dt2yyyymmddhhmmss, HeadersDict, ApacheHeadersDict, str2html, encodeURIComponent, dt2rfc822gmt, rfc822gmt2dt, b64d_and_utf8d


_SERVER = dict(os.environ)
for k in list(_SERVER.keys()):
    if k.startswith("REDIRECT_"):
        _SERVER[k.replace("REDIRECT_", "")] = _SERVER[k]
arguments = FieldStorage(environ=_SERVER, keep_blank_values=True)
arguments = {k: [_.value for _ in arguments[k]] if isinstance(arguments[k], list) else arguments[k].value for k in arguments}
_SERVER = HeadersDict(_SERVER)
_GET = arguments
_POST = arguments
_SESSION = SimpleCookie()
_COOKIE = {k: v.value for k, v in SimpleCookie(_SERVER["HTTP_COOKIE"]).items()} if "HTTP_COOKIE" in _SERVER else {}
# need to vet it manually as it depends on the system
_HEADERS = ApacheHeadersDict({k: v for k, v in _SERVER.items() if k not in [
    "DOCUMENT_ROOT",
    "LANG",
    "CONTEXT_DOCUMENT_ROOT",
    "SERVER_SIGNATURE",
    "SERVER_SOFTWARE",
    "SERVER_PORT",
    "REMOTE_PORT",
    "SCRIPT_NAME",
    "SERVER_ADMIN",
    "LANGUAGE",
    "QUERY_STRING",
    "REDIRECT_QUERY_STRING",
    "GATEWAY_INTERFACE",
    "REQUEST_URI",
    "SERVER_PROTOCOL",
    "PYTHONIOENCODING",
    "SERVER_ADDR",
    "LC_ALL",
    "SCRIPT_FILENAME",
    "PATH",
    "CONTEXT_PREFIX",
]})
default_content_type = {
    "Content-Type": "text/html; charset=utf-8"
}
__response = {
    "status_code": 200,
    "headers": {},
    "content": b"",
    "cache": b""
}
__response["headers"].update(default_content_type)
__methods = {}
PRINTED = {
    "STATUS": False,
    "HEADERS": False,
}


def obj_to_bytes(obj, html: bool = True):
    if isinstance(obj, str):
        obj = obj.encode()
    elif not isinstance(obj, bytes):
        try:
            obj = json.dumps(obj, indent=2)
            if html:
                obj = str2html(obj)
        except:
            obj = str(obj)
            if html:
                obj = str2html(obj)
        obj = obj.encode()
    return obj


def log(obj, fp: str = None):
    obj = obj_to_bytes(obj, html=False)
    now = dt2yyyymmddhhmmss().encode()
    open(fp or "log.log", "ab").write(now+b" "+obj+b"\n")


def log_construct(fp: str = None):
    def _log(obj):
        return log(obj, fp)

    return _log


def set_status(code: int):
    if not PRINTED["STATUS"]:
        __response["status_code"] = code
    else:
        raise Exception("status_code printed: {}, {}".format(
            PRINTED["STATUS"],
            __response["status_code"])
        )


def set_header(k, v):
    __response["headers"][k] = v


def flush():
    _generate_headers()
    _print(__response["content"])
    __response["content"] = b""
    sys.stdout.buffer.flush()


def _print(obj):
    sys.stdout.buffer.write(obj_to_bytes(obj))


def print(obj = "", end=b"\n"):
    obj = obj_to_bytes(obj)
    __response["content"] += obj
    __response["cache"] += obj
    if end:
        end = obj_to_bytes(end)
        __response["content"] += end
        __response["cache"] += end


def traceback(tag_name: str = "code", style: str = "", limit=None, chain=True):
    return "<{tag} style='{}'>{}</{tag}>".format(
        style,
        str2html(_traceback.format_exc(limit, chain)),
        tag=tag_name
    )


def _generate_headers():
    if not PRINTED["STATUS"]:
        _print("{}: {}\n".format("Status", __response["status_code"]))
        PRINTED["STATUS"] = True
    if not PRINTED["HEADERS"]:
        for k, v in __response["headers"].items():
            _print("{}: {}\n".format(k, v))
        session = _SESSION.output()
        if session:
            session += "\n"
        _print(session)
        _print("\n")
        PRINTED["HEADERS"] = True


def _generate_response():
    _generate_headers()
    _print(__response.pop("content"))
    status_code = __response["status_code"]
    if not __response["cache"] and status_code >= 500 and status_code <= 599:
        if status_code in http.client.responses:
            msg = http.client.responses[status_code]
            status_message = "<h1>{} {}</h1><br/><p>{}</p>".format(status_code, msg, "The server has no response regarding this error.")
            _print(status_message)


def _should_return_304(fp: str = None):
    if not fp or not os.path.isfile(fp):
        return False
    lastmodified = math.floor(os.path.getmtime(fp))
    lastmodified = datetime.datetime.fromtimestamp(lastmodified)
    set_header("Last-Modified", dt2rfc822gmt(lastmodified))
    if "If-Modified-Since" in _HEADERS:
        ims = rfc822gmt2dt(_HEADERS["If-Modified-Since"])
        if ims and ims >= lastmodified:
            return True
    return False


def should_return_304(fp: str):
    def _304():
        return _should_return_304(fp)

    return _304


def _max_age(age: int = 0):
    return "max-age={}".format(age)


def _cache_control():
    set_header("Cache-Control", _max_age()+", must-revalidate")


def _should_read_from_cache_file():
    last_modified = 999
    if_modified_since = 123
    if if_modified_since >= last_modified:
        # cache = pickle.loads(open(_SERVER["SCRIPT_NAME"]+"cache", "rb").read())
        # set_status(cache["status_code"])
        # for k, v in cache["headers"]:
        #    set_header(k, v)
        # print(cache["cache"], end="")
        return True
    else:
        return False


def _write_to_cache_file(cache):
    # cache.pop("response")
    # open(_SERVER["SCRIPT_NAME"]+"cache", "wb").write(pickle.dumps(cache))
    return


def generate_range_headers(fp, disposition: str = "inline"):
    if not os.path.isfile(fp):
        set_status(404)
        raise FileNotFoundError
    range = [0, None]
    if "Range" in _HEADERS:
        m = re.match(r"bytes=(\d+)-(\d+)?$", _HEADERS["Range"])
        if m:
            start, end = [int(x) if x else x for x in m.groups()]
            if end and end < start:
                set_status(416)
                raise ValueError("end [{}] < start [{}]".format(end, start))
            range = [start, end]
    try:
        fo = open(fp, "rb")
    except:
        set_status(500)
        raise IOError("cannot open file")
    filename = os.path.basename(fp)
    size = os.path.getsize(fp)
    if range[0] >= size:
        set_status(416)
        raise ValueError("start [{}] > file size [{}]".format(range[0], size))
    if not range[1] or range[1] >= size:
        range[1] = size-1
    if range[0] != 0 or range[1] < size-1:
        set_status(206)
    length = range[1]-range[0]+1
    try:
        filename.encode("ascii")
        filename = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        filename = "filename*=utf-8''{}".format(encodeURIComponent(filename))
    set_header("Accept-Range", "bytes")
    set_header("Content-Type", mimetypes.guess_type(filename)[0] or "application/octet-stream")
    set_header("Content-Disposition", "{}; {}".format(disposition, filename))
    set_header("Content-Range", "bytes {}-{}/{}".format(range[0], range[1], size))
    set_header("Content-Length", str(length))
    return fo, range


def print_file(fo, buf_size: int = 32 * 1024, range = None):
    if not hasattr(fo, "tell") or not hasattr(fo, "read") or not hasattr(fo, "seek") or not hasattr(fo, "close"):
        raise IOError("{} is not file object".format(fo))
    if not range:
        fo.seek(0, 2)
        range = [0, fo.tell()-1]
    fo.seek(range[0])
    while True:
        buf = min(buf_size, range[1] + 1 - fo.tell())
        buffer = fo.read(buf)
        buf = None
        if not buffer:
            break
        print(buffer, end="")
        buffer = None
        flush()
    fo.close()


def basic_authorization(credentials: dict):
    def basic_auth():
        return _basic_authorization(credentials)

    return basic_auth


def _basic_authorization(credentials: dict = None):
    if not credentials:
        credentials = {"admin": "admin"}
    if "Authorization" not in _HEADERS:
        set_authenticate_response()
        return False
    u, p = parse_authorization()
    if u in credentials and credentials[u] == p:
        return True
    set_authenticate_response()
    return False


def set_authenticate_response():
    set_status(401)
    set_header("WWW-Authenticate", "Basic")


def parse_authorization():
    if "Authorization" in _HEADERS:
        authorization = _HEADERS["Authorization"].split("Basic ")[-1]
        return b64d_and_utf8d(authorization).split(":")
    else:
        return []


def execute(
        method: str = "get", cacheable: bool = False,
        cache_ctrl = _cache_control,
        cache_norm = _should_return_304,
        cache_strat = _should_read_from_cache_file,
        cache_store = _write_to_cache_file,
        authentication = _basic_authorization,
        enable_tb: bool = True, traceback_kwargs: dict = None
    ):
    def wrapper(method_main):
        limit = None
        chain = True
        try:
            limit = traceback_kwargs["limit"]
        except:
            pass
        try:
            chain = traceback_kwargs["chain"]
        except:
            pass
        def _execute():
            try:
                if authentication():
                    if cacheable:
                        cache_ctrl()
                    if cacheable and cache_norm():
                        set_status(304)
                    elif not cacheable or (cacheable and not cache_strat()):
                        method_main()
            except:
                log(_traceback.format_exc(limit, chain))
                __response["headers"].update(default_content_type)
                if enable_tb:
                    tb = traceback(**(traceback_kwargs or {}))
                else:
                    tb = "<h1>500 Internal Server Error</h1><br/><p>HTML stack trace is disabled.<br/>Check traceback log.</p>"
                __response["content"] = obj_to_bytes(tb)
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())
            try:
                _generate_response()
                if cacheable and __response["status_code"] == 200:
                    cache_store(__response)
            except:
                log(_traceback.format_exc())
                try:
                    set_status(500)
                except:
                    log(_traceback.format_exc())
            finally:
                __response.clear()

        __methods[method] = _execute
        return _execute

    return wrapper


def main():
    method = _SERVER["REQUEST_METHOD"].lower()
    if method in __methods:
        __methods[method]()
    else:
        set_status(405)

