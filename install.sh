#!/bin/bash
set -xe
[ -e /home/$USER/.local/bin/remind ] && rm /home/$USER/.local/bin/remind
ln -s "$(pwd)/src/main.py" /home/$USER/.local/bin/remind
cp doc/remind.1 /home/$USER/.local/share/man/man1
