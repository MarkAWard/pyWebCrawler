import urllib2


class Crawler(object):

    index = {}
    graph = {}
    seed = ""

    def __init__(self):
        self.index = {}
        self.graph = {}

    # Crawl a webpage passed in as seed. Every link found in the seed's
    # html source code is added to the list tocrawl. Depth first search.
    # Each page that is crawled is added to the index dictionary. When 
    # there are no more pages to be crawled, return the index
    def crawl(self, web_seed):
        self.seed = web_seed
        tocrawl = [web_seed]
        crawled = []
        while tocrawl:
            # next page to crawl
            page = tocrawl.pop()
            if page not in crawled:
                page_source_code = self.fetch(page)
                self.add_page_to_index(self.index, page, page_source_code)
                outlinks = self.get_all_links(page_source_code)
                self.graph[page] = outlinks
                # add newly found links to the tocrawl list
                self.union(tocrawl, outlinks)
                crawled.append(page)
            print tocrawl
        return self.index, self.graph


    def fetch(self, url):
        try:
            request = urllib2.urlopen(url)
            return request.read()
        except:
            return ""



    # return the next found url and end postion of the url
    # to then be able to continue searching
    def find_next_link(self, page_source):
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
    def get_all_links(self, page_source):
        links = []
        while True:
            url, next_index = self.find_next_link(page_source)
            if not url:
                break
            links.append(url)
            page_source = page_source[next_index:]
            return links

    # add keyword url pair to the index dictionary
    def add_to_index(self, index, keyword, url):
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
    def add_page_to_index(self, index, url, content):
        # define characters to split at and strip
        splitlist = ' ,.-<>!#/\\'
        for word in self.split_string(content,splitlist):
            if not lookup(index,word):
                self.add_to_index(index,word,url)
            
################# FIX ME #################################
    def split_string(self, source, splitlist):
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

# list_a = list_a U list_b
    def union(self, list_a, list_b):
        try:
            for item in list_b:
                if item not in list_a:
                    list_a.append(item)
        except:
            return


# version of pagerank algorithm
# determine the 'rank' of the page by the incoming links
# improve for loops
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

if __name__ == "__main__":
    C = Crawler()
    C.crawl("") # enter seed

    print C.index
    print "\n\n", C.graph
    print "\n\n", C.seed
   
