from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
import random


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    """ 
    Returns the page of content "title" if when gets request as "{server}/wiki/title" exist, otherwise returns the 404 page.
    """
    page = util.get_entry(title)

    if page == None:
        return render(request, "encyclopedia/error.html", {
            "message": "404 Page Not Found....." 
        })
    else:
        html = markdown2.markdown_path(f"entries/{title}.md")
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "html": html
        })


def search_result(request):
    """ returns the page with title as search string or returns the search result page conatining list of pages with title name whose substring is search string """
    
    query = request.GET['q']

    result = []
    entries = util.list_entries()

    for entry in entries:
        if query in entry:
            result.append(entry)
    
    if query in entries:
        return HttpResponseRedirect(reverse("wiki", args=(f"{query}",)))
    else:
        return render(request, "encyclopedia/search_result.html", {
            "result":result,
            "length":len(result)
        })



def new_page(request):
    """
    New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.

    Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    Users should be able to click a button to save their new page.
    When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
    """
    
    if request.method == 'GET':
        return render(request, "encyclopedia/newpage.html")

    title = request.POST['title']
    data = request.POST['md_field']
    
    if title in util.list_entries():
        return render(request, "encyclopedia/error.html", {
        "message": "Sorry page with that title already exist. Please choose another page title."
    })

    file = open(f"entries/{title}.md",'w')
    file.write(data)
    
    return HttpResponseRedirect(reverse("NewPage"))


def edit_page(request, edt_title):
    """ 
    Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.

    The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
    The user should be able to click a button to save the changes made to the entry.
    Once the entry is saved, the user should be redirected back to that entry’s page.

    """
    data = util.get_entry(edt_title)

    if request.method == 'GET':

        return render(request, "encyclopedia/edit_page.html", {
            "content": data,
            "title": edt_title
        })

    elif request.method == "POST":
        data = request.POST['md_field']
        
        file = open(f"entries/{edt_title}.md",'w')
        file.write(data)

        return HttpResponseRedirect(reverse("wiki", args=(edt_title,)))


def random_page(request):
    entries = util.list_entries()
    rand_num = random.randrange(0, len(entries))
    random_title = entries[rand_num]
    return HttpResponseRedirect(reverse("wiki", args=(random_title,)))