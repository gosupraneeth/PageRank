import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #raise NotImplementedError
    probability_dict=dict()

    # adding probability of random pages
    for key in corpus:
        prob=(1-damping_factor)*(1/len(corpus))
        probability_dict[key]=prob

    # adding probability for the linked pages
    for value in corpus[page]:
        probability_dict[value]+=damping_factor*(1/len(corpus[page]))

    return probability_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError

    page_rank=dict()
    # initialising the count with 0
    for page in corpus:
        page_rank[page]=0

    # taking the first random sample
    sample=random.choice(list(page_rank.keys()))

    # itering over n times and calculating the count
    for iter in range(n):

        page_rank[sample]+=1
        probability_dict=transition_model(corpus,sample,damping_factor)
        probability_dict=dict(sorted(probability_dict.items(), key=lambda item: item[1],reverse=True))
        maxi=max(probability_dict.values())
        max_list=[]
        for key,value in probability_dict.items():
            if maxi==value:
                max_list.append(key)

        sample=random.choice(max_list)


    # dividing with n to get the probability
    for page in page_rank:
        page_rank[page]=page_rank[page]/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError

    page_rank=dict()

    # initialising with the 1/N values
    for page in corpus:
        page_rank[page]=1/len(corpus)

    # running through the while loop and claculating the page ranks untill the change is less than 0.001
    while True:

        flag=0
        for page in corpus:
            current_value=page_rank[page]
            page_rank[page]=(1-damping_factor)/len(corpus)
            for link in corpus:
                if page in corpus[link]:
                    try:
                        page_rank[page]+=damping_factor*(page_rank[link]/len(corpus[link]))
                    except ZeroDivisionError:
                        page_rank[page]+=damping_factor*(page_rank[link]/len(corpus))
            new_value=page_rank[page]
            if abs(new_value-current_value) >=0.001:
                flag=1

        if flag is 0:
            break

    return page_rank


if __name__ == "__main__":
    main()
