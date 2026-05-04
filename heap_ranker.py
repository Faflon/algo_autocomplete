import heapq


def dfs_with_heap(node, top_5_heap):
    """
    Depth-first search to collect words from the trie.
    Time complexity: O(N) where N is the number of nodes in the trie.
    """
    results = []

    if not node:
        return results

    if len(top_5_heap) == 5 and node.max_score <= top_5_heap[0][0]:
        return

    if node.is_end:
        if len(top_5_heap) < 5:
            heapq.heappush(top_5_heap, (node.score, node.word))
        else:
            if node.score > top_5_heap[0][0]:
                heapq.heappushpop(top_5_heap, (node.score, node.word))
    sorted_children = sorted(
        node.children.values(), key=lambda child: child.max_score, reverse=True
    )

    for child_node in sorted_children:
        dfs_with_heap(child_node, top_5_heap)


def get_top_5_completions(prefix_node):
    """
    Gets the top 5 completions for a given prefix node using a heap to maintain the top scores.
    """
    if not prefix_node:
        return []

    top_5_heap = []
    dfs_with_heap(prefix_node, top_5_heap)

    top_5_heap.sort(key=lambda x: x[0], reverse=True)
    return [(query, score) for score, query in top_5_heap]
