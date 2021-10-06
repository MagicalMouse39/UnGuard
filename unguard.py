import os
import subprocess
from zipfile import ZipFile

banner = '''
Welcome to UnGuard
 -- by Magical --

'''

CREATE_DIR_CMD = 'mkdir {name}'

if os.name == 'nt':
    COPY_CMD = 'copy {src} {dst}'
else:
    COPY_CMD = 'cp {src} {dst}'

def move_rename(src: str, dst: str):
    pass

def fmt_path(path: str):
    if os.name == 'nt':
        return path.replace('/', '\\')
    else:
        return path.replace('\\', '/')


print(banner)

# START TEST
maps_file = 'tests/client.txt'
print('\n\nRenaming methods and variables...\n')

mapping = {}

with open(maps_file, 'r') as mapfile:
    current_class = ''
    crrent_class_name = ''
    lines = mapfile.readlines()
    line_num = 0
    while True:
        line = lines[line_num]

        if line.startswith('#'):
            continue

        current_class = line.split('-> ')[1].split(':')[0]
        current_class_name = line.split(' ->')[0]
        move_rename(fmt_path(f'{current_class}.java'), f'{current_class_name}.java')
        map = {}
        while line.startswith('    '):
                
            line_num += 1

# EXIT TEST
exit(-1)
# END TEST

mc_version  = input('MC Version: ')
mc_jar      = os.path.expandvars(fr'%appdata%\.minecraft\versions\{mc_version}\{mc_version}.jar')

if not os.path.exists(mc_jar):
    print(f'Version "{mc_version}" not found!')
    exit(-1)

maps_file   = os.path.expandvars(input('Maps: '))

if not os.path.exists(maps_file):
    print(f'Map file "{maps_file}" not found!')
    exit(-1)

print('\n\nCopying...\n')
os.system(CREATE_DIR_CMD.format(name='decompiled'))
os.system(f'cd decompiled && {CREATE_DIR_CMD.format(name="src")}')
cp = COPY_CMD.format(src=mc_jar, dst=fmt_path('./decompiled/original.jar'))
print(cp)
os.system(cp)

print('\n\nDecompiling with fernflower...\n')
ff_args     = '-din=1 -rbr=1 -dgs=1 -asc=1 -rsy=1 -iec=1 -jvn=1 -log=TRACE '
for r, d, f in os.walk('jars'):
    for file in f:
        if file.endswith('.jar'):
            ff_args += f'"-e={os.path.join(r, file)}" '

with subprocess.Popen(f'java -jar fernflower.jar {ff_args} {fmt_path("./decompiled/original.jar ./decompiled/src")}', shell=True) as fernflower:
    fernflower.wait()

print('\n\nUnzipping...\n')
with ZipFile(fmt_path('./decompiled/src/original.jar')) as compressed_jar:
    compressed_jar.extractall(fmt_path('./decompiled/src/'))