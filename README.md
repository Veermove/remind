% Remind(1) Remind user manual
% Tymoteusz Tretowicz
% May 7, 2023

# NAME

remind - simple reminder program

# SYNOPSIS

remind [*command*] [*subcommand*] [*options*] [*flags*]...

# DESCRIPTION

Remind stores notes/reminders in sqlite database created in users home directory.
Notes or reminders consist of title, which program uses to find them later and
main text that ought to be remembered.

Creating simple reminder:

    remind remember -t Example title -v My first reminder

## REMIND
To see all reminders:

    remind list [-st | -sd]

Flags `-st` and `-sd` sort reminders by title and date respectively.

To see specific reminder:

    remind <title> [-q | --quiet]

## REMEMBER
To create new reminder:

    remind remember [-t | --title] <title> [-v | --value] <main text>

or provide value from standard input:

    remind remember [-t | --title] <title> [-sv | --stdin-val]

Additioanlly before creating reminder you can edit provided value in default editor:

    remind remember [-t | --title] <title> [-a | --alter]

## FORGET

To delete reminder:

    remind forget <title>

## ALTER

To edit reminder:

    remind alter <title> [-t | --title] <title>

This will open default editor with reminder value. After saving and closing editor new value will be saved.

# OPTIONS
When reading note flag `-q` or `--quiet` will print only main text of reminder without metdata. In other cases such as forgeting or altering, when this flag is provided program will not print anything.

Flag `-h` or `--help` will print contextual help message.

The remind source code and all documentation may be downloaded from:
<https://github.com/Veermove/remind>.
