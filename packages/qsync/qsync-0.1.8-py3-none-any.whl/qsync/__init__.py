from json.decoder import JSONDecodeError
from os import path, walk, mkdir, remove
from multiprocessing import Process
from json import dumps, loads
from distutils.dir_util import remove_tree
from time import sleep, ctime
from datetime import datetime
from shutil import copy2
from random import randint
from requests import get
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# all errors


class InvalidPathError(Exception):

    def __init__(self, path) -> None:
        self.message = "This path does not exists : " + path
        super().__init__(self.message)


# real shit 0_0
class SyncIniter():

    """
    this class contains all the necessary to start a one/twos ways sync
    """

    def __init__(self, sync_src, sync_dst, bi_directionnal=True, remote=False, force_id=None, remote_ip="", loop_time=5):
        self.bi_directionnal = bi_directionnal
        self.sync_src = sync_src.replace("\\", "/")
        self.sync_dst = sync_dst.replace("\\", "/")
        self.remote = remote
        self.remote_ip = remote_ip
        self.sync_id = f"{hex(randint(10**256,10**257))}" if force_id == None else f"{force_id}"
        self.tmp_file = self.sync_id + ".conf"
        self.loop_time = loop_time

    def __check_file_integrity(self):

        if (not path.exists(self.sync_src)):
            raise InvalidPathError(self.sync_src)
        elif (not path.exists(self.sync_dst)) and (not self.remote):
            raise InvalidPathError(self.sync_dst)

    def start_sync(self):
        """
        basically start the sync processes
        """

        if self.remote:
            self.__check_file_integrity()
            # first sync way
            self.s1 = Process(target=SyncProcess(
                self.sync_src, self.sync_dst, self.tmp_file, remote=True, remote_ip=self.remote_ip, loop_time=self.loop_time).start)
            self.s1.start()

        else:

            self.__check_file_integrity()
            # first sync way
            self.s1 = Process(target=SyncProcess(
                self.sync_src, self.sync_dst, self.tmp_file, loop_time=self.loop_time).start)
            self.s1.start()

            if self.bi_directionnal:
                # second sync way
                self.s2 = Process(target=SyncProcess(
                    self.sync_dst, self.sync_src, self.tmp_file, loop_time=self.loop_time).start)

                self.s2.start()

    def stop_sync(self) -> None:
        """
        stop the two sync processes (or the one if the sync is one way)
        """
        self.s1.kill()
        if self.bi_directionnal:
            self.s2.kill()

        remove(self.tmp_file)


class SyncProcess():

    """

    This class contains all the necessary to init a watchdog and process to sync two folders in one way

    """

    def __init__(self, sync_src: str, sync_dst: str, tmp_file: str, remote=False, remote_ip="", loop_time=5):
        self.sync_src = sync_src
        self.sync_dst = sync_dst
        self.tmp_file = tmp_file
        self.map = []
        self.old_map = []
        self.remote = remote
        self.loop_time = loop_time
        self.sRelativePath = ""
        self.sRemoteIP = remote_ip
        self.sync_id = self.tmp_file.replace(".conf", "")
        self.last_op = {}
        self.bIsConnected = False

    def __determine_relative_path(self):
        lSrcSplit = self.sync_src.split("/")
        lDstSplit = self.sync_dst.split("/")

        sep = ""
        for el in lSrcSplit:

            if el in lDstSplit:
                sep = el
                break

        self.sRelativePath = sep + self.sync_src.split(sep)[1]

    def __remote_sync_process(self):

        # self.__determine_relative_path()

        self.map = []
        self.__recursive(self.sync_src)
        self.__write_last_op()
        self.__store_update("", init=True)

        # init <sync_id>.lastop file
        with open(f"{self.sync_id}.lastop", "w") as f:
            f.write(dumps({}))
            f.close()

        # set old_map to remote map value
        with open(self.tmp_file, "r") as f:

            ctt = loads(f.read())
            f.close()

        self.old_map = ctt["sync_map"]

        while True:

            # update self.old_map
            self.old_map = self.map
            self.map = []
            # update self.map
            self.__recursive(self.sync_src)

            try:

                if self.__is_sync_safe(remote=True):
                    # try gettting a newer version of remote map
                    self.__update_remote_map()

                # try trigger the other server to make modifications on this filesystem
                get(f"https://{self.sRemoteIP}:2121/sync_map",
                    timeout=1, params={"sync_id": self.sync_id}, verify=False)
                self.bIsConnected = True
            except Exception as e:
                self.bIsConnected = False

            mod_files = self.__get_files_to_update()

            # loop and compare maps of directories architecture
            if str(self.old_map) != str(self.map):

                if self.__is_sync_safe(remote=True):
                    print("User action detected, storing it...")
                    for ele in self.map:

                        # build the future path of element
                        tmp = ele.replace(
                            self.sync_src, self.sync_dst).replace("\\", "/")

                        # add non existing folder
                        if path.isdir(ele) and (not ele in self.old_map):
                            self.__store_update(
                                tmp, folder=True, delete=False)
                            print(
                                f"\type : add non existing folder \npath = {ele}")

                        # add non existing file
                        elif path.isfile(ele) and (not ele in self.old_map):
                            self.__store_update(
                                tmp, folder=False, delete=False)
                            print(
                                f"\ttype : add non existing file \npath = {ele}")

                    deleted_elements = [
                        ele for ele in self.old_map if ele not in self.map]

                    for ele in deleted_elements:
                        print(f"\ttype : deleted element\npath = {ele}")
                        # build the future path of element
                        tmp = ele.replace(
                            self.sync_src, self.sync_dst).replace("\\", "/")

                        self.__store_update(
                            tmp, unknown_type=True, delete=True)

                    self.__write_last_op(remote=True)

            # loop throught files that have been modified
            if (mod_files != []) and self.__is_sync_safe():
                if self.__is_sync_safe(remote=True):
                    for file in mod_files:
                        print(f"\ttype : modified file \npath = {file}")
                        # build the future path of element
                        tmp = file.replace(
                            self.sync_src, self.sync_dst).replace("\\", "/")

                        self.__store_update(tmp, folder=False, delete=False)

                    self.__write_last_op(remote=True)

            sleep(self.loop_time)

    def __store_update(self, full_path, folder=False, delete=False, unknown_type=False, init=False):

        dJSONContent = {"actions": []}

        if init:
            with open(f"{self.sync_id}.conf.remote", "w") as f:
                f.write(dumps(dJSONContent))
                f.close()
            return

        if path.exists(f"{self.sync_id}.conf.remote"):

            with open(f"{self.sync_id}.conf.remote", "r") as f:

                try:
                    dJSONContent = loads(f.read())
                except JSONDecodeError:
                    f.close()
                    # file is being cleared by server process,
                    # wait 0.2 and restart
                    sleep(0.2)
                    self.__store_update(
                        full_path, folder=folder, delete=folder, unknown_type=unknown_type, init=init)

        if unknown_type and delete:

            dJSONContent["actions"].append(
                {"action_type": "delete", "target": full_path})

        elif folder and (not delete):
            dJSONContent["actions"].append(
                {"action_type": "new_folder", "target": full_path})

        elif (not folder) and (not delete):
            dJSONContent["actions"].append(
                {"action_type": "modified_file", "target": full_path})

        # check if the last action is not the same as the one we want to add.
        if (len(dJSONContent) >= 1) and (self.last_op == dJSONContent["actions"][-1]):
            return

        # remove duplicates to improve efficiency
        dJSONContent["actions"] = [dict(t) for t in {tuple(
            d.items()) for d in dJSONContent["actions"]}]

        with open(f"{self.sync_id}.conf.remote", "w") as f:
            f.write(dumps(dJSONContent))
            f.close()

        # update <sync_id>.lastop file
        with open(f"{self.sync_id}.lastop", "w") as f:
            f.write(dumps(dJSONContent["actions"][-1]))
            f.close()

        # set last_op
        self.last_op = dJSONContent["actions"][-1]

    def __update_remote_map(self):

        try:
            dRemoteMap = get(
                f"https://{self.sRemoteIP}:2121/remote_map", timeout=1, params={"sync_id": self.sync_id}, verify=False)

            dRemoteMap = dRemoteMap.json()

            with open(f"{self.tmp_file}", "w") as f:
                f.write(dumps(dRemoteMap))
                f.close()

        except:
            pass

    def __sync_process(self) -> None:
        """

        the main function of the sync process

        """

        # first directory map
        self.__recursive(self.sync_src)
        self.old_map = self.map
        self.__write_last_op()

        while True:

            self.map = []
            self.__recursive(self.sync_src)
            mod_files = self.__get_files_to_update()

            # loop and compare maps of directories architecture
            if str(self.old_map) != str(self.map):

                if self.__is_sync_safe():

                    print(f"sync map from {self.sync_src} to {self.sync_dst}")

                    for ele in self.map:

                        # build the future path of element
                        tmp = ele.replace(self.sync_src, self.sync_dst)

                        # add non existing folder
                        if path.isdir(ele) and (not path.exists(tmp)):
                            mkdir(tmp) if not path.exists(tmp) else None

                        # add non existing file
                        elif path.isfile(ele) and (not path.exists(tmp)):
                            copy2(ele, tmp)

                    deleted_elements = [
                        ele for ele in self.old_map if ele not in self.map]

                    for ele in deleted_elements:
                        # build the future path of element
                        tmp = ele.replace(self.sync_src, self.sync_dst)

                        # delete existing folder in the other sync that has been deleted here
                        if path.isdir(tmp):
                            remove_tree(tmp)

                        # delete existing file in the other sync that has been deleted here
                        elif path.isfile(tmp):
                            print(f"deleting file : ", tmp)
                            remove(tmp)

                    self.__write_last_op()

                self.old_map = self.map

            # loop throught files that have been modified
            if (mod_files != []) and self.__is_sync_safe():
                if self.__is_sync_safe():
                    for file in mod_files:

                        # build the future path of element
                        tmp = file.replace(self.sync_src, self.sync_dst)
                        print(
                            f"sync modif from : {self.sync_src} to : {self.sync_dst}")
                        copy2(file, tmp)

                    self.__write_last_op()

            sleep(self.loop_time)

    def __get_files_to_update(self) -> list:
        """
            loop throught the map and check if the file modification
            date is from less than a loop time

        Returns:
            list: the list of files modified that need to be updated on the other end
        """

        files = []
        for ele in self.map:
            if path.isfile(ele):

                now = datetime.now()

                mdate = datetime.strptime(ctime(path.getmtime(ele)),
                                          "%a %b %d %H:%M:%S %Y")

                delta = now - mdate

                if delta.seconds <= self.loop_time:
                    files.append(ele)

        return files

    def __recursive(self, rootdir: str, set_old=False):
        """
        map a directory and his own subdirs, updates self.map
        """
        for root, subdirs, files in walk(rootdir):
            for dir in subdirs:
                sub_root = path.join(rootdir, dir)
                if path.exists(sub_root):
                    if set_old:
                        self.old_map.append(sub_root)
                    else:
                        self.map.append(sub_root)
                    self.__recursive(sub_root, set_old=set_old)

            for file in files:
                if path.exists(path.join(rootdir, file)):
                    if set_old:
                        self.old_map.append(path.join(rootdir, file))
                    else:
                        self.map.append(path.join(rootdir, file))

    def __write_last_op(self, remote=False):
        try:
            with open(self.tmp_file, "w") as f:
                f.write(
                    dumps({"sync_src": self.sync_src, "sync_dst": self.sync_dst, "old_sync_map": self.old_map, "sync_map": self.map, "date": datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")}))
                f.close()

        except Exception as e:
            print(e)
            # busy file ??
            sleep(self.loop_time)
            self.__write_last_op(remote=remote)

    def __is_sync_safe(self, remote=False) -> bool:
        """
        return True only if last op was from the same sync side or the weight/map has changed
        """

        # make sure no erros are in map (often when a file is moved to the upper folder)
        for i in range(len(self.map)):

            if not path.exists(self.map[i]):
                print(self.map[i])
                # make sure the bug/file is removed in both ways
                tmp = self.map[i].replace(
                    self.sync_src, self.sync_dst).replace("\\", "/")
                self.map.pop(i)
                if not remote:

                    if path.isdir(tmp):
                        remove_tree(tmp)
                    elif path.isfile(tmp):
                        remove(tmp)
                else:
                    # make sure to store the deletion if we are in a remote context
                    print("Error detected in map :\n\tType : deleted file")
                    self.__store_update(tmp, unknown_type=True, delete=True)

                # refresh the folders mapping
                self.__write_last_op()
                # skip a loop time as the folder seems to be in a huge load
                sleep(self.loop_time)

                return True

        # as it could be edited by the second process at the same time
        # it is necessary to put this block into a try/catch
        try:
            json = {}
            with open(self.tmp_file, "r") as f:
                json = loads(f.read())
                f.close()
        except Exception as e:
            return False

        f_now = datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")
        now = datetime.strptime(f_now, "%Y-%m-%d-%H-%M-%S")
        last_sync_time = datetime.strptime(
            json['date'], "%Y-%m-%d-%H-%M-%S")
        delta = now - last_sync_time

        if remote:

            if self.bIsConnected and self.last_op != {}:
                remote_last_op = get(f"https://{self.sRemoteIP}:2121/last_op",
                                     timeout=1, params={"sync_id": self.sync_id}, verify=False).json()
                last_op = self.last_op
                last_op["target"] = last_op["target"].replace(
                    self.sync_dst, self.sync_src).replace("//", "/")

                if dumps(last_op) == dumps(remote_last_op):
                    return False

            return True if (self.old_map != str(self.map)) and (delta.seconds >= self.loop_time*2) else False

        return True if (not json["old_sync_map"] == str(self.map)) and (delta.seconds >= self.loop_time*2) else False

    def start(self) -> None:
        """
        function to start a sync loop (you may want to pass this method as target of a process)
        """
        if self.remote:
            self.__remote_sync_process()

        else:
            self.__sync_process()
