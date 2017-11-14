import subprocess
import sys


def execute_command(command, cwd):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=cwd)
    #output, error = process.communicate()

    ## But do not wait till netstat finish, start displaying output immediately ##
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()



commands = ['wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz',
            'tar xzvf Python-3.6.0.tgz',
            './configure --enable-loadable-sqlite-extensions',
            'make',
            'sudo make install',
            'pip3.6 install -r /home/pi/dipterv1/backend/requirements.txt']

cwds = [None,
        None,
        'Python-3.6.0/',
        'Python-3.6.0/',
        'Python-3.6.0/',
        None]


for x in range(0, len(commands)):
    command = commands[x]
    cwd = cwds[x]
    print(command)
    print(cwd)
    execute_command(command, cwd)