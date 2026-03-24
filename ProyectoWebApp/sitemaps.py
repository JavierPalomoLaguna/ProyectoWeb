from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'index',
            'servicios',
            'tienda',
            'contacto',
            'blog',
            'politica_privacidad',
            'aviso_legal',
            'politica_cookies',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def location(self, post):
        return reverse('post_detail', args=[post.id])