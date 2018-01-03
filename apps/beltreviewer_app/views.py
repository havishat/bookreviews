# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
# the index function is called when root is visited
def index(request):
    return render(request, "beltreviewer_app/index.html")

def create(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    # user = User.objects.create(password=request.POST['password'],username=request.POST['username'],name=request.POST['name'])

    # messages.success(request, "Successfully registered!")
    return redirect('/books')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    # messages.success(request, "Successfully logged in!")
    return redirect('/books')

#Books Home page (after login)
def books(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        # 'review': Review.objects.all().order_by('-created_at')[:3],
        'recent': Review.objects.recent_and_not()[0],
        'more': Review.objects.recent_and_not()[1]
    }
    return render(request, 'beltreviewer_app/success.html', context)

#creates the book review
def addbookreview(request):
    return render(request, "beltreviewer_app/reviews.html")
    
def addbr(request):
    print request.POST['author_name']
    if len(request.POST['author_name']) == 0:
        messages.error(request,"empty, please type something")
        return redirect("/books/add")
    elif len(Author.objects.filter(author_name=request.POST['author_name'])) > 0:
        messages.error(request,"author name is in the db")
        return redirect("/books/add")
    else: 
        author = Author.objects.create(author_name=request.POST['author_name'])
        request.session['author_id'] = author.id
        book = Book.objects.create(title=request.POST['title'], author = Author.objects.get(id = request.session['author_id']))
        request.session['book_id'] = book.id
        Review.objects.create(review=request.POST['review'],rating=request.POST['rating'], book = Book.objects.get(id = request.session['book_id']), reviewer = User.objects.get(id = request.session['user_id']) )
        return redirect('/books')

def bookreview(request, id):
    print 'welcome'
    context = {
        'book': Book.objects.get(id=id),
        'author': Author.objects.filter(books__id=id),
        'review': Review.objects.filter(book__id=id).all(),
        # "reviews": Review.objects.filter(book__id=id),
        # 'user': User.objects.get(id=request.session['id']),
    }
    request.session['book_id'] = id
    print Review.objects.filter(book__id=id).all()
    return render(request, "beltreviewer_app/bookreview.html", context)

def createreview(request, id):
    print "hello2"
    Review.objects.create(book = Book.objects.get(id = request.session['book_id']),  reviewer = User.objects.get(id = request.session['user_id']), rating = request.POST['rating'], review = request.POST['review'])
    print "hello"
    return redirect('/books/' + id)

def userinfo(request, id):
    context = {
        'user': User.objects.get(id=id),
        'books': Book.objects.filter(reviews__reviewer__id = id)
    }
    # print User.objects.get(id=id)
    # print Review.objects.filter(reviewer__id=id), "helloworld"
    print Book.objects.filter(reviews__reviewer__id = id) 
    return render(request, "beltreviewer_app/userinfo.html",context)

def logout(request):
	request.session['user'] = None 
	return redirect("/")