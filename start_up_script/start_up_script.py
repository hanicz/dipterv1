import subprocess
import sys
import sqlite3


def execute_command(command, cwd):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd=cwd)
    #output, error = process.communicate()

    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()



commands = ['sudo apt-get update',
            'sudo apt-get upgrade',
            'sudo apt-get install sqlite3'
            'sudo apt-get install nodejs npm',
            'sudo apt-get install libsqlite3-dev',
            'wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz',
            'tar xzvf Python-3.6.0.tgz',
            './configure --enable-loadable-sqlite-extensions',
            'make',
            'sudo make install',
            'pip3.6 install -r /home/pi/dipterv1/backend/requirements.txt',
            'curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -',
            'sudo apt-get install nodejs'
            'npm install']

cwds = [None,
        None,
        None,
        None,
        None,
        None,
        None,
        'Python-3.6.0/',
        'Python-3.6.0/',
        'Python-3.6.0/',
        None,
        None,
        None,
        'dipterv1/frontend']


for x in range(0, len(commands)):
    command = commands[x]
    cwd = cwds[x]
    print(command)
    print(cwd)
    execute_command(command, cwd)


conn = sqlite3.connect('/home/pi/dipterv1/backend/test.db')

c = conn.cursor()

c.execute('''CREATE TABLE ROLE (
                id INTEGER NOT NULL, 
                name VARCHAR(250) NOT NULL, 
                priority INTEGER NOT NULL, 
                PRIMARY KEY (id), 
                UNIQUE (name))''')


c.execute('''CREATE TABLE CREDENTIAL_STORE (
                id INTEGER NOT NULL, 
                environment VARCHAR(250) NOT NULL, 
                code VARCHAR(250) NOT NULL, 
                PRIMARY KEY (id), 
                UNIQUE (environment))''')

roles = [(1, 'READ', 1, ),
         (2, 'WRITE', 2, ),
         (3, 'DELETE', 3, )]

c.executemany('INSERT INTO ROLE VALUES (?,?,?)', roles)

cred_entries = []

app_secret = raw_input('Enter the app secret: ')
email = raw_input('Enter the email details seperated by '':'' : ')
dbx_key = raw_input('Enter the dropbox key: ')
dbx_secret = raw_input('Enter the dropbox secret: ')

cred_entries.append((1,'SECRET_KEY',app_secret))
cred_entries.append((2,'MAIL',email))
cred_entries.append((3,'DROPBOX_KEY',dbx_key))
cred_entries.append((4,'DROPBOX_SECRET',dbx_secret))

c.executemany('INSERT INTO CREDENTIAL_STORE VALUES (?,?,?)', cred_entries)
conn.commit()
conn.close()

