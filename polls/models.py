import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


# 投票应用中需要创建2个模型，分别是”问题“和”选项“
# 问题模型
class Question(models.Model):
    # 设置在Django的后台显示的名字，不设置的话会显示为英文
    objects = None

    class Meta:
        # 单数时显示的内容
        verbose_name = '投票问题'
        # 复数时显示的内容
        verbose_name_plural = '投票问题'

    # “问题”的定义，是django.db.models.Model的子类
    # 有两个字段，分别是question_text和pub_date
    # 都是Field类的实例
    # 字符字段被表示为CharField，日期时间字段被表示为DateTimeField
    # question test和date published是字段的可读名，不影响，只是在数据库表中对其进行描述
    question_text = models.CharField('投票名称', max_length=200)
    pub_date = models.DateTimeField('发布时间')

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently"
    )

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

    # 返回对象的描述信息，这里有描述信息，所有可以直接返回
    # Django自动生成的admin里可以使用这个方法标识对象
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    class Meta:
        verbose_name = '投票选项'
        verbose_name_plural = '投票选项'

    # 选项的定义
    # 有三个字段，分别是question,Choice_text和votes
    # ForeignKey定义了一个关系，每一个Choice对象都关联一个Question对象
    # Django支持所有常用数据库关系：1V1，1VN，NVN。
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='投票问题')
    choice_text = models.CharField('选项名', max_length=200)
    # 将votes的default的默认值设置0
    votes = models.IntegerField('投票数量', default=0)

    def __str__(self):
        return self.choice_text
