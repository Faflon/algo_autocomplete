import heapq


def dfs_collect_words(node):
    """
    Depth-first search to collect words from the trie.
    Time complexity: O(N) where N is the number of nodes in the trie.
    """
    results = []

    if not node:
        return results

    if node.is_end:
        results.append((node.word, node.score))

    for child_node in node.children.values():
        results.extend(dfs_collect_words(child_node))

    return results


def get_top_5_completions(prefix_node):
    """
    Get the top 5 completions for a given prefix node with best scores.
    """
    if not prefix_node:
        return []

    all_possible_words = dfs_collect_words(prefix_node)
    top_5_words = heapq.nlargest(5, all_possible_words, key=lambda x: x[1])

    return top_5_words
