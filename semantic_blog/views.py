from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from semantic_blog import  helpers
from semantic_blog.forms import ArticleForm
from semantic_blog.models import UserArticleConnection, Article, Tag, Enhancement

@login_required
def index(request):
    user_profile = request.user.userprofile

    ctx = RequestContext(request, {
        'name': user_profile.get_display_name,
        'articles': Article.objects.all(),
        })

    return render_to_response("index.html", ctx)

@login_required
@transaction.commit_on_success
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()

            user_profile = request.user.userprofile

            user_article_conn = UserArticleConnection()
            user_article_conn.article = article
            user_article_conn.user = user_profile
            user_article_conn.connection = UserArticleConnection.AUTHOR
            user_article_conn.save()

            enhancements = helpers.get_article_enhancements(article)

            article.enhancements = enhancements
            article.save()

        return redirect('semantic_blog.views.index')
    else:
        form = ArticleForm()

    ctx = RequestContext(request, {
        'form': form,
        })

    return render_to_response('create_article.html', ctx)

@login_required
def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    user_article_conn = get_object_or_404(UserArticleConnection, \
        article = article, connection = UserArticleConnection.AUTHOR)

    enhancements = article.get_enhancements()

    tags = article.get_tags()

    ctx = RequestContext(request, {
        'article': article,
        'author': user_article_conn.user,
        'enhancements': enhancements,
        'tags': tags,
        })

    return render_to_response('view_article.html', ctx)

@login_required
def find_content(request):
    if request.method == 'POST':
        lookup = request.POST['lookup']

        articles = Article.objects.filter(content__icontains=lookup)[:5]
        tags = Tag.objects.filter(value__icontains=lookup)[:5]

        ctx = RequestContext(request, {
            'articles': articles,
            'tags': tags,
            })

        return render_to_response("find.html", ctx)
    else:
        return redirect('semantic_blog.views.index')
