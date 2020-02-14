import os
from pathlib import Path
import sys
from bottle import request, route, run, template, static_file
import mistune

def get_markdown_files(notepath):
    markdown_files = [] 
    for path in Path(notepath).rglob("*.md"):
        markdown_files.append(MarkdownGeniePath(notepath, path.as_posix(), path.name))

    return markdown_files

class MarkdownGeniePath:
    """
    Simple data class to more easily work with absolute path names and filenames
    """
    def __init__(self, notepath, absolute_path, filename):
        self.notepath = notepath
        self.absolute_path = absolute_path
        self.filename = filename
        self.pretty_filename = self._get_pretty_name()
        self.url_path = self._get_url_path()

    def __str__(self):
        return f"{self.absolute_path}: {self.filename}"

    def _get_pretty_name(self):
        ## Need to make sure this doesn't pop a file without an md tag
        temp = self.filename.split(".")
        return temp[0]

    def _get_url_path(self):
        s = self.absolute_path.split("/")
        url_path_arr = []
        for i in s:
            if i not in self.notepath:
                url_path_arr.append(i)

        url_path_arr.pop()
        url_path_arr.append(self.pretty_filename)
        return "/".join(url_path_arr)

def create_routes(assets_path, notepath, markdown_files):
    # TODO find better place for this var
    main_template = "{}/views/main.tpl".format(assets_path)
    content_template = f"{assets_path}/views/content.tpl"

    @route('/')
    @route('/home')
    @route('/index')
    def index():
        return template(main_template, info="", md=markdown_files, ct=content_template)

    @route('/<note>')
    def r(note):
        ## This is a fucking hack
        ## Needs to be rewritten.
        ## This should pull from some other source. Not usre now. Think about it
        for markdown_file in markdown_files:
            if markdown_file.pretty_filename == note:
                markdown_note_path = f"{markdown_file.absolute_path}"
        with open(markdown_note_path, 'r') as markdown_note:
            buf = markdown_note.read()
        rendered_markdown_note = mistune.markdown(buf)
        return template(main_template, info=rendered_markdown_note, md=markdown_files, ct=content_template)

    @route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='{}/static'.format(assets_path))

def start_server(c):
    markdown_files = get_markdown_files(c.notepath)
    create_routes(c.assets_path, c.notepath, markdown_files)
    run(host=c.host, port=3000, reloader=True)
