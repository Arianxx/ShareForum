import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from uuslug import slugify

from .common_tools import crop_img, delete_img


# Create your models here.

class Book(models.Model):
    """
    它和计票模型（Poll）是一对一关系。这个关系在Poll模型中定义，因为书籍id是计票模型的外键，以便删除时的一致性。因此不会存在没有引用书籍的计
    票模型对象。
    它还和讨论模型（Discuss)拥有一对多关系。
    """
    # TODO: 增加查看次数信息
    name = models.CharField('书籍名称', max_length=32)
    pub_date = models.DateField('出版日期', default=timezone.now, blank=True, null=True)
    slug = models.SlugField(max_length=64, unique=True)
    intro = models.TextField('简介', max_length=1280, blank=True)
    cover = models.ImageField('封面', upload_to='book_cover/%Y/%m/%d', default="book_cover/default.jpg", blank=True)

    publishing = models.ForeignKey("Publishing", on_delete=models.CASCADE, related_name="books", null=True)
    auther = models.ForeignKey("Auther", on_delete=models.CASCADE, related_name="books")
    tags = models.ManyToManyField("Tag", related_name="books")

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = '书籍'
        ordering = ['pub_date']
        unique_together = ['name', 'auther', ]

    def __str__(self):
        return "Book(%s)" % self.name

    def save(self, *args, **kwargs):
        cover_default_path = self.cover.field.default.replace('/', '\\')
        if not cover_default_path in self.cover.path:
            origin_book = Book.objects.get(slug=self.slug)
            if origin_book.cover.path != self.cover.path:
                # 如果要更改封面，就删除原来的封面
                try:
                    os.remove(origin_book.cover.path)
                except FileNotFoundError:
                    pass

        ret = super(Book, self).save(*args, **kwargs)

        # 自动根据书籍的名称和作者添加一个slug
        slug = '-by-'.join([self.name, self.auther.name])
        self.slug = slugify(slug)

        # 保存书籍时，一并保存它的计票对象（Poll），从而不用手动去创建计票对象。
        try:
            self.__getattribute__("poll")
        except AttributeError:
            poll = Poll(book=self)
            poll.save()

        if not cover_default_path in self.cover.path:
            # 不剪裁默认封面
            COVER_WIDTH = getattr(settings, 'COVER_WIDTH', 210)
            COVER_HEIGHT = getattr(settings, 'COVER_HEIGHT', 280)
            crop_img(self.cover, COVER_WIDTH, COVER_HEIGHT)

        return ret

    def delete(self, *args, **kwargs):
        # 删除书籍时，一并删除它储存在本地的封面图片
        default_path = self.cover.field.default.replace('/', '\\')
        if not default_path in self.cover.path:
            delete_img(self.cover)

        return super().delete(*args, **kwargs)


class Auther(models.Model):
    """
    与书籍模型（Book）是多对一关系。关系在Book中定义。
    """
    name = models.CharField('作者名', max_length=32, unique=True)
    about = models.TextField('关于作者', max_length=1280, blank=True)
    slug = models.SlugField(max_length=32, unique=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'

    def __str__(self):
        return "Auther(%s)" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        ret = super(Auther, self).save(*args, **kwargs)
        return ret

    @property
    def book_num(self):
        return self.books.count()


class Publishing(models.Model):
    """
    与书籍模型（Book）是多对一关系。关系在Book中定义。
    """
    name = models.CharField('出版社名', max_length=32, unique=True)
    establish_date = models.DateField('创建日期', null=True, blank=True)
    about = models.TextField('关于出版社', max_length=1024, blank=True)
    slug = models.SlugField(max_length=32, unique=True)

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = '出版社'

    def __str__(self):
        return "Publishing(%s)" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        ret = super(Publishing, self).save(*args, **kwargs)
        return ret

    @property
    def book_num(self):
        return self.books.count()


class Tag(models.Model):
    """
    与书籍模型（Book)是多对多关系。关系在Book中定义。
    """
    name = models.CharField('标签名', max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)

    class Meta:
        verbose_name = '书籍标签'
        verbose_name_plural = '书籍标签'

    def __str__(self):
        return "Tag(%s)" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        ret = super(Tag, self).save(*args, **kwargs)
        return ret

    @property
    def book_num(self):
        return self.books.count()


class Poll(models.Model):
    """
    计票模型。保存了赞同和反对的信息。
    """
    # TODO:使用django内置的user对象来投票，并记录投票人。
    up = models.IntegerField('赞同', default=0)
    down = models.IntegerField('反对', default=0)
    book = models.OneToOneField("Book", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '投票信息'
        verbose_name_plural = '投票信息'

    def __str__(self):
        return "Poll(book:%s, up:%d, down:%d)" % (self.book.name, self.up, self.down)


class Carousel(models.Model):
    """
    存放首页滚动图
    """
    img = models.ImageField("滚动图", upload_to='carousel/%Y/%d/%d')
    name = models.CharField('图片名字', max_length=32, blank=True)
    title = models.CharField('展示标题', max_length=128, blank=True)
    intro = models.TextField('展示介绍', max_length=128, blank=True)
    link = models.URLField("链接地址", blank=True)

    class Meta:
        verbose_name = '滚动图'
        verbose_name_plural = '滚动图'

    def __str__(self):
        return 'Carousel(name:%s, dir=%s)' % (self.name, str(self.img))

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)

        # TODO: 头图长宽的变量
        CAROUSEL_WIDTH = getattr(settings, 'CAROUSEL_WIDTH', 1600)
        CAROUSEL_HEIGHT = getattr(settings, 'CAROUSEL_HEIGHT', 900)
        crop_img(self.img, CAROUSEL_WIDTH, CAROUSEL_HEIGHT)

        return ret

    def delete(self, *args, **kwargs):
        delete_img(self.img)

        return super().delete(*args, **kwargs)
