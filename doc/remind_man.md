% Remind(1) Remind user manual
% Tymoteusz Tretowicz
% May 7, 2023

# NAME

remind - simple reminder program

# SYNOPSIS

reminder [*command*] [*options*]...

# DESCRIPTION

Remind stores notes/reminders in sqlite database created in users home directory.
Notes or reminders consist of title, which program uses to find them later and
main text that ought to be remembered.

Creating simple reminder:

    remind remember -t Example title -v My first reminder

# OPTIONS

The remind source code and all documentation may be downloaded from
<https://github.com/Veermove/remind>.
