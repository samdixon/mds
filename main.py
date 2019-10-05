import os
import sys
from bottle import request, route, run, template, static_file
import mistune
import routes

# Hacky code right now
# Tries to take a path to notes
# If you don't give it a path it works relatively current working dir 
# Else it looks to path you give it for notes
try:
    if os.path.exists(sys.argv[1]):
        global_path = sys.argv[1]
except:
    global_path = "./"

def get_md_files():
    p = os.listdir(global_path)
    l = ["home"]
    for i in p:
        if "md" in i:
            l.append(i)
        else:
            pass
    return l

def prettify_md_files(markdown_files):
    pretty_md_files = []
    for i in markdown_files:
        temp = i.split(".")
        pretty_md_files.append(temp[0])

    return pretty_md_files

def get_pretty_md_files():
    return prettify_md_files(get_md_files())
    
def check_home_address():
    if request.remote_addr != '127.0.0.1':
        sys.exit()

# Simple data structure for passing context to pages
class PageContents:
    def __init__(self, page, contents):
        self.page = page
        self.title = page.capitalize()
        self.contents = contents


@route('/')
@route('/home')
def home():
    pretty_md_files = get_pretty_md_files()
    check_home_address()
    return template('{}views/temp.tpl'.format(global_path), info="", md=pretty_md_files)

@route('/<note>')
def r(note):
    pretty_md_files = get_pretty_md_files()
    if request.remote_addr != '127.0.0.1':
        sys.exit()
    f = '{}{}.md'.format(global_path, note) 
    print(f)
    with open(f, 'r') as f1:
        buf = f1.read()
    m = mistune.markdown(buf)
    return template('{}views/temp.tpl'.format(global_path), info=m, md=pretty_md_files)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='{}static'.format(global_path))

def start_server():
    run(host='localhost', port=3000, reloader=True)

if __name__ == "__main__":
    start_server()
