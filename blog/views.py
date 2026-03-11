from django.shortcuts import render, get_object_or_404
from blog.models import Post, Categoria

def blog(request):
    posts = Post.objects.prefetch_related('categorias').order_by('orden')
    categorias_unicas = {}
    for post in posts:
        for cat in post.categorias.all():
            categorias_unicas[cat.nombre] = cat

    context = {
        'posts': posts,
        'categorias_unicas': categorias_unicas.values(),
        'meta_title': 'Blog de Desarrollo Web y Marketing Digital | Código Vivo Studio',
        'meta_description': 'Consejos sobre desarrollo web, tiendas online y posicionamiento SEO para restaurantes y comercios.',
    }
    return render(request, 'blog/blog.html', context)

def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    posts = Post.objects.filter(categorias=categoria)
    context = {
        "categoria": categoria,
        "posts": posts,
        'meta_title': f'{categoria.nombre} - Blog | Código Vivo Studio',
        'meta_description': f'Artículos sobre {categoria.nombre}. Consejos y noticias del sector.',
    }
    return render(request, "blog/categoria.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'meta_title': f'{post.titulo} | Código Vivo Studio',
        'meta_description': post.contenido[:155],
    }
    return render(request, 'blog/post_detail.html', context)