import datetime
from django.http.response import HttpResponseForbidden, Http404, HttpResponse
from django.template.context import RequestContext
from django.utils import tzinfo
from django.utils.datastructures import MultiValueDictKeyError
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


    #hitcount



    return render(request, 'title_page.html', {
        'title': title,
        'entries': entries_of_the_title,
        'form': args,
        'pages': pages,
        'current_page': entries_of_the_title,
        'page_num': num
        }, context_instance=RequestContext(request))

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

def RealTimeSearch(reqeust):
    if reqeust.POST:
        value = reqeust.POST['value']
    else:
        value = ""

    if value and TitleModel.objects.filter(name__istartswith=value):
        results = TitleModel.objects.filter(name__contains=value, name__istartswith=value).order_by()[:5]
        html = ""
        for result in results:
            data = """
                <li>
                    <a href='{}'>
                        {}
                    </a>
                </li>
            """.format("/baslik/{}".format(result.name), result.name)
        html += data
    elif not value:
        html = "<li>arama kutusuna bir şeyler yazın efendism.</li>"
    else:
        html = "<li>herhangi bir şey bulamadık efendism.</li>"

    return HttpResponse(html)

from django.contrib import auth
def LoginPage(request):
    try:
        request.user.get_username()
        return HttpResponseRedirect('/zaaa')
    except:
        c = {}
        c.update(csrf(request))
        try:
            status = request.GET['q']
        except:
            status = ""

        return render(request, 'login.html', {'c': c, 'status': status})

def AuthView(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    remember_me = request.POST.get('remember_me', None)
    user = auth.authenticate(username=username, password=password, remember_me=remember_me)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    elif User.objects.filter(username=username):
        if not password:
            return HttpResponseRedirect('/account/login?q=1')
        else:
            return HttpResponseRedirect('/account/login?q=2')
    elif not username and not password:
        return HttpResponseRedirect('/account/login?q=3')
    else:
        return HttpResponseRedirect('/account/login?q=4')

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
                return HttpResponseRedirect('/account/login')
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


def refresh_left_frame(request):
    #LastFeed
    LastFeeds = feedparser.parse('http://localhost:8000/feed/enson')
    try:
        last_feeds = LastFeeds.entries[1:-1]
        last_first = LastFeeds.entries[0]
        last_last = LastFeeds.entries[-1]
    except:
        last_feeds = []
        last_first = []
        last_last = []


    #return

    return render(request, 'ajax.html', {
        'last_feeds': last_feeds,
        'last_first': last_first,
        'last_last': last_last
    })

def ChangePassword(request):
    if not request.user:
            return HttpResponseRedirect('/')
            pass
    else:
        try:
            user = User.objects.get(username=request.user)
        except:
            return HttpResponseRedirect('/')
            pass

    if request.POST:
        try:
            oldpass = request.POST['oldpass']
        except:
            oldpass = ""
        try:
            newpass1 = request.POST['newpass1']
        except:
            newpass1 = ""
        try:
            newpass2 = request.POST['newpass2']
        except:
            newpass2 = ""
        if user.check_password(oldpass):
            if not oldpass:
                return HttpResponseRedirect('?q=3')
                pass
            if not newpass1:
                return HttpResponseRedirect('?q=4')
            if not newpass2:
                return HttpResponseRedirect('?q=4')
            if newpass1 == newpass2:
                user.set_password(newpass1)
                user.save()
                return HttpResponseRedirect('?q=5')
            else:
                return HttpResponseRedirect('?q=2')
        else:
            return HttpResponseRedirect('?q=1')

    args = {}
    args.update(csrf(request))

    try:
        status = request.GET["q"]
    except:
        status = ""
    return render(request, 'change_password.html', {
        'form': args,
        'status': status
        })

def ChangeEmail(request):
    if not request.user:
            return HttpResponseRedirect('/')
            pass
    else:
        try:
            user = User.objects.get(username=request.user)
        except:
            return HttpResponseRedirect('/')
            pass

    if request.POST:
        try:
            oldemail = request.POST['oldemail']
        except:
            oldemail = ""
        try:
            newemail1 = request.POST['newemail1']
        except:
            newemail1 = ""
        try:
            newemail2 = request.POST['newemail2']
        except:
            newemail2 = ""
        if user.email == oldemail:
            if not oldemail:
                return HttpResponseRedirect('?q=3')
            if not newemail1:
                return HttpResponseRedirect('?q=4')
            if not newemail2:
                return HttpResponseRedirect('?q=4')
            if newemail1 == newemail2:
                user.email = newemail1
                user.save()
                return HttpResponseRedirect('?q=5')
            else:
                return HttpResponseRedirect('?q=2')
        else:
            return HttpResponseRedirect('?q=1')

    args = {}
    args.update(csrf(request))

    try:
        status = request.GET["q"]
    except:
        status = ""
    return render(request, 'change_email.html', {
        'form': args,
        'status': status
        })

