# -*- coding: utf-8 -*-
"""Headless wrapper for macro 11 (Session-10 Phase-2 parts)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
USER_MACRO = os.path.join(HERE, "11_create_session10_parts.py")
with open(USER_MACRO, "r") as f:
    code = f.read()
exec(compile(code, USER_MACRO, "exec"))
print("[wrapper] macro 11 finished.")
