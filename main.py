import os
import sys
from bottle import request, route, run, template, static_file
import mistune

def get_global_notes_path():
    try:
        if os.path.exists(sys.argv[1]):
            GLOBAL_NOTES_PATH = sys.argv[1]
    except:
        GLOBAL_NOTES_PATH = "./"

    return GLOBAL_NOTES_PATH

def get_assets_path():
    a = os.path.realpath(__file__)
    split = a.split("/")
    split.pop()
    joined = "/".join(split)
    return joined 

ASSETS_PATH = get_assets_path()
GLOBAL_NOTES_PATH = get_global_notes_path()

def get_md_files():
    p = os.listdir(GLOBAL_NOTES_PATH)
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

def create_routes():
    # TODO find better place for this var
    main_template = "{}/views/main.tpl".format(ASSETS_PATH)

    @route('/')
    @route('/home')
    @route('/index')
    def index():
        check_home_address()
        pretty_md_files = get_pretty_md_files()
        return template(main_template, info="", md=pretty_md_files)

    @route('/<note>')
    def r(note):
        check_home_address()
        pretty_md_files = get_pretty_md_files()
        markdown_note_path = '{}{}.md'.format(GLOBAL_NOTES_PATH, note) 
        print(markdown_note_path)
        with open(markdown_note_path, 'r') as markdown_note:
            buf = markdown_note.read()
        rendered_markdown_note = mistune.markdown(buf)
        return template(main_template, info=rendered_markdown_note, md=pretty_md_files)

    @route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='{}/static'.format(ASSETS_PATH))



def start_server():
    create_routes()
    run(host='localhost', port=3000, reloader=True)

if __name__ == "__main__":
    start_server()
