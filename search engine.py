import urllib

url = input('enter url : ')

def get_page(url):
    if url:
        file = urllib.urlopen(url)
        a = file.read()
        return a
    return None

def get_all_links(page): # gets all links contained in the page
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_next_target(page): # gets the link in the page
    start_link = page.find('href="htt')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(a, b): # union of a and b
    for e in b: 
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content): # stores all the keywords and url in index
    try:
        while '="' in content:
            pos1=content.index('="')
            pos2=content.index('"',pos1+2)
            if content[pos1+2:pos1+6]!='http':
                words = content[pos1+2:pos2].split()
                for word in words:
                    add_to_index(index, word, url)
            content=content[pos2+1:]
    except:
        a=1

def add_to_index(index, keyword, url): # add keyword and urls in the index
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    i=0
    try:
        while tocrawl and i<20: 
            page = tocrawl.pop()
            if page not in crawled:
                content = get_page(page)
                add_page_to_index(index, page, content)
                outlinks = get_all_links(content)
                graph[page] = outlinks
                union(tocrawl, outlinks)
                crawled.append(page)
                i=i+1
    except:
        return index, graph
    return index, graph

def compute_ranks(graph): # calculate the ranks of urls 
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

def lookup(index, keyword): # look for keyword in the index
    if keyword in index:
        return index[keyword]
    else:
        return None

def lucky_search(index, ranks, keyword): # returns url with highest rank
    if keyword not in index:
        return None
    else:
        a=index[keyword]
        c=a[0]
        rank=0
        for i in a:
            if rank<ranks[i]:
                c=i
                rank = ranks[i]
    return c

def ordered_search(index, ranks, keyword): # returns list of url sorted according to their ranks
    if keyword not in index:
        return []
    else:
        a=index[keyword]
        c=[]
        sorted=[]
        for i in a:
            c.append(ranks[i])
        c.sort(reverse=True)
        for j in c:
            for k in a:
                if ranks[k]==j:
                    sorted.append(k)
                    break
    return sorted

page = get_page(url)
link = get_all_links(page)
index, graph = crawl_web(url)
rank = compute_ranks(graph)

print link

