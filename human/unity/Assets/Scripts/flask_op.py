#!/usr/bin/env python3
# By Tiger3018 2022/06/15, MIT License
from flask import Flask, request
import json
import threading
import UnityEngine  # , NetCore


def web_app_all():
    server_node = Flask("__main__")

    @server_node.route("/shutdown")  # workaround of flask server. on server_forever
    def gen_interrupt() -> None:
        raise KeyboardInterrupt("/shutdown invoked.")

    @server_node.post("/")
    def control_tower() -> None:
        try:  # not a thread safe process
            global vList
            print(json.loads(request.data))
            velocity = json.loads(request.data)
            vList[0] = float(velocity["x"])
            vList[1] = float(velocity["y"])
            vList[2] = float(velocity["z_motor"])
            vList[3] = float(velocity["z_tower"])
            UnityEngine.Debug.Log("python: x:" + str(vList[0]))
            return {"message": "OK"}
        except Exception as e:
            return {"message": "error for {}.".format(str(e))}, 403

    @server_node.errorhandler(404)
    @server_node.errorhandler(405)
    @server_node.errorhandler(500)
    def error(e):
        # UnityEngine.Debug.Log(dir(e))
        return {"message": str(e.description)}, e.code

    # may occur error on show_server_banner
    server_node.run(host="127.0.0.1", port=12121)


# class tower_test(UnityEngine.MonoBehaviour):
    # def Update():
    # print("hey you")

UnityEngine.Debug.Log("python script init")
if __name__ != "__main__":
    message = "init flask. in {}".format(__name__)
    UnityEngine.Debug.Log(message)
    # server_node.run(host="127.0.0.1", port=12121)
    # UnityEngine.Debug.Log(threading.get_ident()) # cause Unity's crash
    # global vList
    # vList[1] = 1
    web_app_all()
    # UnityEngine.Debug.Log(dir(tower))
    # UnityEngine.Console.Log(message)
else:
    # server_node.run(host="127.0.0.1", port=21212)
    print("error")
    # target = lambda:server_node.run(host="127.0.0.1", port=21212)
    pass
    # print(MonoBehaviour)
    # print(transform, gameObject)
