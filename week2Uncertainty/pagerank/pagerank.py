import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main() -> None:
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


def crawl(directory) -> dict:
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


def transition_model(corpus, page, damping_factor) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # raise NotImplementedError

    probs = {}
    total_pages = len(corpus)
    links = corpus[page]

    # If page has no outgoing links, treat it as linking to all pages
    if not links:
        prob = 1 / total_pages
        for p in corpus:
            probs[p] = prob
        return probs

    # Baseline probability for all pages (the "random jump" part)
    # Each page in the corpus has an equal (1 - d) / N chance of being chosen
    random_jump_prob = (1 - damping_factor) / total_pages

    # Probability from following links (the "damping factor" part)
    # Each linked page gets an additional d / NumLinks(page) chance
    link_prob = damping_factor / len(links)

    for p in corpus:
        probs[p] = random_jump_prob
        if p in links:
            probs[p] += link_prob

    return probs


def sample_pagerank(corpus, damping_factor, n) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError

    # Initialize counts for each page to 0
    counts = {page: 0 for page in corpus}

    # Generate the first sample by picking a page at random
    current_page = random.choice(list(corpus.keys()))
    counts[current_page] += 1

    # Generate the remaining n-1 samples
    for _ in range(n - 1):
        # Get the probability distribution for the next step
        probabilities = transition_model(corpus, current_page, damping_factor)

        # Extract pages and their corresponding weights
        pages = list(probabilities.keys())
        weights = list(probabilities.values())

        # Choose the next page based on the distribution
        # random.choices returns a list, so we take the first element [0]
        current_page = random.choices(pages, weights=weights, k=1)[0]

        # Update the visit count for the chosen page
        counts[current_page] += 1

    # Convert counts to proportions (estimated PageRank)
    pagerank = {page: count / n for page, count in counts.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor) -> dict:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError

    N = len(corpus)
    # Initialize each page's rank to 1 / N
    pageranks = {page: 1 / N for page in corpus}

    # Pre-calculate the constant "random jump" part of the formula
    random_jump = (1 - damping_factor) / N

    while True:
        new_pageranks = {}

        for p in corpus:
            # Calculate the summation of contributions from all pages i that link to p
            total_link_contribution = 0

            for i in corpus:
                # Case A: Page i links to p
                if p in corpus[i]:
                    total_link_contribution += pageranks[i] / len(corpus[i])

                # Case B: Page i has no links (interpret as linking to all pages)
                elif len(corpus[i]) == 0:
                    total_link_contribution += pageranks[i] / N

            # Apply the PageRank formula: (1-d)/N + d * sum(PR(i)/NumLinks(i))
            new_pageranks[p] = random_jump + (damping_factor * total_link_contribution)

        # Check for convergence (no value changes by more than 0.001)
        # We check the absolute difference for every page
        is_converged = True
        for page in pageranks:
            if abs(new_pageranks[page] - pageranks[page]) > 0.001:
                is_converged = False
                break

        # Update the ranks for the next iteration
        pageranks = new_pageranks

        if is_converged:
            break

    # Ensure the sum is exactly 1 (handling floating point rounding)
    total_sum = sum(pageranks.values())
    return {p: r / total_sum for p, r in pageranks.items()}


if __name__ == "__main__":
    main()
