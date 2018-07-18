from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from configuration import *
from pyga.requests import Page, Session, Visitor
from configuration_parameters import *

required = "~ Required !"
visitor = Visitor()
session = Session()


@view_config(route_name='css_main', renderer='templates/css/main.jinja2')
def css_main(request):
    request.response.content_type = 'text/css'
    return {
        'configuration': configuration,
        'mobile': is_mobile(request)
    }


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    track_page(request.remote_addr, "/")
    return {
        'configuration': configuration,
        'mobile': is_mobile(request)
    }


@view_config(route_name='pages', renderer='templates/page.jinja2')
def pages(request):
    try:
        page = request.matchdict['page']
    except KeyError:
        return go_home(request)
    if page:
        track_page(request.remote_addr, request.path)
    return {
        'page': page,
        'configuration': configuration,
        'mobile': is_mobile(request)
    }


@view_config(route_name='newsletter', renderer='templates/page.jinja2')
def newsletter(request):
    track_page(request.remote_addr, request.path)
    return {
        'page': 'newsletter',
        'configuration': configuration,
        'mobile': is_mobile(request)
    }


@view_config(route_name='json_toc', renderer='json')
def json_toc(request):
    return {
        'toc': get_toc(),
        'sample_chapters': sample_chapters,
        'mobile': is_mobile(request)
    }


@view_config(route_name='redirect_code_examples')
def redirect_code_examples(request):
    track_page(request.remote_addr, request.path)
    url = configuration['shared']['static'] + "code/Fundamental-Kotlin.zip"
    return HTTPFound(location=url)


@view_config(route_name='redirect_author')
def redirect_author(request):
    track_page(request.remote_addr, request.path)
    url = 'http://www.milosvasic.net'
    return HTTPFound(location=url)


@view_config(route_name='redirect_social')
def redirect_social(request):
    try:
        network = request.matchdict['network']
    except KeyError:
        return go_home(request)
    try:
        network_url = configuration['shared']['social'][network]
    except KeyError:
        return go_home(request)
    if network_url:
        track_page(request.remote_addr, request.path)
        return HTTPFound(location=network_url)
    else:
        return go_home(request)


@view_config(route_name='redirect_sample_chapters')
def redirect_sample_chapters(request):
    chapter_url = None
    try:
        chapter = request.matchdict['chapter']
    except KeyError:
        return go_home(request)
    for chapter_item in sample_chapters:
        if chapter_item['url'] == chapter:
            chapter_url = configuration['shared']['static'] + "sample_chapters/" + chapter

    if chapter_url:
        track_page(request.remote_addr, request.path)
        return HTTPFound(location=chapter_url)
    else:
        return go_home(request)


@view_config(context=HTTPNotFound)
def not_found(request):
    page_to_track = "/error/404" + request.path
    track_page(request.remote_addr, page_to_track)
    return go_home(request)


def track_page(ip, page):
    visitor.ip_address = ip
    page = Page(page)
    tracker.track_pageview(page, session, visitor)


def go_home(request):
    url = request.route_url('home')
    return HTTPFound(location=url)


def is_mobile(request):
    client = request.user_agent_classified
    return client.is_mobile or client.is_tablet
