# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User, Group


import json, os

from core.models import Game, Rules, ImageCategory, VideoCategory, MenuOrder, SingleMenuOrder
from core.forms import UserForm, UserProfileForm
from core.views_helper import *

def home(request):
    context = RequestContext(request)
    content = {}

    if not request.user.is_authenticated():
        content['msg'] = "Bitte zuerst die IP des Computers setzen und dann einloggen/registrieren."
    return render_to_response('home.html', content, context_instance=context)


def register(request):
    context = RequestContext(request)
    registered = False
    msg = []

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            password = request.POST['password']
            password_repeat = request.POST['password_repeat']
            if password == password_repeat:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                user.userextension.ip = getIP(request)
                user.userextension.participated_lans.add(getCurrentLAN())
                user.userextension.save()
                registered = True
            else:
                msg.append("Passwörter sind verschieden!")
        else:
            msg.append(
                "Benutzername enthält ungültige Zeichen oder ist schon vergeben!")
    else:
        user_form = UserForm()
    return render_to_response('register.html', {'errors': msg, 'user_form': user_form, 'registered': registered}, context_instance=context)


@never_cache
def login(request):
    msg = []
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user.userextension.ip = getIP(request)
                user.userextension.participated_lans.add(getCurrentLAN())
                user.userextension.save()
                # Redirect to a success page.
                auth_login(request, user)
                next = request.POST['next']
                return redirect('/%s' % next)
            else:
                # Return a 'disabled account' error message
                msg.append("Benutzeraccount für {0} gesperrt.".format(user))
        else:
            # Return an 'invalid login' error message.
            msg.append("Benutzername oder Passwort falsch.")
    return render_to_response('login.html', {'errors': msg}, context_instance=context)


def users(request):
    context = RequestContext(request)
    content = {}

    content['users'] = User.objects.filter(userextension__participated_lans=getCurrentLAN())

    return render_to_response('users.html', content, context_instance=context)


@login_required(login_url="/login/")
def menu(request):
    context = RequestContext(request)
    content = {}
    orders = MenuOrder.objects.all().order_by('id')
    content['orders'] = orders

    return render_to_response('menu.html', content, context_instance=context)


@login_required(login_url="/login/")
def menu_order(request, slug=None, command=None):
    context = RequestContext(request)
    content = {}
    try:
        order = MenuOrder.objects.get(id=slug)
    except:
        order = None
    
    if order:
        content['order'] = order
        content['order_list'] = SingleMenuOrder.objects.filter(order=order).order_by('-name')
        content['user'] = request.user

    if request.user.is_authenticated():
        if request.method == 'POST':
            if command == "delete":
                try:
                    SingleMenuOrder.objects.get(id=request.POST["menuSingleOrderId"]).delete()
                except:
                    content['error'] = "Beim Löschen der Bestellung trat ein Fehler auf."
                return HttpResponseRedirect(reverse('menu_order', kwargs={'slug': order.id}))
            elif command == "lock":
                order.locked = not order.locked
                order.save()
                return HttpResponseRedirect(reverse('menu_order', kwargs={'slug': order.id}))
            else:
                content['error'] = SingleMenuOrder.create(order, request.user.id, request.POST["orderNumber"], request.POST["extra"], request.POST["price"])
                if not content['error']:
                    return HttpResponseRedirect(reverse('menu_order', kwargs={'slug': order.id}))
    
    return render_to_response('menu_order.html', content, context_instance=context)


@login_required(login_url="/login/")
def videos(request):
    context = RequestContext(request)
    content = {}
    galleryExternDic = {}

    content['categories'] = VideoCategory.objects.all()

    gallery_folder = os.path.join(settings.MEDIA_ROOT, "video_gallery")
    for root, dirnames, files in os.walk(gallery_folder):
        for file in files:
            relDir = os.path.relpath(root, gallery_folder)
            relFile = os.path.join(relDir, file)
            if relDir in galleryExternDic:
                galleryExternDic[relDir].append(relFile)
            else:
                galleryExternDic[relDir] = [relFile, ]

    content['imageFiler'] = galleryExternDic

    return render_to_response('videos.html', content, context_instance=context)


@login_required(login_url="/login/")
def images(request):
    context = RequestContext(request)
    content = {}
    galleryExternDic = {}

    content['categories'] = ImageCategory.objects.all().exclude(description="Speisekarte")

    gallery_folder = os.path.join(settings.MEDIA_ROOT, "image_gallery")
    for root, dirnames, files in os.walk(gallery_folder):
        for file in files:
            relDir = os.path.relpath(root, gallery_folder)
            relFile = os.path.join(relDir, file)
            if relDir in galleryExternDic:
                galleryExternDic[relDir].append(relFile)
            else:
                galleryExternDic[relDir] = [relFile,]

    content['imageFiler'] = galleryExternDic


    return render_to_response('images.html', content, context_instance=context)


def rules(request):
    context = RequestContext(request)
    content = {}

    content['rules'] = Rules.objects.all()
    return render_to_response('rules.html', content, context_instance=context)


@login_required(login_url="/login/")
def game(request, slug):
    context = RequestContext(request)
    content = {}

    try:
        content['game'] = Game.objects.get(slug=slug)
        content['matches'] = Match.objects.filter(game=content['game'], lan=getCurrentLAN())
    except Exception:
        return HttpResponseRedirect(reverse('home'))
    return render_to_response('game.html', content, context_instance=context)


@login_required(login_url="/login/")
def match(request, slug, match_id, command=None):
    context = RequestContext(request)
    content = {}
    if request.user.is_authenticated():
        if request.method == 'POST':
            if command == "register_user":
                register_user_in_match(request)
            elif command == "create_teams":
                create_teams(request)
            elif command == "create_self_team":
                content['msg'] = create_self_team(request)
            elif command == "update_self_team":
                content['msg'] = update_self_team(request)
            elif command == "create_admin_team":
                content['msg'] = create_admin_team(request)
            elif command == "delete_team":
                delete_team(request)
            elif command == "create_tournament":
                create_tournament(request)
            elif command == "entry_round_result":
                entry_round_result(request)
            elif command == "delete_tournament":
                delete_tournament(request)
            return HttpResponseRedirect(reverse('match', args=[slug, match_id]))
        try:
            content['match'] = Match.objects.get(game__slug=slug, id=match_id)
        except Exception:
            content['msg'] = "Seite nicht gefunden!"
    else:
        content['msg'] = "Bitte zuerst einloggen!"
    return render_to_response('match.html', content, context_instance=context)


@csrf_protect
def save_tournament_bracket(request):
    group = Group.objects.get(name="Admin")
    success = False
    msg = ""

    if group in request.user.groups.all():
        json_data = request.POST["json"]
        data = json.loads(json_data)
        match_id = request.POST["match_id"]
        match = Match.objects.get(id=match_id)

        if match.tour_choose_type == "tree":
            match_round = [item for sublist in data["results"][0]
                           for item in sublist]
        elif match.tour_choose_type == "tree_loser":
            match_round = [item for sublist in data["results"][0]
                           for item in sublist]
            match_round.extend(
                [item for sublist in data["results"][1] for item in sublist])
            match_round.extend(
                [item for sublist in data["results"][2] for item in sublist])

        for index, single_round in enumerate(match_round):
            game_round = Round.objects.get(match=match, round_number=index+1)
            if single_round[0] != "None":
                game_round.pkt1 = single_round[0]
            if single_round[1] != "None":
                game_round.pkt2 = single_round[1]
            game_round.save()
        success = True
    else:
        msg = "Nicht ausreichende Rechte zum Editieren."
    response_data = {'success': success, 'msg': msg}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@never_cache
def edit_profile(request):
    context = RequestContext(request)
    error_msg = []
    msg = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            upf = UserProfileForm(
                data=request.POST,
                instance=request.user.userextension,
                prefix='userprofile',
                files=request.FILES
            )
            if upf.is_valid():
                user = request.user
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                #user.userextension.birthdate = request.POST['birthdate']
                try:
                    user.save()
                except Exception as e:
                    error_msg.append(e)

                userprofile = upf.save(commit=False)
                userprofile.user = user
                userprofile.save()
                msg = "Daten erfolgreich aktualisiert."
            else:
                for error in upf.errors.viewvalues():
                    error_msg.append(error)
        else:
            upf = UserProfileForm(prefix='userprofile')
    else:
        return redirect('/login/')
    return render_to_response('edit_profile.html', {'user': request.user, 'userprofileform': upf, 'errors': error_msg, 'msg': msg}, context_instance=context)


def lan_archive(request, slug):
    context = RequestContext(request)
    content = {}

    lan = IntranetMeta.objects.get(lan_id=slug)
    content['lan'] = lan
    content['matches'] = Match.objects.filter(lan=lan).order_by('datetime')

    return render_to_response('lan-archive.html', content, context_instance=context)


@never_cache
@login_required(login_url="/login/")
def logout(request):
    auth_logout(request)
    return redirect('/')
