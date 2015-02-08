import datetime
from django.http.response import HttpResponseForbidden, Http404
from django.utils import tzinfo
import feedparser
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from main.forms import EntryForm, RegisterUserForm
from main.models import Title as TitleModel, Entry as EntryModel
from django.core.paginator import Paginator
from random import randint
from django.contrib.auth.models import User


def TitlePage(request, title):
    #entry formunun kodları
    if request.POST:
        form = EntryForm(request.POST, initial={'author': request.user, 'title': get_object_or_404(TitleModel, name=title)})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/baslik/{}'.format(title))
    else:
        form = EntryForm(initial={'author': request.user, 'title': get_object_or_404(TitleModel, name=title)})

    args = {}
    args.update(csrf(request))
    args['form'] = form

    #digerleri
    try:
        entries_of_the_title = get_list_or_404(EntryModel, title=get_object_or_404(TitleModel, name=title))

    except:
        entries_of_the_title = ""

    #sayfa ayarlama kodlari
    pages = Paginator(entries_of_the_title, 10)
    try:
        if request.GET['p']:
            entries_of_the_title = pages.page(int(request.GET['p']))
            num = str(request.GET['p'])
    except:
        entries_of_the_title = pages.page(1)
        num = "1"



    return render(request, 'title_page.html', {
        'title': title,
        'entries': entries_of_the_title,
        'form': args,
        'pages': pages,
        'current_page': entries_of_the_title,
        'page_num': num
        })

def EntryPage(request, entry_id):
    entry = get_object_or_404(EntryModel, id=entry_id)
    if request.POST:
        form = EntryForm(request.POST, initial={'author': request.user, 'title': get_object_or_404(TitleModel, name=entry.title)})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/baslik/{}'.format(entry.title))
    else:
        form = EntryForm(initial={'author': request.user, 'title': get_object_or_404(TitleModel, name=entry.title)})

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, 'entry_page.html', {
        'entry': entry,
        'form': args
    })

def FeedPage(request):
    #feed
    feeds = feedparser.parse('http://localhost:8000/feed/enson')
    try:
        return render(request, 'feed_1.html', {
            'feeds': feeds.entries[1:-1],
            'first': feeds.entries[0],
            'last': feeds.entries[-1]
            })
    except:
        return render(request, 'feed_1.html', {
            'feeds': '',
            'first': '',
            'last': ''
            })

def SearchPage(request):
    try:
        if request.GET['q']:
            try:
                redirect_name = TitleModel.objects.get(name=request.GET['q']).name
            except:
                new_title = TitleModel(name=request.GET['q'])
                #entry formunun kodları
                if request.POST:
                    new_title.save()
                    form = EntryForm(request.POST, initial={'author': request.user, 'title': request.GET['q']})
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/baslik/{}'.format(request.GET['q']))
                    else:
                        TitleModel.objects.get(name=request.GET['q']).delete()
                else:
                    form = EntryForm(initial={'author': request.user, 'title': request.GET['q']})

                args = {}
                args.update(csrf(request))
                args['form'] = form
                return render(request, 'search/no_title.html', {
                    'form': args,
                    'title': request.GET['q']
                })

            return HttpResponseRedirect('/baslik/{}'.format(redirect_name))
        else:
            return render(request, 'search/search.html')
    except:
        return render(request, 'search/search.html')

from django.contrib import auth
def LoginPage(request):
    try:
        request.user.get_username()
        return HttpResponseRedirect('/zaaa')
    except:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

def AuthView(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    remember_me = request.POST.get('remember_me', None)
    user = auth.authenticate(username=username, password=password, remember_me=remember_me)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/basarisiz-giris')

def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/arama?p=cikis')

def RegisterUserPage(request):
    try:
        request.user.get_username()
        return HttpResponseRedirect('/zaa')
    except:
        if request.POST:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/giris-yap')
        else:
            form = RegisterUserForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form

        return render(request, 'register.html', {'form': args})

def index(request):
    entryCount = EntryModel.objects.all().count()
    try:
        randomEntry = EntryModel.objects.all()[randint(0, (entryCount-1))].id
        return HttpResponseRedirect('/entry/{}'.format(randomEntry))
    except:
        return HttpResponseRedirect('/arama?p=')


def vote(request):
    if request.POST:
        entry_id = request.POST['entry_id']
        vote_action = request.POST['vote_action']
        vote_type = request.POST['vote_type']
    else:
        entry_id = ''
        vote_action = ''
        vote_type = ''

    message = "mn"


    entry = EntryModel.objects.get(id=int(entry_id))

    if entry.author != request.user:
        if vote_action == 'vote' and vote_type.find('downvote'):
            entry.upVotes.add(request.user)
            message = " {}".format(entry.count_up_votes())
        elif vote_action == 'return' and vote_type.find('downvote'):
            entry.upVotes.remove(request.user)
            message = " {}".format(entry.count_up_votes())
        elif vote_action == 'vote' and vote_type.find('upvote'):
            entry.downVotes.add(request.user)
            message = " {}".format(entry.count_down_votes())
        elif vote_action == 'return' and vote_type.find('upvote'):
            entry.downVotes.remove(request.user)
            message = " {}".format(entry.count_down_votes())
    else:
        if vote_type.find('downvote') or vote_type.find('upvote'):
            message = "his entry"


    return render(request, 'ajax.html', {'message': message})

def UserPage(request, user_name):
    user = get_object_or_404(User, username=user_name)

    def totalEntry(user=user):
        try:
            return EntryModel.objects.filter(author=user).count()
        except:
            return "0"

    def EntriesEntered(user=user, choice=0):

        startDate = datetime.datetime.now() - datetime.timedelta(days=choice)
        endDate = datetime.datetime.now()

        try:
            if choice != 1:
                return EntryModel.objects.filter(author=user, pub_date__range=(startDate, endDate)).count()
            else:
                return EntryModel.objects.filter(author=user, pub_date__range=(startDate, endDate)).count()
        except:
            return "0"

    def randomEntry(user=user):
        try:
            count = EntryModel.objects.filter(author=user).count() - 1
            return EntryModel.objects.filter(author=user)[randint(0, count)]
        except:
            return ""

    def VotedEntry(user=user):
        try:
            votes = []
            if EntryModel.objects.filter(upVotes=user):
                votes.extend(EntryModel.objects.filter(upVotes=user))
            if EntryModel.objects.filter(downVotes=user):
                votes.extend(EntryModel.objects.filter(downVotes=user))

            return votes
        except:
            return []

    def HisEntries(user=user):
        try:
            return EntryModel.objects.filter(author=user).order_by('-pub_date')[:10]
        except:
            return []

    return render(request, 'user_page.html', {
        'pageUser': user,
        'totalEntry': totalEntry(),
        'thisMonth': EntriesEntered(choice=30),
        'thisWeek': EntriesEntered(choice=7),
        'thisDay': EntriesEntered(choice=1),
        'randomEntry': randomEntry(),
        'VotedEntry': VotedEntry()[:10],
        'HisEntries': HisEntries(),
        'totalvotes': len(VotedEntry())

    })

def EditPage(request, id):
    if id:
        entry = get_object_or_404(EntryModel, id=id)
        if request.user != entry.author:
            return Http404()
    else:
        return Http404()

    if request.POST:
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/entry/{}'.format(entry.id))
    else:
        form = EntryForm(instance=entry)

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'edit_entry.html', {
        'form': args,
        'entry': entry
        })

def deleteentry(request):
    if request.POST:
        id = request.POST['id']

    else:
        id = ''

    try:
        get_object_or_404(EntryModel, id=id)
    except:
        return HttpResponseRedirect('/')

    if request.user == get_object_or_404(EntryModel, id=id).author:
        get_object_or_404(EntryModel, id=id).delete()
        message = "entryiniz silindi efendism"

    else:
        message = "ajanlarımız izinsiz bir işlem yaptığını tespit etti"

    return render(request, 'ajax.html', {'message': message})
