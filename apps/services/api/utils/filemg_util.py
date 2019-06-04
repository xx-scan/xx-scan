import re
from rest_framework.response import Response


import filelock
def file_lock_read(file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        return open(file_path, "r+", encoding="utf-8").read()
    finally:
        _flock.release()


def file_lock_write(write_str, file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        open(file_path, "w+", encoding="utf-8").write(write_str)
    finally:
        _flock.release()


def file_lock_add(write_str, file_path):
    _flock = filelock.FileLock(file_path + ".lock", timeout=2)
    _flock.acquire()
    try:
        open(file_path, "a", encoding="utf-8").write(write_str)
    finally:
        _flock.release()


def old_test_file(request, File, key_name='param', re_partern="([0-9a-zA-z].*)"):
    # data = json.loads(request.body.decode())
    def get_scanner_datas():
        lines = file_lock_read(File).split("\n")

        res_datas = []
        for line in lines:
            false_matched = re.match("\#\s(.*)", line)
            true_matched = re.match(re_partern, line)
            if false_matched:
                res_datas.append((false_matched.group(1), False))
            elif true_matched:
                res_datas.append((true_matched.group(1), True))
            else:
                # res_datas.append((None, False))
                pass
        return res_datas

    def resave_scanner_data(res_datas):
        file_lock_write(write_str="\n".join(["# "+ str(x[0]) if x[1]==False else str(x[0]) for x in res_datas ]), file_path=File)

    res_datas = get_scanner_datas()
    request_data = request.GET if request.method == "GET" else request.data
    action_type = request_data["action"] if "action" in request_data.keys() else None
    if action_type:
        res_datas = get_scanner_datas()
        ## 增加元素
        if action_type == "add":
            res_datas.append( (request_data[key_name], True) )
        # stats = [res_datas.remove(x) for x in res_datas if x[0]["scanner"] == request.GET["scanner"] ]

        ## 在列表中删除这个元素
        if action_type == "delete":
            if key_name in request_data.keys():
                [res_datas.remove(x) for x in res_datas if x[0] == request_data[key_name]]

        if action_type == "addmany":
            # res_datas.append((request_data[key_name], True) )
            ## 需要用数组传
            res_datas.extend([(x, True) for x in request_data[key_name] ] )

        ## 失效
        if action_type == "expire":
            _new_datas = []
            if key_name in request_data.keys():
                for x in res_datas:
                    if x[0] != request_data[key_name]:
                        _new_datas.append(x)
                    else:
                        _new_datas.append((x[0], False) )
            res_datas = _new_datas

        ## 重新生效
        if action_type == "reture":
            _new_datas = []
            if key_name in request_data.keys():
                for x in res_datas:
                    if x[0] != request_data[key_name]:
                        _new_datas.append(x)
                    else:
                        _new_datas.append((x[0], True))
            res_datas = _new_datas

        if action_type == "download":
            return Response({"reason": "此处不提供下载;下载规则模板即可查看"})

    try:
        return Response({"datas": [x for x in res_datas if x[0] != ""]})
    finally:
        resave_scanner_data(res_datas)


def write_str2file(file, txtstr):
    try:
        # with open(file, "w+", encoding="utf-8") as f:
        #     f.write(txtstr)
        #     f.close()
        file_lock_write(file_path=file, write_str=txtstr)
        return True
    except:
        return False