# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# 可通过 python manage.py inspectdb tb_表名 > app应用名/models.py 将数据库的表转换成模型
from django.db import models


class Subject(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名称')
    intro = models.CharField(max_length=1000, blank=True, null=True, verbose_name='介绍')
    is_hot = models.BooleanField(default=False, verbose_name='是否热门')

    def __str__(self):
        return self.name  # 将学科名字返回让用户更直白的理解

    class Meta:
        managed = False
        db_table = 'tb_subject'
        verbose_name = '学科'
        verbose_name_plural = '学科'

SEX_OPPIONS = (
    (True, '男'),
    (False, '女')
)

class Teacher(models.Model):
    no = models.AutoField(primary_key=True, verbose_name= '编号')
    name = models.CharField(max_length=20, verbose_name= '姓名')
    sex = models.BooleanField(default=True, choices=SEX_OPPIONS,verbose_name='性别')
    birth = models.DateField(verbose_name='出生日期')
    intro = models.CharField(max_length=1000, verbose_name='介绍')
    photo = models.ImageField(max_length=255, verbose_name='照片')
    good_count = models.IntegerField(default=0, db_column='gcount', verbose_name='好评')
    bad_count = models.IntegerField(default=0, db_column='bcount', verbose_name='差评')
    subject = models.ForeignKey(to=Subject, on_delete=models.DO_NOTHING, db_column='sno', verbose_name='所属学科')

    class Meta:
        managed = False
        db_table = 'tb_teacher'
        verbose_name = '教师'
        verbose_name_plural = '教师'




class User(models.Model):
    """用户"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    # 用户密码在数据库中需要哈希摘要进行密码保护
    password = models.CharField(max_length=32, verbose_name='密码')
    tel = models.CharField(max_length=20, verbose_name='手机号码')
    reg_data = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    last_visit = models.DateTimeField(null=True, verbose_name='最后登录时间')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

