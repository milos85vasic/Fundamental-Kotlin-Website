# coding=utf-8
import os

import xmltodict
import datetime


def get_date():
    today = datetime.date.today()
    return today.strftime('%B %Y')


def get_toc():
    script_dir = os.path.dirname(__file__)
    with open(script_dir + '/assets/toc.ncx', 'r') as toc_file:
        toc_data = toc_file.read()
    xml_dict = xmltodict.parse(toc_data)
    return xml_dict


configuration = {
    "shared": {
        "website_version": "2.0",
        "author": u'Miloš Vasić',
        "date": get_date(),
        "static": "http://static.fundamental-kotlin.com/",
        "author_website": "/api/redirect/author",
        "isbn": "9788692030710",
        "footer_menu": [
            {
                "title": "Terms and Conditions",
                "href": "/pages/terms"
            },
            {
                "title": "Privacy Policy",
                "href": "/pages/privacy"
            },
            {
                "title": "Refund Policy",
                "href": "/pages/refund"
            }
        ],
        "social": {
            "facebook": "https://www.facebook.com/fundamental.kotlin/",
            "twitter": "https://twitter.com/fund_kotlin",
            "tumblr": "http://fundamentalkotlin.tumblr.com/",
            "google": "https://plus.google.com/104225421274450956155",
            "instagram": "https://www.instagram.com/fundamentalkotlin/",
            "linkedin": "https://www.linkedin.com/in/milos-vasic-53778682",
            "xing": "https://www.xing.com/profile/Milos_Vasic4",
            "pinterest": "https://www.pinterest.com/milosvasic85/",
            "goodreads": "https://www.goodreads.com/book/show/32307194-fundamental-kotlin"
        }
    },
    "home": {
        "title": "Fundamental Kotlin",
        "description": "Fundamental Kotlin, 1st Edition.",
        "keywords": "Kotlin, Programming, Programming language, Fundamental, Basics, Book, eBook, Learn",
        "book_author": u'Miloš Vasić',
        "book_title": "Fundamental Kotlin",
        "book_edition": "1st Edition",
        "book_revision": "3",
        "pages": [
            {
                "title": "Home",
                "anchor": "home",
                "content": "home",
                "secondary_content": "formats",
                "image": "Cover.jpg",
                "image_alt": "Fundamental Kotlin - 1st Edition"
            },
            {
                "title": "Table of Contents",
                "anchor": "contents",
                "content": "contents",
                "image": "SecEd_ProjectStructure.png",
                "image_alt": "Project structure"
            },
            {
                "title": "Code Examples",
                "anchor": "code",
                "content": "code",
                "image": "CodeExamples.png",
                "image_alt": "Code Examples"
            },
            {
                "title": "Buy",
                "anchor": "buy",
                "content": "buy",
                "image": "Buy.png",
                "image_alt": "Shopping cart",
                "extra_classes": ["buy_highlight"]
            },
            {
                "title": "Contact",
                "anchor": "contact",
                "content": "contact",
                "image": "Contact.png",
                "image_alt": "Fundamental Kotlin - 1st Edition"
            },
            # {
            #     "title": "Newsletter",
            #     "href": "/newsletter"
            # },
            {
                "title": "About the Author",
                "content": "author",
                "image": "Author.png",
                "image_alt": "Fundamental Kotlin - 1st Edition"
            }
        ]
    },
    "terms": {
        "title": "Terms and Conditions",
        "description": "Website and Fundamental Kotlin eBook terms and conditions.",
        "keywords": "Terms, Conditions, Rules",
        "pages": [
            {
                "title": "Terms and Conditions",
                "content": "terms"
            }
        ]
    },
    "refund": {
        "title": "Refund Policy",
        "description": "Policy about money refund.",
        "keywords": "Refund, Policy, Money, Back",
        "pages": [
            {
                "title": "Refund Policy",
                "content": "refund"
            }
        ]
    },
    "privacy": {
        "title": "Privacy Policy",
        "description": "Privacy and security policy.",
        "keywords": "Privacy, Security, Safety, Policy, Users",
        "pages": [
            {
                "title": "Privacy Policy",
                "content": "privacy"
            }
        ]
    },
    "newsletter": {
        "title": "Subscribe to Newsletter",
        "description": "Subscribe to Newsletter and receive news about new releases and publications.",
        "keywords": "Newsletter, Subscribe, News, Releases, Mailing list",
        "pages": [
            {
                "title": "Subscribe to Newsletter",
                "content": "newsletter"
            }
        ]
    }
}

sample_chapters = [
    {
        "title": "About Fundamental Series",
        "url": "sec_ed_about_fundamental_series.pdf"
    },
    {
        "title": "What is Kotlin?",
        "url": "sec_ed_what_is_kotlin.pdf"
    },
    {
        "title": "Basic characteristics",
        "url": "sec_ed_basic_characteristics.pdf"
    },
    {
        "title": "Hello from Kotlin!",
        "url": "sec_ed_hello_from_kotlin.pdf"
    },
    {
        "title": "Inheritance",
        "url": "sec_ed_inheritance.pdf"
    },
    {
        "title": "Interfaces",
        "url": "sec_ed_interfaces.pdf"
    }
]
