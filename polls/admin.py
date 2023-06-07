from django.contrib import admin
from .models import Question, Choice


# Register your models here.
# ChoiceInline是一个内联表单，继承于admin.StackedInline，表示内联表单以堆叠方式展示
# 将admin.StackedInline改为TabularInline，关联对象以一种表格式的方式展示，显得更加紧凑
class ChoiceInline(admin.TabularInline):
    # model = Choice 表示内联表单是用于展示Choice模型类的视图
    model = Choice
    # 表示初始有3个格外的空选项，即用于添加新的选项
    extra = 2


# 定义QuestionAdmin的模型管理类，用于管理Question模型的数据
class QuestionAdmin(admin.ModelAdmin):
    # fieldsets是一个列表，定义表单中显示的字段集合
    # 列表的每一项是一个元组，每个元组的第一个字段表示这个字段集合的名字
    fieldsets = [
        ("文本数据", {"fields": ["question_text"]}),
        ("日期信息", {"fields": ["pub_date"]})
        ]
    # inlines也是一个列表，定义内联关系，这里定义了一个ChoiceInline类，
    # 表示在Question编辑页面中，可以直接编辑与之关联的Choice对象
    inlines = [ChoiceInline]
    # list_display是一个元组。将要显示的显示的字段名添加到这个元组中，在更改列页中以列的形式展现这个对象
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # 新增一个显示过滤去，以”pub_date"为条件过滤问题
    list_filter = ["pub_date"]
    # 定义一个搜索框
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
