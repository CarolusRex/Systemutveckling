# coding: utf-8
# Author: Ludwig Fingal
import os
import ntpath
from bottle import route, run, template, request, static_file, abort, redirect


@route("/")
def list_articles():
    """
    This is the home page, which shows a list of links to all articles
    in the wiki.
    """
    files = os.listdir("articles")
    filelist = []
    for file in files:
        filename = os.path.splitext(ntpath.basename(file))[0]
        filelist.append('<li><a href="/wiki/'+filename+'">'+filename+'</a>')
    return template("index", filelist=''.join(filelist))


@route('/wiki/')
@route('/wiki/<pagename>')
def show_article(pagename):
    """Displays a single article (loaded from a text file)."""
    if pagename:
        title = pagename
    else:
        title = "Articles"
    try:
        with open("articles/" + pagename + ".txt", "r") as file:
            lines = file.readlines()
            text = ''.join(lines)
        return template("article", title=title, text=text)
    except IOError:
        abort(404, "That article does not exist")


@route('/edit/')
def edit_form():
    """
    Shows a form which allows the user to input a title and content
    for an article. This form is sent via POST to /update/.
    """

    return template("edit")

@route('/wiki/<pagename>/edit')
def edit_exist_form(pagename):
    """
    Shows a form which allows the user to input a title and content for an already
    existing article. This form is sent via POST to /update_existing/.
    """
    global article
    article = pagename
    if pagename:
        title = pagename
    else:
        title = "Editing article"
    try:
        file = open("articles/" + pagename + ".txt", "r")
        lines = file.readlines()
        text = ''.join(lines)
        file.close()
        return template("edit_existing", title=title, text=text, lines=lines)
    except IOError:
        abort(404, "That article does not exist")


@route('/delete/')
def edit_form():
    """
    Shows a form which allows the user to input a title for an article.
    This form should be sent via POST to /del_update/.
    """

    return template("delete")


@route('/del_update/', method="POST")
def del_article():
    """
    Receives page title from a form, and deletes a text file for that page.
    """
    title = request.forms.title
    try:
        open("articles/" + title + ".txt", "r")
        pass
    except IOError:
        abort(404, "That article doesn't exist")
    os.remove("articles/" + title + ".txt")
    return template("del_update", title=title)


@route('/update/', method="POST")
def update_article():
    """
    Receives page title and contents from a form, and creates/updates a
    text file for that page.
    """
    title = request.forms.title
    text = request.forms.text
    if title and text:
        with open("articles/" + title + ".txt", "w+") as file:
            file.writelines(text)
        redirect('/wiki/' + title)
    else:
        abort(403, "Fill in all fields, please!")


@route('/wiki/<pagename>/update', method="POST")
def update_existing(pagename):
    title = request.forms.title
    text = request.forms.text
    article = pagename
    if title and text:
        os.rename("articles/" + article + ".txt", "articles/" + title + ".txt")
        with open("articles/" + title + ".txt", "w+") as file:
            file.writelines(text)
        redirect('/wiki/' + title)
    else:
        abort(403, "Fill in all fields, please!")


@route('/static/<filename>')
def serve_static(filename):
    """ Serves static files """
    return static_file(filename, root="static")

run(host='localhost', port=8080, debug=True, reloader=True)