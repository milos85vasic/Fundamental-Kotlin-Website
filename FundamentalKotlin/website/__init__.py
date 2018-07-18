from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = SignedCookieSessionFactory('fUnDam3nTll77')
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.include('pyramid_jinja2')
    config.include('pyramid_useragent')
    config.add_static_view('assets', 'assets', cache_max_age=3600)
    config.add_route('css_main', '/css/main.css')
    config.add_route('home', '/')
    config.add_route('contact', '/contact')
    config.add_route('json_toc', '/json/toc')
    config.add_route('pages', '/pages/{page}')
    config.add_route('newsletter', '/newsletter')
    config.add_route('newsletter_subscribe', '/newsletter/subscribe')
    config.add_route('redirect_author', '/api/redirect/author')
    config.add_route('redirect_code_examples', '/api/redirect/code/')
    config.add_route('redirect_social', '/api/redirect/social/{network}')
    config.add_route('redirect_sample_chapters', '/api/redirect/sample/chapters/{chapter}')
    config.scan()
    return config.make_wsgi_app()
