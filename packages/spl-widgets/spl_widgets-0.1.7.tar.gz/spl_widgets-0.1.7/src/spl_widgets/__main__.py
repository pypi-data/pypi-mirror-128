from sys import argv; import os
from . import update_widgets,gorilla_clean, stk_swx, widgets_help, tuner

modules_to_alias={
    "update_widgets":update_widgets,
    "widgets_help":widgets_help,
    "gorilla_clean":gorilla_clean,
    "stk_swx":stk_swx,
    "tuner":tuner
}

cmd = argv[1:]

# if cmd[0] == "gorilla_clean":
#     gorilla_clean.main()

# elif cmd[0] == "stk_swx":
#     stk_swx.main()

# elif cmd[0] == "widgets_help":
#     widgets_help.main()

# elif cmd[0] == "tuner":
#     tuner.main()

# elif cmd[0] == "update_widgets":

if cmd[0] in modules_to_alias.keys(): modules_to_alias[cmd[0]].main()
else: print(f"Bad command ({cmd[0]})")