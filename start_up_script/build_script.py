import subprocess
import sys
import os

commands = ['soud mount',
            'git pull',
            'sudo ng build',
            'uwsgi --ini fileshare.ini'
            ]

cwds = [None,
        None,
        None
        ]


for x in range(0, len(commands)):
    command = commands[x]
    cwd = cwds[x]
    print(command)
    print(cwd)
    execute_command(command, cwd)