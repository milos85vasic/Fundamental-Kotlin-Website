import hashlib
import random
import smtplib
import string
from email.mime.text import MIMEText

from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.view import view_config
from validate_email import validate_email
from configuration import *
from pyga.requests import Page, Session, Visitor
from configuration_parameters import *

required = "~ Required !"
visitor = Visitor()
session = Session()


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


@view_config(route_name='newsletter_subscribe', renderer='json')
def newsletter_subscribe(request):
    captcha = required
    name = required
    email = required
    message_return = []
    message_title = "To subscribe to newsletter please correct the following:"
    validation_failed = {}
    validation_values = {}
    subscription_result = False

    try:
        captcha = request.POST['captcha']
        captcha = captcha.strip()
        name = request.POST['name'].strip()
        name = name.strip()
        email = request.POST['email'].strip()
        email = email.strip()
    except KeyError:
        pass

    if email and email != required:
        validation_values["email"] = email
        is_valid = validate_email(email)
        if not is_valid:
            message_return.append("- Enter valid email address")
            validation_failed["email"] = True
    else:
        if name != required and captcha != required:
            message_return.append("- Fill email address field")
            validation_failed["email"] = True

    if name != required:
        validation_values["name"] = name
        if not name:
            message_return.append("- Fill the name field with your full name")
            validation_failed["name"] = True

    if captcha != required:
        if not captcha:
            message_return.append("- Enter captcha letters shown")
            validation_failed["captcha"] = True
        else:
            if ''.join(request.session['captcha_letters']).lower() != captcha.lower():
                message_return.append("- You entered invalid captcha code.")
                validation_failed["captcha"] = True

    # no validation errors and all fields filled
    send_condition = not validation_failed and \
                     name != required and \
                     email != required and \
                     captcha != required

    if send_condition:
        try:
            you = contact_email
            message = "User subscribed to newsletter: " + email
            msg = MIMEText(message)
            msg['Subject'] = "New newsletter subscription by " + name
            msg['From'] = email
            msg['To'] = you
            s = smtplib.SMTP('mail.fundamental-kotlin.com')
            s.login(you, smtp_password)
            s.sendmail(email, [you], msg.as_string())
            s.quit()
            subscription_result = True
            message_title = "You successfully subscribed. Thank you!"
            track_page(request.remote_addr, "/newsletter/subscribe/success")
        except smtplib.SMTPException:
            message_title = "We could not subscribe you. Please try again later. Thank you!"
            track_page(request.remote_addr, "/newsletter/subscribe/failed")

    captcha_images = []
    captcha_letters = []
    for num in range(1, 10):
        captcha_letters.append(random.choice(string.ascii_letters).lower())

    request.session['captcha_letters'] = captcha_letters

    for letter in captcha_letters:
        letter_name = letter + "_0001.png"
        hash_object = hashlib.md5((letter_name + salt).encode())
        captcha_images.append(hash_object.hexdigest() + ".png")

    track_page(request.remote_addr, request.path)
    return {
        'captcha': captcha_images,
        'message': message_return,
        'message_title': message_title,
        'subscription_result': subscription_result,
        'validation_failed': validation_failed,
        'validation_values': validation_values,
        'mobile': is_mobile(request)
    }


# @view_config(route_name='contact', renderer='json')
# def contact(request):
#     captcha = required
#     name = required
#     email = required
#     message = required
#     message_return = []
#     message_title = "To send your message please correct the following:"
#     validation_failed = {}
#     validation_values = {}
#
#     try:
#         captcha = request.POST['captcha']
#         captcha = captcha.strip()
#         name = request.POST['name'].strip()
#         name = name.strip()
#         email = request.POST['email'].strip()
#         email = email.strip()
#         message = request.POST['message'].strip()
#         message = message.strip()
#     except KeyError:
#         pass
#
#     if email and email != required:
#         validation_values["email"] = email
#         is_valid = validate_email(email)
#         if not is_valid:
#             message_return.append("- Enter valid email address")
#             validation_failed["email"] = True
#     else:
#         if name != required and message != required and captcha != required:
#             message_return.append("- Fill email address field")
#             validation_failed["email"] = True
#
#     if name != required:
#         validation_values["name"] = name
#         if not name:
#             message_return.append("- Fill the name field with your full name")
#             validation_failed["name"] = True
#
#     if message != required:
#         validation_values["message"] = message
#         if not message:
#             message_return.append("- Enter the content for your message")
#             validation_failed["message"] = True
#
#     if captcha != required:
#         if not captcha:
#             message_return.append("- Enter captcha letters shown")
#             validation_failed["captcha"] = True
#         else:
#             if ''.join(request.session['captcha_letters']).lower() != captcha.lower():
#                 message_return.append("- You entered invalid captcha code.")
#                 validation_failed["captcha"] = True
#
#     # no validation errors and all fields filled
#     send_condition = not validation_failed and \
#                      name != required and \
#                      email != required and \
#                      message != required and \
#                      captcha != required
#
#     if send_condition:
#         try:
#             you = contact_email
#             msg = MIMEText(message)
#             msg['Subject'] = 'Message from Fundamental Kotlin website by: ' + name
#             msg['From'] = email
#             msg['To'] = you
#             s = smtplib.SMTP('mail.fundamental-kotlin.com')
#             s.login(you, smtp_password)
#             s.sendmail(email, [you], msg.as_string())
#             s.quit()
#             message_title = "You successfully emailed us. Thank you!"
#             track_page(request.remote_addr, "/contact/success")
#         except smtplib.SMTPException:
#             track_page(request.remote_addr, "/contact/failed")
#             message_title = "We could not send your message. Please come back later. Thank you!"
#
#     captcha_images = []
#     captcha_letters = []
#     for num in range(1, 10):
#         captcha_letters.append(random.choice(string.ascii_letters).lower())
#
#     request.session['captcha_letters'] = captcha_letters
#
#     for letter in captcha_letters:
#         letter_name = letter + "_0001.png"
#         hash_object = hashlib.md5((letter_name + salt).encode())
#         captcha_images.append(hash_object.hexdigest() + ".png")
#
#     return {
#         'captcha': captcha_images,
#         'message_title': message_title,
#         'message': message_return,
#         'validation_failed': validation_failed,
#         'validation_values': validation_values,
#         'mobile': is_mobile(request)
#     }


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
