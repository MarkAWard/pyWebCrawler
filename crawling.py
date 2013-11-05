import urllib2

# list_a = list_a U list_b
def union(list_a, list_b):
    for item in list_b:
        if item not in list_a:
            list_a.append(item)

# return the next found url and end postion of the url
# to then be able to continue searching
def find_next_link(page_source):
    # could be improved... reg exp?
    link_tag = page_source.find('<a href=')
    if link_tag < 0:
        return None, 0

    # add 1 to start at the first char after "    
    beg_url = page_source.find('"', link_tag) + 1
    end_url = page_source.find('"', beg_url)
    url = page_source[beg_url:end_url]

    return url, end_url

# continuously call find_next_link till it returns
# none. At each step add the found link to the list
def get_all_links(page_source):
    links = []
    while True:
        url, next_index = find_next_link(page_source)
        if not url:
            break
        links.append(url)
        page_source = page_source[next_index:]
    return links

# Crawl a webpage passed in as seed. Every link found in the seed's
# html source code is added to the list tocrawl. Depth first search.
# Each page that is crawled is added to the index dictionary. When 
# there are no more pages to be crawled, return the index
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    while tocrawl:
        # next page to crawl
        page = tocrawl.pop()
        if page not in crawled:
            page_source_code = get_page(page)
            add_page_to_index(index, page, page_source_code)
            # add newly found links to the tocrawl list
            union(tocrawl, get_all_links(page_source))
            crawled.append(page)
    return index


def fetch(url):
    try:
        request = urllib2.urlopen(url)
        return request.read(100)
    except:
        return ""


def get_source(page):

    source = """<a href= "http://StopEmailingMeETS!!!!" > link this </a><a href= "http://StopEmailingEveryoneETS!!!!" > link this </a><a href= "http://StopEmailingMeETS!!!!" > link this </a><a href= "http://StopEmailingMe!!!!" > link this </a>
"""
    return source


def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return '''<html> <body> This is a test page for learning to crawl!
<p> It is a good idea to
<a href="http://www.udacity.com/cs101x/crawling.html">
learn to crawl</a> before you try to
<a href="http://www.udacity.com/cs101x/walking.html">walk</a> or
<a href="http://www.udacity.com/cs101x/flying.html">fly</a>.</p></body>
</html>'''

        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return '''<html> <body> I have not learned to crawl yet, but I am
quite good at  <a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.
</body> </html>'''

        elif url == "http://www.udacity.com/cs101x/walking.html":
            return '''<html> <body> I cant get enough
<a href="http://www.udacity.com/cs101x/index.html">crawling</a></body></html>'''

        elif url == "http://www.udacity.com/cs101x/flying.html":
            return '''<html>
<body>The magic words are Squeamish Ossifrage!</body></html>'''
    except:
        return ""
    return ""

# check for the keyword in the index and return all urls
# that are paired with that keyword
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

# add keyword url pair to the index dictionary
def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]



#######################################################
# TODO: Improve the split_string func and split list  #
#     maybe only get stuff in the body. Check out     #
#     possible py libraries for parsing               #
#######################################################

# content is url's source code, split it into words and
# add each word to the index with the url.
# Dont like it right now....
def add_page_to_index(index,url,content):
    # define characters to split at and strip
    splitlist = ' ,.-<>!#/\\'
    for word in split_string(content,splitlist):
        if not lookup(index,word):
            add_to_index(index,word,url)
            
################# FIX ME #################################
def split_string(source,splitlist):
    words = []
    atSplit = True
    for char in source:
        if char in splitlist:
            atSplit = True
        else:
            if atSplit:
                words.append(char)
                atSplit = False
            else:
                words[-1] = words[-1] + char
    return words



index = crawl("http://www.udacity.com/cs101x/index.html")
print index
print lookup(index,"test")
print lookup(index,"or")
print lookup(index,"crawling")

#print crawled
#for entry in index:
#    print entry
