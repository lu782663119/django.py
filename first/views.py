from itertools import count
from django.shortcuts import render, redirect
from urllib.parse import unquote

# Create your views here.
from random import sample
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
# 视图函数（接收来自浏览器的用户请求，然后返回一个）
from first.captcha import Captcha
from first.models import Subject, Teacher, User
from first.utils import gen_random_code, gen_md5_digest


def show_subjects(request:HttpRequest):
    subjects = Subject.objects.all().order_by('no')  # 学科通过编号从大到小排序

    return render(request, 'subjects.html', {
        'subjects': subjects
    })

def show_teachers(request:HttpRequest) -> HttpResponse:
    # 捕获一个超过编号范围的异常，防止程序崩溃
    try:
        sno = int(request.GET.get('sno', 0))    # 获取学科的编号
        teachers = []
        if sno:
            subject = Subject.objects.only('name').get(no=sno)     # 获取学科所处编号
            teachers = Teacher.objects.filter(subject=subject).order_by('no')        # 通过学科编号查询所属的老师
        return render(request, 'teachers.html', {
        'subject': subject,
        'teachers': teachers
         })
    except (ValueError, Subject.DoesNotExist):
        return redirect('/')




def praise_or_criticize(request: HttpRequest):    # 好评点赞刷新代码
    if request.session.get('userid'):
        try:
            sno = request.GET.get('sno') # 获取学科编号
            tno = request.GET.get('tno')  # 获取老师编号
            teacher = Teacher.objects.get(no=tno)   # 获取老师的编号
            if request.path.startswith('/praise/'):
                teacher.good_count += 1
                count = teacher.good_count
            else:
                teacher.bad_count += 1
                count = teacher.bad_count
            teacher.save()
            data = {'code':20000, 'mesg': '投票成功', 'count': count}  # 返回当前页面
        except (ValueError, Teacher.DoesNotExist):
            data = {'code':20001, 'mesg': '投票失败'}
    else:
        data = {'code': 20002, 'mesg': '请先登录再投票'}
    return JsonResponse(data)



def get_captcha(request: HttpRequest):
    captcha_txt = code = gen_random_code()
    request.session['captcha'] = captcha_txt
    image_data = Captcha.instance().generate(code)
    return HttpResponse(image_data, content_type='image/png')


def login(request: HttpRequest):   # 根据不同得请求方法来执行渲染还是登录
    hint, backurl = '', request.GET.get('backurl', '/')
    if request.method == 'POST':
        backurl = request.POST.get('backurl', '/')  # 获取表单返回的URL链接
        if backurl != '/':
            backurl = unquote(backurl)   # 如果返回的表单URL不为空 则跳转回之前的页面
        captcha_from_serv = request.session.get('captcha', '0')
        captcha_from_user = request.POST.get('captcha', '1').lower()
        if captcha_from_serv == captcha_from_user:
            username = request.POST.get('username')  # 获取用户名
            password = request.POST.get('password')  # 获取密码
            if username and password:
                password = gen_md5_digest(password)
                user = User.objects.filter(username=username, password=password).first()
                if user:
                    request.session['userid'] = user.no     # 将用户ID存储到COOKIE
                    request.session['username'] = user.username
                    return redirect('/')
                else:
                    hint = '用户名或密码错误'
            else:
                hint = '请输入有效的用户名和密码'
        else:
            hint = '验证码错误'
    return render(request, 'login.html', {'hint': hint, 'backurl': backurl}, ) # 传输一个错误信息


def register(request: HttpRequest):  # 根据不同得请求方法来执行渲染还是注册
    if request.method == 'POST':
        pass
    return render(request, 'register.html')


def logout(request: HttpRequest):
    request.session.flush()
    return redirect('/')
