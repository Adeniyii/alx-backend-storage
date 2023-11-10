#!/usr/bin/env python3
""""""

get_page = __import__("web").get_page

for i in range(5):
    print("{}: \n ==============================".format(i))
    print(get_page("http://slowwly.robertomurray.co.uk"))
