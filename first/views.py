from django.shortcuts import render, redirect

# Create your views here.
from random import sample
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
# 视图函数（接收来自浏览器的用户请求，然后返回一个）
from first.models import Subject, Teacher


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
    try:
        sno = request.GET.get('sno')  # 获取学科编号
        tno = request.GET.get('tno')  # 获取老师编号
        teacher = Teacher.objects.get(no=tno)   # 获取老师的编号
        if request.path.startswith('/praise/'):
            teacher.good_count += 1
        else:
            teacher.bad_count += 1
        teacher.save()
        return redirect(f'/teachers/?sno={sno}')  # 返回当前页面
    except (ValueError, Teacher.DoesNotExist):
        return redirect('/')


def login(request: HttpRequest):
    return render(request, 'login.html')

