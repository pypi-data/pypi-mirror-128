"""
    test_domonic
    ~~~~~~~~~~~~
    - unit tests for domonic.dom

"""

import unittest
# import requests
# from mock import patch

from domonic.html import *
from domonic.style import *
from domonic.dom import *
from domonic import *


class TestCase(unittest.TestCase):
    """ Tests for the dom package """

    def setUp(self):
        # can be used by all tests
        self.page = html(
            head(
                meta(_charset="utf-8"),
                meta(**{"_http-equiv": "X-UA-Compatible"}, _content="IE=edge"),
                title('website.com'),
                meta(_name="description", _content=""),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="robots", _content="all,follow"),
                link(_rel="stylesheet", _href="static/css/bootstrap.min.css"),
                link(_rel="shortcut icon", _href="favicon.png")
            ),
            body(
                div(_class="overlay").html(
                    div(_class="content h-100 d-flex align-items-center").html(
                        div(_class="container text-center text-black").html(
                            p("Welcome to the information age", _class="headings-font-family text-uppercase lead"),
                            h1("We are", span("COMPANY", _class="font-weight-bold d-block"), _class="text-uppercase hero-text text-black"),
                            p("And this is our company website", _class="headings-font-family text-uppercase lead")
                        )
                    )
                ),
                header(_class="header sticky-top").html(
                    nav(_class="navbar navbar-expand-lg bg-white border-bottom py-0").html(
                        div(_class="container").html(
                            h6("website.com"),
                            div(_id="navbarSupportedContent", _class="collapse navbar-collapse").html(
                                ul(_class="navbar-nav ml-auto px-3").html(
                                    li(a("Home", _href="", _class="nav-link text-uppercase link-scroll"), _class="nav-item active"),
                                    li(a("About", _href="#about", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Services", _href="#services", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Team", _href="#team", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Contact", _href="#contact", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                )
                            )
                        )
                    )
                ),
                section(_id="about", _class="about").html(
                    div(_class="container").html(
                        div(_class="row mb-5").html(
                            div(_class="col-lg-12").html(
                                header(_style="padding-top:20px;").html(
                                    h6("About us", _class="lined text-uppercase"),
                                ),
                                p("Specialists in xxxxx.", _class="lead"),
                                p("COMPANY can provide xxxxxx solutions. We have expertise in the following areas."),
                                div(_class="row").html(
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("A"),
                                            li("B"),
                                            li("C"),
                                        )
                                    ),
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("1"),
                                            li("2"),
                                            li("3"),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                div(_class="row text-white text-center", _style="background: url(static/img/header.jpg); padding:20px;").html(
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),

                ),
                section(_id="services", _class="bg-gray").html(
                    div(_class="container").html(
                        header(_class="text-center mb-5").html(
                            #  h2("Services", _class="lined text-uppercase"),
                        ),
                        div(_class="row text-center").html(
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                        )
                    ),
                    section(_id="team").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                # h2("Our team", _class="text-uppercase lined"),
                            ),
                            div(_class="row text-center").html(
                                # div(_class="col-lg-3 col-md-6 mb-4").html(
                                div(_class="col-lg-12").html(
                                    img(_src="static/img/gol.gif", _alt="Username", _class="img-fluid mb-4", _width="300px;", _height="300px;"),
                                    h4(_class="font-weight-bold text-uppercase").html(
                                        a("Username", _href="#", _class="no-anchor-style")
                                    ),
                                    p("Director", _class="small text-gray text-uppercase"),
                                ),
                            )
                        )
                    ),
                    section(_id="contact").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                #  h2("Contact", _class="text-uppercase lined"),
                            ),
                            div(_class="row").html(
                                div(_class="col-lg-12 text-center").html(
                                    p(
                                        "Email : ",
                                        a("user@website.com", _href="mailto:user@website.com"),
                                        br(),
                                        "or Call us on : ",
                                        a("123456789", _href="tel:123456789")
                                    ),
                                    ul(_class="mb-0 list-inline text-center").html(
                                        li(a(i(_class="fab fa-twitter"), _href="https://twitter.com/user", _class="social-link social-link-twitter"), _class="list-inline-item"),
                                        li(a(i(_class="fab fa-linkedin"), _rel="nofollow", _href="https://www.linkedin.com/in/user/", _class="social-link social-link-instagram"), _class="list-inline-item"),
                                        li(a(i(_class="fas fa-envelope"), _href="mailto:user@website.com", _class="social-link social-link-email"), _class="list-inline-item")
                                    )
                                )
                            )
                        )
                    ),
                    footer(_style="padding:20px;").html(
                        div(_class="row text-center").html(
                            div(_class="col-lg-12 text-center").html(
                                p("Copyright &copy; 2021 COMPANY. All rights Reserved.", _class="mb-0 text-gray"),
                            )
                        )
                    ),
                    script(_src="static/js/jquery.min.js"),
                    link(_rel="stylesheet", _href="https://use.fontawesome.com/releases/v5.7.1/css/all.css", _integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr", _crossorigin="anonymous")
                )
            )
        )

    def test_NodeList(self):
        nlist = self.page.body.childNodes
        assert isinstance(nlist, NodeList)
        # assert len(nlist) == 1
        # test Nodelist methods and properties. foreach, entries, keys, values
        node = document.createElement("div")
        kid1 = document.createElement("p")
        kid2 = document.createTextNode("hey")
        kid3 = document.createElement("span")
        node.appendChild(kid1)
        node.appendChild(kid2)
        node.appendChild(kid3)
        somelist = node.childNodes
        for each in somelist.values():
            print(each)
        # <p>
        # #text "hey"
        # <span>
        # https://developer.mozilla.org/en-US/docs/Web/API/NodeList/values
        # TODO - output should be no close tag and a hash say text?
        for each in somelist.keys():
            print(each)
        somelist.forEach(
            lambda currentValue, currentIndex, listObj, **kwargs: print(currentValue, currentIndex, kwargs),
            'myThisArg'
        )
        for each in somelist.entries():
            print(each)
        # Array [ 0, <p> ]
        # Array [ 1, #text "hey" ]
        # Array [ 2, <span> ]
        # print(somelist.item(0))
        # print(somelist.item(1))
        # print(somelist.item(2))
        assert somelist.item(0) == kid1
        assert somelist.item(1) == kid2
        assert somelist.item(2) == kid3

    def test_Node(self):

        n = Node()
        self.assertIsInstance(n, Node)
        # n.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        # n.baseURI = 'eventual.technology'
        # n.baseURIObject = None
        # n.isConnected = True
        # n.namespaceURI = "http://www.w3.org/1999/xhtml"
        # n.nodePrincipal = None
        # n.outerText = None
        # n.ownerDocument = None
        # n.prefix = None  # 🗑️
        # n.rootNode = None

        b = Node()
        n.appendChild(b)
        # note this was fixed from being a property to a method in 6.6.7
        self.assertEqual(True, n.hasChildNodes())

        c = Node()
        n.appendChild(c)
        self.assertEqual(c, n.lastChild)
        self.assertEqual(b, n.firstChild)
        self.assertEqual(2, n.childElementCount)
        self.assertEqual(True, b in n.childNodes)
        self.assertEqual(True, c in n.childNodes)
        self.assertEqual(None, n.localName)  # obsolete if not a tag or attribute should return none
        self.assertEqual(2, len(n.children))
        self.assertEqual(None, n.nodeValue)

        # test all props on Node
        # self.assertEqual(None, n.baseURI)
        # self.assertEqual(None, n.baseURIObject)
        # self.assertEqual(None, n.childNodes)
        # self.assertEqual(None, n.firstChild)
        # self.assertEqual(None, n.isConnected)
        # self.assertEqual(None, n.isDefaultNamespace)
        # self.assertEqual(None, n.isEqualNode)
        # self.assertEqual(None, n.isSameNode)
        # self.assertEqual(None, n.isSupported)
        # self.assertEqual(None, n.lastChild)
        # self.assertEqual(None, n.localName)
        # self.assertEqual(None, n.namespaceURI)
        # self.assertEqual(None, n.nextSibling)
        # self.assertEqual(None, n.nodeName)
        # self.assertEqual(None, n.nodeType)
        # self.assertEqual(None, n.nodeValue)
        # self.assertEqual(None, n.ownerDocument)
        # self.assertEqual(None, n.parentElement)
        # self.assertEqual(None, n.parentNode)
        # self.assertEqual(None, n.prefix)
        # self.assertEqual(None, n.previousSibling)
        # self.assertEqual(None, n.textContent)

        # print(n.nodeType())
        d = div("test")
        # print(type(d))
        # print(d.nodeName)

        # TODO - i thought had to be uppercase. but this breaks on html5lib treeparser
        # line 1681ish html5parser.py  says... assert node.name == "script"
        # which stops that parser working with domonic
        #
        # self.assertEqual("DIV", d.nodeName)

        self.assertEqual("test", d.nodeValue)
        self.assertEqual(True, n.contains(c))

        n.insertBefore(d, c)
        self.assertEqual(True, n.children[1] == d)

        self.assertEqual(True, n.contains(c))
        n.removeChild(c)
        self.assertEqual(False, n.contains(c))

        # print( n.replaceChild(self, newChild, oldChild) )
        n2 = n.cloneNode()
        # print(len(n2.children))
        self.assertEqual(True, len(n2.children) == 2)
        self.assertEqual(False, n.children == n2.children)
        self.assertEqual(True, n.isSameNode(n))
        self.assertEqual(False, n.isSameNode(n2))
        a1 = div("hi")
        a2 = div("hi")
        self.assertEqual(True, a1.isEqualNode(a2))

        print(a1.nodeValue)
        self.assertEqual(True, a1.nodeValue == "hi")

        a1.nodeValue = "something else"
        self.assertEqual(True, a1.nodeValue == "something else")
        # print(a1.nodeValue)

        a1.textContent = "something new"
        self.assertEqual(True, a1.textContent == "something new")
        # print(a1.textContent)

        myobj = domonic.domonify('div(_class="mytest")')
        # print('---')
        # print(type(myobj))
        myobj.style.float = "left"
        # print('---')
        # print(myobj)
        self.assertEqual(True, str(myobj) == '<div class="mytest" style="float:left;"></div>')

        # print("NOW>>>>")
        mylist = li() / 10
        assert str(mylist) == '<li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>'

        myobj = domonic.load(mylist)
        print(myobj)

        myorderedlist = ol()
        myorderedlist += str(li() / 10)
        assert str(myorderedlist) == '<ol><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li></ol>'

        # TODO - tests
        # compareDocumentPosition()
        # getRootNode()
        # isDefaultNamespace()
        # lookupNamespaceURI()
        # lookupPrefix()
        # normalize()
        # def isSupported(self): return False #  🗑
        # getUserData() 🗑️
        # setUserData() 🗑️

    def test_node(self):
        sometag = div("asdfasdf", div(), div("yo"), _id="test", _thingy="test22")
        somenewdiv = div('im new')
        sometag.appendChild(somenewdiv)

        assert str(somenewdiv.parentNode) == '<div id="test" thingy="test22">asdfasdf<div></div><div>yo</div><div>im new</div></div>'
        assert isinstance(somenewdiv.parentNode, div)
        assert somenewdiv.parentNode.id == "test"
        # print(somenewdiv.parentElement)
        # print(somenewdiv.previousSibling)
        assert str(somenewdiv.previousSibling.nextSibling) == "<div>im new</div>"

        mylist = ul(li(1), li(2), li(3))
        assert str(mylist[1]) == "<li>2</li>"

        mylist = ul(li(), li(), li())
        print(*mylist)

        a1, b1, c1 = ul(li(1), li(2), li(3))
        # print(a1)
        assert str(a1) == '<li>1</li>'

        a1, b1, c1, d1, e1 = button() * 5
        # print(a1, b1, c1, d1, e1)
        assert str(a1) == '<button></button>'
        assert str(b1) == '<button></button>'
        assert str(c1) == '<button></button>'
        assert str(d1) == '<button></button>'
        assert str(e1) == '<button></button>'

        # print(mylist[1] != mylist[1])
        a1 = img()
        a1 >> {'_src': "http://www.someurl.com"}
        # print(a1)
        assert str(a1) == '<img src="http://www.someurl.com" />'

        a1 = button()
        a1 += "hi"
        a1 += "how"
        a1 += "are"
        a1 += "you"
        assert str(a1) == "<button>hihowareyou</button>"
        a1 -= "hi"
        assert str(a1) == "<button>howareyou</button>"

        # print(div(_test="1", **{"_data-test": ""}))

        assert sometag.id == 'test'
        # print(sometag.style.color)  # TODO - get on style
        assert sometag._thingy == 'test22'
        assert sometag.thingy == 'test22'

        # print(10/sometag)
        # print('>>>>', sometag.args[0])
        # print('>>>>',sometag)
        # print('>>>>', sometag.lastChild())
        # print('>>>>', sometag.content)

        # import gc
        # import pprint
        # for r in gc.get_referents(somenewdiv):
        #     pprint.pprint(r)

        # for r in gc.get_referents(sometag):
        #     pprint.pprint(r)

    def test_body(self):
        somebody = body("test", _class="why")  # .html("wn")
        assert str(somebody) == '<body class="why">test</body>'
        # replacing content
        somebody = body("test", _class="why").html("nope")
        assert str(somebody) == '<body class="why">nope</body>'

    def test_dom(self):
        # test div html and innerhtml update content
        sometag = div("asdfasdf", div(), div("yo"), _id="someid")
        self.assertEqual(sometag.tagName, 'div')
        self.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        sometag.html('test')
        self.assertEqual(str(sometag), '<div id="someid">test</div>')
        sometag.innerHTML = 'test2'
        self.assertEqual(str(sometag), '<div id="someid">test2</div>')

        # same test on body tag
        bodytag = body("test", _class="why")
        self.assertEqual(str(bodytag), '<body class="why">test</body>')
        # print(bodytag)

        bodytag.html("bugs bunny")
        self.assertEqual(str(bodytag), '<body class="why">bugs bunny</body>')
        # print('THIS:',bodytag)

        # sometag.innerText()
        # print(sometag.getAttribute('_id'))
        self.assertEqual(sometag.getAttribute('_id'), 'someid')
        # print(sometag.getAttribute('id'))
        # self.assertEqual(sometag.getAttribute('_id'), 'someid')

        mydiv = div("I like cake", div(_class='myclass').html(div("1"), div("2"), div("3")))
        # print(mydiv)
        assert str(mydiv) == '<div>I like cake<div class="myclass"><div>1</div><div>2</div><div>3</div></div></div>'

        print(sometag.innerText())
        # return
        # print(sometag.nodeName)
        # assert(sometag.nodeName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?

        print(sometag.setAttribute('id', 'newid'))
        assert sometag.getAttribute('id') == 'newid'
        assert str(sometag) == '<div id="newid"></div>'

        print(sometag.lastChild)
        print(sometag.hasChildNodes)
        # print('>>',sometag.textContent()) # TODO - will have a think. either strip or render tagless somehow

        sometag.removeAttribute('id')
        assert str(sometag) == '<div></div>'

        sometag.appendChild(footer('test'))
        assert str(sometag) == '<div><footer>test</footer></div>'

        assert sometag.children[0].tagName == 'footer'
        assert str(sometag.children[0]) == '<footer>test</footer>'

        # print(sometag.firstChild)
        assert str(sometag.firstChild) == '<footer>test</footer>'

        htmltag = html()
        assert htmltag.tagName == 'html'
        assert str(htmltag) == '<html></html>'
        htmltag.write('sup!')
        # print("?????", htmltag)
        assert str(htmltag) == '<html>sup!</html>'
        htmltag.className = "my_cool_css"
        # print(htmltag)
        assert str(htmltag) == '<html class="my_cool_css">sup!</html>'
        # print(htmltag)
        # print('-END-')

    def test_create(self):
        print(html().documentElement)
        print(html().URL)
        somebody = document.createElement('sometag')
        print(str(somebody))
        comm = document.createComment('hi there here is a comment')
        print(comm)

        print(html().createElement('sometag'))
        # somebody = document.createElement('sometag')
        # print(str(somebody()))

    def test_events(self):
        print(html().documentElement)
        print(html().URL)
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        print(site)

        def test(evt, *args, **kwargs):
            print('test ran!')
            print(evt)
            print(evt.target)

        site.addEventListener('click', test)
        somebody.addEventListener('anything', test)
        print(site.listeners)
        # site.removeEventListener('click', test)
        # print( site.listeners )

        site.dispatchEvent(Event('click'))
        somebody.dispatchEvent(Event('anything'))

        # document.getElementById("myBtn").addEventListener("click", function(){
        #   document.getElementById("demo").innerHTML = "Hello World";
        # });

    def test_contains(self):
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        print(site)
        another_div = div()
        print(site.contains(somebody))
        another_div = div()
        print(site.contains(another_div))
        another_div = document.createElement('div')
        print(site.contains(another_div))
        third_div = document.createElement('div')
        another_div.appendChild(third_div)
        site.appendChild(another_div)
        print(site.contains(third_div))

    def test_getElementById(self):
        dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById('test')
        print('--')
        print(result)
        print('--')
        pass

    def test_remove(self):
        dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById('test')
        print("owner:", result.ownerDocument)
        result.remove()
        print(result)
        print('--')
        print(dom1)
        print('--')
        pass

    # def test_getElementByClassName(self):
    #     dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))
    #     result = dom1.getElementByClassName('thing')
    #     print('--')
    #     print(result)
    #     print('--')
    #     pass

    def test_dir(self):
        dom1 = div(div(), _dir="rtl")
        print('--')
        print(dom1.dir)
        print('--')
        pass

    def test_normalize(self):
        dom1 = html()
        wrapper = dom1.createElement("div")
        wrapper.appendChild(dom1.createTextNode("Part 1 "))
        wrapper.appendChild(dom1.createTextNode("Part 2 "))
        wrapper.appendChild("Part 3 ")

        print('--')
        print(dom1)
        print('--')
        print(len(wrapper.childNodes))  # 2
        wrapper.normalize()
        print(len(wrapper.childNodes))  # 1
        print(wrapper.childNodes[0].textContent)  # "Part 1 Part 2 "
        pass

    # def test_Node():
        # TODO - tests all below
        # contains - probably need more recursive testing
        # replaceChild
        # anchors

    def test_querySelector(self):
        dom1 = html(div(div(div(div(div(div(div(div(_id="thing"), span(_id="fun"), div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))

        result = dom1.querySelector('#thing')
        # print('--')
        # print("RESULT>>>>>", result)
        # print('--')
        assert result.id == 'thing'

        result = dom1.querySelector('span')
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == 'fun'

        result = dom1.querySelector('.test')
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.className == 'test this thing'

        result = dom1.getElementsByClassName('this')
        # print('--')
        # print("RESULT>>>>>", result)
        assert len(result) == 1
        assert result[0].className == 'test this thing'

        links = self.page.querySelectorAll("a[rel=nofollow]")
        for linky in links:
            print(linky.getAttribute("href"))
        print('GO! >>>>>>>>>')  # works
        # return

        result = self.page.querySelectorAll("li[class='nav-item']")
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("h4[class='font-weight-bold text-uppercase']")
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # fails

        result = self.page.querySelectorAll("li.nav-item")
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href='#services']")
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("p.text-gray")
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href$='technology']")
        print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href*='twitter']")
        print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = dom1.querySelectorAll('.fa-twitter')
        print('--')
        print("z RESULT>>>>>", result)
        # TODO - failing. however this is now running through qselectorall
        # return
        # assert result.className == 'test this thing'



    def test_getElementsBySelector(self):

        dom1 = html(div(div(div(div(div(div(div(div(_id="thing"), span(_id="fun"), div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))

        result = dom1.getElementsBySelector('#thing', dom1)[0]
        # print("RESULT>>>>>", result)
        # print('--')
        assert result.id == 'thing'

        result = dom1.getElementsBySelector('span', dom1)[0]
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == 'fun'

        # result = dom1.getElementsBySelector('.test', dom1)#[0]  # [0] #?? no class called test?
        # print('--')
        # print("RESULT>>>>>", result)
        # TODO - failing. however this is now running through qselectorall
        # return
        # assert result.className == 'test this thing'

        # result = dom1.getElementsBySelector('.this', dom1)[0]
        # print('--')
        # print("RESULT>>>>>", result)
        # assert len(result) == 1
        # assert result[0].className == 'test this thing'

        from domonic.dQuery import º
        º(self.page)

        # print(º('a'))
        # print(str(page.getElementsBySelector("a[rel=nofollow]", page)[0]))
        # print(str(page.getElementsBySelector("a", page)))

        # print(º('#team'))
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        node = str(self.page.getElementsBySelector("#team", self.page)[0])
        assert node.startswith('<section id="team"')

        # print(º('a[rel=nofollow]'))
        # print(str(page.getElementsBySelector("a[rel=nofollow]", page)[0]))

        # print(º('.fab'))
        # print(str(page.getElementsBySelector(".fab", page)))

        # print(º('.far'))
        # print(º('a'))
        # print(str(page.getElementsBySelector(".fab", page)))

        # if there's a rule.
        # if its a tag

        # if just class regular seems better
        #  circular reerence if i use it in query selector for tags.

        # if True:
        # return

        # render( page, 'index.html' )

        links = self.page.getElementsBySelector("a[rel=nofollow]", self.page)
        for linky in links:
            print(linky.getAttribute("href"))
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("li[class='nav-item']", self.page)
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("h4[class='font-weight-bold text-uppercase']", self.page)
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # fails

        result = self.page.getElementsBySelector("li.nav-item", self.page)
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href='#services']", self.page)
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("p.text-gray", self.page)
        print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href$='technology']", self.page)
        print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href*='twitter']", self.page)
        print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

    def test_decorators(self):
        from domonic.decorators import el

        @el(html)
        @el(body)
        @el(div)
        def test():
            return 'hi!'
        print(test())
        assert str(test()) == '<html><body><div>hi!</div></body></html>'
        print('decorators work!')

        @el(html, True)
        @el(body, True)
        @el(div, True)
        def test():
            return 'hi!'
        assert test() == '<html><body><div>hi!</div></body></html>'
        print('decorators work2!')

        @el('html')
        @el('body')
        @el('div')
        def test():
            return 'hi!'
        print(test())
        assert str(test()) == '<html><body><div>hi!</div></body></html>'
        print('decorators work3!')

        @el(html, True)
        @el(body)
        @el('div')
        def test():
            return 'hi!'
        print(test())
        print('decorators work4!')

    def test_domonic_window_console_log(self):
        # note originally dom had everything from document
        # this will likely move later versions

        # window = Window()
        # Window().console.log("test this")
        # window.console.log("test this")

        # c = Console()
        # c.log()
        # Console.log('test')
        # someObject = { 'str': "Some text", 'id': 5 }
        # Console.log(someObject)

        # [09:27:13.475] ({str:"Some text", id:5})

        count = 5
        Console.log('--count: %d', count)
        assert Console.log('count: %d', count) == "count: 5"
        Console.log('--count:', count)
        assert Console.log('count:', count) == "count: 5"

        console.time("answer time")
        console.timeLog("answer time")
        console.timeEnd("answer time")

        errorMsg = 'the # is not even'
        for number in range(2, 5):
            console.log('the # is ' + str(number))
            console.assert_(number % 2 == 0, {'number': number, 'errorMsg': errorMsg})

        console.info('test2')
        console.warn('test3')

        pass

    def test_domonic_matches(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"),
            li("Philippine eagle", _class="endangered"),
            li("Great white pelican")
        )
        birds = content.getElementsByTagName('li')
        # print(birds)
        for bird in birds:
            # print(bird)
            if bird.matches('.endangered'):
                print('The ' + bird.textContent + ' is endangered!')

    # def test_domonic_closest(self):

    def test_sanitize(self):

        # our input string to clean
        # stringToClean = 'Some text <b><i>with</i></b> <blink>tags</blink>, including a rogue script <script>alert(1)</script> def. # TODO - failing due to blink tag

        # TODO - parser is stripping last space off the string
        # stringToClean = 'Some text <b><i>with</i></b> <p>tags</p>, including a rogue script <script>alert(1)</script> def.'
        # result = Sanitizer().sanitizeToString(stringToClean)
        # console.log("result::", result)
        # assert result == "Some text <b><i>with</i></b> <blink>tags</blink>, including a rogue script def."
        # return

        sample = "<div style='cool'><span id='span1' class='theclass' style='font-weight: bold'>hello</span></div>"
        # sample = '<div style="cool"><span id="span1" class="theclass" style="font-weight: bold">hello</span></div>'

        # Allow only <span style>: <span style='font-weight: bold'>...</span>
        s1 = Sanitizer({'allowAttributes': {"style": ["span"]}}).sanitize(sample)
        # print(type(s1))
        # print(s1)
        assert str(s1) == '<div><span style="font-weight: bold">hello</span></div>'

        # Allow style, but not on span: <span>...</span>
        s2 = Sanitizer({'allowAttributes': {"style": ["div"]}}).sanitize(sample)
        # print(s2)
        assert str(s2) == '<div style="cool"><span>hello</span></div>'

        # Allow style on any elements: <span style='font-weight: bold'>...</span>
        s3 = Sanitizer({'allowAttributes': {"style": ["*"]}}).sanitize(sample)
        # print("3::::", s3)
        # print(str(s3))
        # Note - check why is id/class not a default config?
        assert str(s3) == '<div style="cool"><span style="font-weight: bold">hello</span></div>'

        # Drop <span id>: <span class='theclass' style='font-weight: bold'>...</span>
        s4 = Sanitizer({'dropAttributes': {"id": ["span"]}}).sanitize(sample)
        # print("4::::", s4)
        assert str(s4) == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'

        # Drop id, everywhere: <span class='theclass' style='font-weight: bold'>...</span>
        s5 = Sanitizer({'dropAttributes': {"id": ["*"]}}).sanitize(sample)
        print("5::::", s5)
        print(s5)
        assert str(s5) == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'

        # Comments will be dropped by default.
        # comment = to_node("Hello  World!")
        # Sanitizer().sanitize(comment)  # "Hello  World!"
        # Sanitizer({'allowComments': True}).sanitize(comment)  # Same as comment.

        # Does the default config allow script elements?
        # Sanitizer.getDefaultConfiguration().allowElements.includes("script")  # false

        # We found a Sanitizer instance. Does it have an allow-list configured?
        # a_sanitizer = ...;
        # !!a_sanitizer.getConfiguration().allowElements # true, if an allowElements list is configured

        # If it does have an allow elements list, does it include the <div> element?
        # a_sanitizer.getConfiguration().allowElements.includes("div")  # true, if "div" is in allowElements.

        # Note that the getConfiguration method might do some normalization. E.g., it won’t
        # contain key/value pairs that are not declare in the IDL.
        # Object.keys(new Sanitizer({madeUpDictionaryKey: "Hello"}).getConfiguration())  # []

        # As a Sanitizer’s config describes its operation, a new sanitizer with
        # another instance’s configuration should behave identically.
        # (For illustration purposes only. It would make more sense to just use a directly.)
        # a = /* ... a Sanitizer we found somewhere ... */;
        # b = Sanitizer(a.getConfiguration());  // b should behave the same as a.

        # getDefaultConfiguration() and new Sanitizer().getConfiguration should be the same.
        # (For illustration purposes only. There are better ways of implementing
        # object equality in JavaScript.)
        # JSON.stringify(Sanitizer.getDefaultConfiguration()) == JSON.stringify(new Sanitizer().getConfiguration());  // true

    def test_comment(self):
        from domonic.html import comment
        # https://github.com/byteface/domonic/issues/38
        com = f"{html(head(),body(comment('foo')))}"
        # print(com)
        com = comment('foo')
        # print(f'{com}')
        assert str(com) == '<!--foo-->'
        from domonic.dom import Comment
        # https://github.com/byteface/domonic/issues/38
        com = f"{html(head(),body(Comment('foo')))}"
        print(com)
        # not able to recreate. Comment was updated to a Node in 6.1
        # this may have been due to that
        # TODO - mulitple arguments to comment

    def test_treewalker(self):

        from domonic.dom import Comment
        from domonic.dom import TreeWalker

        doc = html(
            div(_id="contentarea").html(
            p("Some ", span("text")),
            b("Bold text")
        )
        )

        rootnode = doc.getElementById("contentarea")
        # print(rootnode)
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        print(walker.currentNode)
        print(walker.firstChild())

        # //Alert the starting node Tree Walker currently points to (root node)
        window.alert(walker.currentNode.tagName)  # alerts DIV (with id=contentarea)
        # assert walker.currentNode.tagName == 'DIV'

        # Step through and alert all child nodes
        # for n in walker.nextNode():
        while walker.nextNode():
            print('+++', walker.nextNode())
            window.alert(walker.currentNode)  # //alerts P, SPAN, and B.

        return

        # //Go back to the first child node of the collection and alert it
        walker.currentNode = rootnode  # //reset TreeWalker pointer to point to root node
        print(walker.currentNode)
        print(walker.firstChild())
        window.alert(walker.firstChild().tagName)  # //alerts P

        # test 2
        doc = html(
            ul(_id="mylist").html(
                    li("List 1"),
                    li("List 2"),
                    li("List 3")
                )
            )

        rootnode = doc.getElementById("mylist")
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        window.alert(len(walker.currentNode.childNodes))  # //alerts 7 (includes text nodes)
        window.alert(len(walker.currentNode.getElementsByTagName("*")))  # //alerts 3

        # test 3
        doc = html(
            div(_id="main").html(
            p("This is a ", span("paragraph")),
            b("Bold text")
        )
        )
        mainDiv = doc.getElementById("main")
        walker = doc.createTreeWalker(mainDiv, NodeFilter.SHOW_ELEMENT, None, False)
        console.log(walker)

        treeWalker = document.createTreeWalker(
            mainDiv,
            NodeFilter.SHOW_TEXT,
            lambda node: NodeFilter.FILTER_ACCEPT if (String(node.nodeValue).trim() != "") else NodeFilter.FILTER_REJECT,
            False
            )

        # //Alert the starting node Tree Walker currently points to (root node)
        # //displays DIV (with id=main)
        console.log(walker.currentNode.tagName)

        # //Step through and alert all child nodes
        while (walker.nextNode()):
            # //displays P, SPAN, and B.
            console.log(walker.currentNode.tagName)

        # //Go back to the first child node of the collection and display it
        # //to do that, we must reset TreeWalker pointer to point to main DIV
        walker.currentNode = mainDiv
        # //displays P
        console.log(walker.firstChild().tagName)

        # //reset TreeWalker pointer to point to main DIV
        walker.currentNode = mainDiv

        # test 4
        # https://gist.github.com/bennadel/10545473

        # test 5
        # https://paul.kinlan.me/dom-treewalker/


if __name__ == '__main__':
    unittest.main()
