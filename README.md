# Remind


Simple program to create reminders and access them from terminal.
Reminders are stored in sqlite database in /home/\<user\>/.remind.db 

To remember use:
```
remind remember [-t|--title] <title> [-v|--value|-sv|--stdinvalue] <value>
```

To remind a note -use:
```
remind <title>
```

To forget a note - use:
```
remind forget <title>
```

To list all notes - use:
```
or: remind list [-t|--title|-d|--date]
```