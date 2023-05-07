rm /home/$USER/.local/bin/remind
ln -s "$(pwd)/src/remind.py" /home/$USER/.local/bin/remind
cp remind.1 /home/$USER/.local/share/man/man1
