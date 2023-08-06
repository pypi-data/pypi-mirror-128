#!/usr/bin/python3
import os
import re
import json
import traceback
from base64 import b64encode, b64decode
from omnitools import dt2yyyymmddhhmmss, encodeURIComponent, decodeURIComponent, str2html
import diff_match_patch as dmp
from pythoncgi import init, _SERVER, _SESSION, _COOKIE, _GET, _POST, _HEADERS, execute, print, set_header, set_status, main, log_construct


init()
br = "<br>"
DOCUMENT_ROOT = _SERVER["DOCUMENT_ROOT"]
REQUEST_URI = _SERVER["REQUEST_URI"]
HTTP_HOST = _SERVER["HTTP_HOST"]
root = DOCUMENT_ROOT+REQUEST_URI
logger = log_construct("ace.log")


def set_status_500(op, e):
    set_status(500)
    set_header("Content-Type", "text/html; charset=utf-8")
    logger("{}: {}".format(op, e))
    print(str2html(e))


def _traceback():
    return traceback.format_exc()


@execute("post", authentication=lambda: True)
def post():
    def op_file():
        fp = root+_POST["file"]
        if os.path.isdir(fp):
            set_status_500("op_file", "'{}' is a directory.".format(_POST["file"]))
        elif os.path.islink(fp):
            set_status_500("op_file", "'{}' is a link.".format(_POST["file"]))
        elif os.path.isfile(fp):
            print(json.dumps(b64encode(encodeURIComponent(open(root+_POST["file"], "rb").read().decode()).encode()).decode()), end=None)
        elif not os.path.exists(fp):
            set_status_500("op_file", "file '{}' does not exist".format(_POST["file"]))
        else:
            set_status_500("op_file", "unknown error with file '{}'".format(_POST["file"]))
    def op_open(root):
        try:
            root += _POST["open"]
            if root.endswith("/"):
                root = root[:-1]
            paths = [os.path.join(root, _) for _ in os.listdir(root) if _ != ".diffs"]
            files = sorted([os.path.basename(_) for _ in paths if os.path.isfile(_)], key=lambda x: x.lower())
            folders = sorted([os.path.basename(_) for _ in paths if os.path.isdir(_)], key=lambda x: x.lower())
            print(json.dumps([folders, files]))
        except:
            set_status_500("op_open", "cannot open '{}': {}".format(_POST["open"], _traceback()))
    def op_history():
        def try_remove_diff(diff_fp):
            try:
                os.remove(diff_fp)
            except:
                try:
                    os.rename(diff_fp, os.path.join(os.path.dirname(diff_fp), "{}.bak".format(os.path.basename(diff_fp))))
                except:
                    return "cannot remove diff file '{}'\n".format(diff_fp.replace(root, ""))+_traceback()
        try:
            fp = root+_POST["history"]
            diffs = os.path.join(os.path.dirname(fp), ".diffs", os.path.basename(fp))
            if os.path.isdir(diffs):
                diffs_fn = sorted([_ for _ in os.listdir(diffs) if not _.endswith(".bak")], key=lambda fn: fn.split(".")[-3], reverse=True)
            else:
                diffs_fn = []
            if "version" not in _POST:
                print(json.dumps(diffs_fn))
            else:
                if not os.path.exists(diffs):
                    os.makedirs(diffs)
                result = True
                try:
                    driver = dmp.diff_match_patch()
                    version = _POST["version"]
                    version_index = diffs_fn.index(version)
                    diff_fps = diffs_fn[:version_index+1]
                    is_roaming = re.match(r"^goto\(.*?\)$", diffs_fn[0].split(".")[-2])
                    if is_roaming:
                        diff_fps = diff_fps[1:]
                        original = open(fp, "rb").read().decode()
                        _version = diffs_fn[0]
                        diff_fp = os.path.join(diffs, _version)
                        diff = driver.patch_fromText(open(diff_fp, "rb").read().decode())
                        original = driver.patch_apply(diff, original)[0]
                        result = try_remove_diff(diff_fp) or result
                    else:
                        original = open(fp, "rb").read().decode()
                    current = original
                    for _version in diff_fps:
                        diff_fp = os.path.join(diffs, _version)
                        diff = driver.patch_fromText(open(diff_fp, "rb").read().decode())
                        original = driver.patch_apply(diff, original)[0]
                    if not (is_roaming and version_index == 0):
                        diff_fp = os.path.join(diffs, "{}.{}.diff".format(dt2yyyymmddhhmmss(), "goto({})".format(version.split(".")[-3])))
                        try:
                            diffobj = driver.patch_make(original, current)
                            diff = driver.patch_toText(diffobj)
                            open(diff_fp, "wb").write(diff.encode())
                        except:
                            _result = "cannot write diff file '{}'\n".format(diff_fp.replace(root, ""))+_traceback()
                            if isinstance(result, str):
                                result += "\n\n"+_result
                            else:
                                result = _result
                    open(fp, "wb").write(original.encode())
                except:
                    _result = "cannot write file '{}'\n".format(_POST["history"])+_traceback()
                    if isinstance(result, str):
                        result += "\n\n" + _result
                    else:
                        result = _result
                if result is True:
                    print(json.dumps(result))
                else:
                    set_status_500("op_history", result)
        except:
            set_status_500("op_history", _traceback())
    def op_save():
        try:
            result = True
            if "/ACE/index.py" in _POST["save"]:
                raise Exception("cannot update ACE CGI file with itself")
            if "/.diffs" in _POST["save"]:
                raise Exception("cannot update diff file with itself")
            fp = root+_POST["save"]
            if os.path.isfile(fp):
                history_name = _POST["history_name"]
                diffs = os.path.join(os.path.dirname(fp), ".diffs", os.path.basename(fp))
                try:
                    os.makedirs(diffs)
                except FileExistsError:
                    pass
                except:
                    raise Exception("cannot create diffs directory for file '{}'".format(_POST["save"]))
                content = decodeURIComponent(b64decode(_POST["content"]).decode())
                driver = dmp.diff_match_patch()
                diff_fp = os.path.join(diffs, "{}.{}.diff".format(dt2yyyymmddhhmmss(), history_name))
                try:
                    diffobj = driver.patch_make(content, open(fp, "rb").read().decode())
                    diff = driver.patch_toText(diffobj)
                    open(diff_fp, "wb").write(diff.encode())
                except:
                    result = "cannot write diff file '{}'\n".format(diff_fp.replace(root, ""))+_traceback()
                try:
                    open(fp, "wb").write(content.encode())
                except:
                    _result = "cannot write file '{}'\n".format(_POST["save"])+_traceback()
                    if isinstance(result, str):
                        result += "\n\n"+_result
                    else:
                        result = _result
                if result is True:
                    print(json.dumps(result))
                else:
                    raise Exception(result)
            elif not os.path.exists(fp):
                try:
                    if not os.path.exists(os.path.dirname(fp)):
                        os.makedirs(os.path.dirname(fp))
                    content = decodeURIComponent(b64decode(_POST["content"]).decode())
                    open(fp, "wb").write(content.encode())
                    print(json.dumps(True))
                except:
                    raise Exception("cannot write file '{}'\n".format(_POST["save"])+_traceback())
            else:
                raise Exception("cannot write file, path '{}' exists".format(_POST["save"]))
        except Exception as e:
            set_status_500("op_save", e.args[0])

    root = os.path.normpath(os.path.join(DOCUMENT_ROOT, ".."))
    set_header("Content-Type", "application/json")
    if "file" in _POST:
        op_file()
    elif "open" in _POST:
        op_open(root)
    elif "history" in _POST:
        op_history()
    elif "save" in _POST:
        op_save()
    else:
        set_status_500("post()", "not implemented")


if __name__ == '__main__':
    main()
