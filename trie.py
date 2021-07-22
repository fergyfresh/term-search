from collections import namedtuple


TERM_TERMINATOR = True
Match = namedtuple("Matches", "start end word")


def build_trie(terms, term_terminator=TERM_TERMINATOR):
    trie = {}
    for term in terms:
        current = trie
        for char in term:
            if char not in current:
                current[char] = {}
            current = current[char]
        current[term_terminator] = term

    return trie


def search_for_terms(terms, doc, term_terminator=TERM_TERMINATOR):
    trie = build_trie(terms)
    n = len(doc)
    matches = []

    def backtracking(i, parent):
        letter = doc[i]
        current_node = parent[letter]
        word_match = current_node.get(TERM_TERMINATOR, False)

        if word_match:
            start, end = i - len(word_match) + 1, i
            is_partial = False
            if matches:
                last_match = matches[-1]
                is_partial = start > last_match.start and start < last_match.end

            if not is_partial:
                m = Match(start, end, word_match)
                matches.append(m)

        if i + 1 < n - 1 and doc[i + 1] in current_node:
            backtracking(i + 1, current_node)

    current = trie
    for i in range(n):
        if doc[i] in trie:
            backtracking(i, trie)
    return matches


if __name__ == "__main__":

    terms = [
        "Borrower",
        "Subsidiaries",
        "Material Project Party",
        "Project",
        "Project Manager",
        "Anti-Money Laundering Laws",
        "Sanctions",
        "Anti-Corruption Laws",
        "Affiliates",
        "Sanctioned Person",
        "Sanctioned Country",
        "Person",
        "Officer",
        "Director",
        "Agents",
    ]

    doc = """
        The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, 
        any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such 
        Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project, 
        have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption 
        Laws. Neither Borrower, nor any Subsidiaries of the Borrowers, nor any officer or director or, to the knowledge of any Borrower, 
        Affiliates, employee, agent or representative of either Borrower has engaged, directly or indirectly, in any activity or conduct 
        which would violate any Anti-Corruption Laws or Anti-Money Laundering Laws. Neither Borrower nor any Subsidiaries of the Borrowers, 
        nor any officer or director or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower 
        has engaged, directly or indirectly, in any dealings or transactions with, involving or for the benefit of a Sanctioned Person,
        or in or involving a Sanctioned Country, where such dealings or transactions would violate Sanctions, in the five (5) year period
        immediately preceding the date hereof.
    """

    matches = search_for_terms(terms, doc)

    # Simple test to ensure bounds of words are calculated properly.
    for match in matches:
        start, end, word = match
        assert doc[start : end + 1] == word

    from pprint import PrettyPrinter

    pp = PrettyPrinter()
    pp.pprint(matches)
