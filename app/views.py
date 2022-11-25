import uuid
from random import randint
from datetime import datetime, time, timedelta
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.forms.models import model_to_dict
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Delivery


def resp(data, msg="ok", code=0):
    return JsonResponse({"code": code, "message": msg, "data": data})


def randcode():
    return "".join([str(randint(0, 9)) for i in range(4)])


def register(request):
    username = request.POST["username"]
    passwd = request.POST["passwd"]
    user = User.objects.create_user(username=username, password=passwd)
    try:
        user.save()
        return resp(None, u"注册成功")
    except:
        return resp(None, u"注册失败", 1)


def login_view(request):
    username = request.POST["username"]
    passwd = request.POST["passwd"]
    user = authenticate(username=username, password=passwd)
    if user is None:
        return resp(None, u"登录失败", 1)
    login(request, user)
    return resp(None, u"登录成功")


@login_required
def logout_view(request):
    logout(request)
    return resp(None, u"您已成功登出")


def login_check(request):
    user = request.user
    print("###check_login", user)
    if user.username:
        print("###has username")
        return resp(user.username)
    print("###empty username")
    return resp(None, u"您尚未登录", 1)


@login_required
def deposit(request):
    deposit_username = request.user.username
    pickup_username = request.POST["pickup_username"]
    if not User.objects.filter(username=pickup_username).exists():
        return resp(None, u"无效的取件人", 1)
    if Delivery.objects.filter(
            device_id=request.POST["device_id"],
            cabinet_no=int(request.POST["cabinet_no"]),
            state__lte=1).exists():
        return resp(None, u"该柜已被占用", 2)
    print("###deposit", deposit_username, pickup_username)
    delivery = Delivery(
        deposit_username=deposit_username,
        pickup_username=pickup_username,
        device_id=request.POST["device_id"],
        cabinet_no=int(request.POST["cabinet_no"])
    )
    delivery.save()
    return resp(None, u"存件申请已提交")


@login_required
def pickup(request):
    d = Delivery.objects.get(id=int(request.POST["id"]))
    if request.user.username != d.pickup_username:
        return resp(None, u"您不是取件人", 1)
    d.state = 2
    d.save()
    return resp(None, u"取件申请已提交")


@login_required
def deposit_list(request):
    dels = Delivery.objects.filter(
        deposit_username=request.user.username
    ).order_by("moment")
    del_dicts = list(map(model_to_dict, dels))
    return resp(del_dicts)


@login_required
def pickup_list(request):
    dels = Delivery.objects.filter(
        pickup_username=request.user.username
    ).order_by("moment")
    del_dicts = list(map(model_to_dict, dels))
    return resp(del_dicts)


@login_required
def open_list(request):
    deposit_dels = Delivery.objects.filter(
        device_id=request.user.username, state=0)
    pickup_dels = Delivery.objects.filter(
        device_id=request.user.username, state=2)
    results = []
    deposit_del_dicts = list(map(model_to_dict, deposit_dels))
    results.extend(deposit_del_dicts)
    pickup_del_dicts = list(map(model_to_dict, pickup_dels))
    results.extend(pickup_del_dicts)
    deposit_dels.update(state=1)
    pickup_dels.update(state=3)
    return resp(results)


@login_required
def clear(request):
    if request.user.username != "hyf":
        return resp(None, u"您不是管理员", 1)
    Delivery.objects.all().delete()
    return resp(None, u"重置成功")


def test(request):
    return resp("this is a test api")
