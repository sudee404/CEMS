from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Latest Posts"
    link = '/latest-posts/'
    description = 'Updates on new blog posts'
    description_template = "feeds/articles.html"

    def items(self):
        return Post.objects.filter().order_by('publish_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
       
        # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])
