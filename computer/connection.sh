#!/bin/bash
# return "ok" or "error" as standard output if the internet is connected or not
ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error
