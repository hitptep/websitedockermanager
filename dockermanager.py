import os
import socket
import Communication

class DockerBlock:
    def __init__(self,dname,dhandle,dstatus,droomnum,dwatchchl):
        self.dname=dname
        self.dhandle=dhandle
        self.dstatus=dstatus
        self.droomnum=droomnum
        self.dwatchchl=dwatchchl

    def start(...):
        pass

    def close(...):
        pass
    
    
class Room:
    dockers=[]
    files=[]
    dfmapper={}
    def __init__(self):
        pass

    def deploydocker(...):
        pass

    def close(...):
        pass


class RoomBlock:
    rooms=[]
    def __init__(self):
        pass

    def create(...):
        pass

    def destroy(...):
        pass


class ControlBlock:
    roomb=RoomBlock()
    com=Communication.com()
    def __init__(self):
        pass

    def run(...):
        # communicate with backend and docker watchdogs
        # do something to control all dockers
        pass

if __name__=="__main__:
    cb=ControlBlock()
    cb.run()
    
