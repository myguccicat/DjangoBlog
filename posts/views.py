from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post


# Create your views here.


def index(request):
    article_records = Post.objects.all()
    article_list = list()
    for count, article in enumerate(article_records):
        article_list.append("#{}: {}<br><hr>".format(str(count), str(article)))
    return HttpResponse(article_list)
