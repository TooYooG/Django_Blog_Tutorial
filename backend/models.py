from django.db import models


# Create your models here.
class Book(models.Model):

    bookName = models.CharField(max_length=200, verbose_name='书籍名称')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __unicode__(self):
        return self.bookName

    def __str__(self):
        return self.bookName