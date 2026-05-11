# -*- coding: utf-8 -*-
"""
Headless wrapper for macro 10 (build parts/bevel_gear.FCStd).
Run via: freecadcmd.exe run_macro_10_headless.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
USER_MACRO = os.path.join(HERE, "10_create_bevel_gear_part.py")

with open(USER_MACRO, "r") as f:
    code = f.read()
exec(compile(code, USER_MACRO, "exec"))

print(f"[wrapper] macro 10 finished.")
