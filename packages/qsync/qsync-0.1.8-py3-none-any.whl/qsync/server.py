import json
import logging
from distutils.dir_util import remove_tree
from os import path, remove, mkdir
from json import loads, dumps
from flask import Flask, send_file, request, jsonify
from werkzeug.utils import secure_filename
from requests import get, post
from distutils.dir_util import remove_tree
from urllib.parse import unquote
from multiprocessing import Process
import urllib3
from time import sleep
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# init flask app
app = Flask(__name__)


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def check_id(sync_id: str) -> bool:
    """check if a sync is associated with a given id

    Args:
        id (str): [description]

    Returns:
        bool: [description]
    """
    return True if path.exists(f"{sync_id}.conf") else False


def isInSyncDir(sync_id: str, sElementPath: str) -> bool:
    """check if a folder exists in the sync directories tree

    Args:
        file_path (str): [description]

    Returns:
        bool: [description]
    """

    try:
        with open(f"{sync_id}.conf", "r") as f:
            ctt = loads(f.read())
            f.close()
    except:  # file is bewing wrote at the same time so we read a malformed json
        sleep(0.5)
        with open(f"{sync_id}.conf", "r") as f:
            ctt = loads(f.read())
            f.close()

    return (ctt["sync_src"] in sElementPath) or (ctt["sync_dst"] in sElementPath) and (not ".." in sElementPath)


def NotifyChanges(sync_id, remote_ip):
    """

    Args:
        sync_id ([type]): [description]
        remote_ip ([type]): [description]
    """

    # get sync_src

    try:
        with open(f"{sync_id}.conf", "r", encoding="utf-8") as f:
            dSyncConf = loads(f.read())
            f.close()
    except:  # file must being wrote, returning a malformed json
        sleep(0.5)
        with open(f"{sync_id}.conf", "r", encoding="utf-8") as f:
            dSyncConf = loads(f.read())
            f.close()

    sync_src = dSyncConf["sync_src"]
    sync_dst = dSyncConf["sync_dst"]
    f.close()

    try:
        # get updates to send
        with open(f"{sync_id}.conf.remote", "r", encoding="utf-8") as f:

            ctt = loads(f.read())
            f.close()

    except:  # file must being wrote, returning a malformed json
        sleep(0.5)
        with open(f"{sync_id}.conf.remote", "r", encoding="utf-8") as f:
            ctt = loads(f.read())
            f.close()

    # clear updates file
    with open(f"{sync_id}.conf.remote", "w", encoding="utf-8") as f:
        f.write(dumps({"actions": []}))
        f.close()

    for dAction in ctt["actions"]:

        if dAction["action_type"] == "new_folder":
            get(f"https://{remote_ip}:2121/mkdir",
                params={"sync_id": sync_id, "full_path": dAction["target"]}, verify=False)

        if dAction["action_type"] == "modified_file":

            if sync_src in dAction["target"]:
                file = dAction["target"].replace(sync_src, sync_dst)
            else:
                file = dAction["target"].replace(sync_dst, sync_src)

            dFileContent = {'file': open(file, 'rb')}
            dst = dAction["target"]
            print(f"\nsending :\n{file}\nto\n{dst}\n")
            post(
                f"https://{remote_ip}:2121/upload_file", params={"sync_id": sync_id, "full_path": dst}, files=dFileContent, verify=False)

        if dAction["action_type"] == "delete":
            get(f"https://{remote_ip}:2121/remove",
                params={"sync_id": sync_id, "full_path": dAction["target"]}, verify=False)


@app.route("/is_running")
def is_running():
    return jsonify({"success": "syncronize me step-bro !"})


@ app.route("/sync_map")
def sync_map():
    sync_id = request.args.get("sync_id")
    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    Process(target=NotifyChanges, args=(sync_id, request.remote_addr,)).start()

    return jsonify({"success": "lessss goooo !!"})


@ app.route("/remote_map")
def remote_map():

    sync_id = request.args.get("sync_id")
    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    try:
        with open(f"{sync_id}.conf", "r") as f:
            ctt = loads(f.read())
            f.close()
    except:  # file is bewing wrote at the same time so we read a malformed json
        sleep(0.5)
        with open(f"{sync_id}.conf", "r") as f:
            ctt = loads(f.read())
            f.close()

    return jsonify(ctt)


@ app.route("/get_file")
def get_file(full_path):
    sync_id = request.args.get("sync_id")
    full_path = unquote(request.args.get("full_path")).replace("+", " ")

    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    elif not isInSyncDir(sync_id, full_path):
        return jsonify({"error": "file not found"})

    return send_file(full_path)


@ app.route("/upload_file", methods=["GET", "POST"])
def upload_file():

    sync_id = request.args.get("sync_id")
    full_path = unquote(request.args.get("full_path")).replace("+", " ")

    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "no file part"})

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':
            return jsonify({"error": "empty file name"})

        filename = secure_filename(file.filename)
        file.save(full_path)

        return jsonify({"success": f"{full_path} uploaded"})
    else:
        return jsonify({"error": "you need to make a POST request here !"})


@ app.route("/remove")
def remove_element():

    sync_id = request.args.get("sync_id")
    full_path = unquote(request.args.get("full_path")).replace("+", " ")

    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    elif not isInSyncDir(sync_id, full_path):
        return jsonify({"error": "element not found"})

    print(f"removing  : {full_path}")

    if path.isfile(full_path):
        remove(full_path)
    elif path.isdir(full_path):
        remove_tree(full_path)
    else:
        return jsonify({"error": "path exists but element type is undetermined, causing impossibility to process deletion"})

    return jsonify({"success": f"removed {full_path}"})


@ app.route("/mkdir")
def makedir():

    sync_id = request.args.get("sync_id")
    dirpath = unquote(request.args.get("full_path")).replace("+", " ")

    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    try:
        mkdir(dirpath)
    except Exception as e:
        return jsonify({"error": "an error occured while trying to make the new directory"})

    return jsonify({"success": f"created {dirpath}"})


@ app.route("/last_op")
def last_op():

    sync_id = request.args.get("sync_id")

    if not check_id(sync_id):
        return jsonify({"error": "id not associated with a sync process"})

    with open(f"{sync_id}.lastop", "r") as f:
        last_op = loads(f.read())
        f.close()

    return jsonify(last_op)
