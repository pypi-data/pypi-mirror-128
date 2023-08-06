"""

This Is For Security Purpose Only
As Many Noobs Using Cheap Tricks To Hack userbot.
We here to save them

~ @TeamUltroid

"""

# Lol You Are So desperate.
# You came all here just to see this
# 😂😂😂😂

import os, enum, sys
from .._python.builtin import List
_discared = ["API_ID","API_HASH","DETA_KEY","SESSION", "VC_SESSION", "REDIS_PASSWORD", "REDISPASSWORD", "HEROKU_API", "BOT_TOKEN"]

_get_sys = {}


# Class Var Clean up
def cleanup_cache(what_u_doing_here=None):
    from pyUltroid.configs import Var
    os_stuff()
    if len(sys.argv) > 1:
        sys.argv = [sys.argv[0], sys.argv[-1]]
    for z in _discared:
        if z in Var.__dict__.keys():
            _get_sys.update({z: Var.__dict__[z]})
            setattr(Var, z, "")


# Env clean up
def os_stuff():
    all = os.environ
    for z in all.keys():
        for zz in _discared:
            if zz in z:
                all.update({z: ""})

# Getting them back for re-start & soft update
def call_back():
    from pyUltroid.configs import Var
    for z in _get_sys:
        if _get_sys[z]:
            setattr(Var, z, str(_get_sys[z]))
            os.environ[z] = str(_get_sys[z])
    

class KEEP_SAFE:
    @property
    def All(self):
        return List([
    "_ignore_eval",
    "SESSION",
    "BOT_TOKEN", 
    "VC_SESSION",
    "DeleteAccountRequest",
    "HEROKU_API",
    "base64",
    "bash",
    "call_back",
    "get_me\(",
    'get_entity("me")',
    "get_entity('me')", 
    "exec",
    "phone",
    "REDIS_PASSWORD",
    "load_addons",
    "load_other_plugins",
    "os.system",
    "subprocess",
    "await locals()",
    "aexec",
    ".session.save()",
    ".auth_key.key",
    "INSTA_PASSWORD",
    "INSTA_SET",
    "SUDOS", 
    "FULLSUDO",
    "KEEP_SAFE",
    ".flushall",
    "_get_sys",
    ".env",
    "DEVLIST"])

enum._make_class_unpicklable(KEEP_SAFE)

__all__ = ["KEEP_SAFE", "cleanup_cache", "call_back"]
