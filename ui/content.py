"""Text shown on the Analysis and Explanation tabs of every page."""

INFO = {
    "Stack": {
        "subtitle": "A last-in, first-out (LIFO) collection: items are added to and removed from the top.",
        "complexity": [
            ("Push", "O(1)"), ("Pop", "O(1)"), ("Peek", "O(1)"),
            ("Search", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "A stack only lets you touch one end, called the top. Push places a new item on top; pop removes the item that was added most recently.",
            "Stacks power undo history, function call stacks, expression evaluation and depth-first traversal."
        ],
        "properties": [
            "Last in, first out (LIFO)",
            "Push and pop never shift other elements",
            "Popping an empty stack is an error (underflow)"
        ],
    },
    "Queue": {
        "subtitle": "A first-in, first-out (FIFO) collection: items join at the rear and leave from the front.",
        "complexity": [
            ("Enqueue", "O(1)"), ("Dequeue", "O(1)"), ("Peek", "O(1)"),
            ("Search", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "A queue serves items in the order they arrived. Enqueue adds to the rear and dequeue removes from the front, like people waiting in line.",
            "Queues are used for task scheduling, buffering, message passing and breadth-first search."
        ],
        "properties": [
            "First in, first out (FIFO)",
            "Operations happen at opposite ends",
            "Dequeueing from an empty queue is an error (underflow)"
        ],
    },
    "Linked List": {
        "subtitle": "A chain of nodes where each node stores a value and a pointer to the next node.",
        "complexity": [
            ("Insert at head", "O(1)"), ("Insert at tail", "O(n) without a tail pointer"),
            ("Delete", "O(n)"), ("Search", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "Unlike an array, the nodes of a linked list are not stored side by side. Each node points to the next one, so reaching the k-th node means following k pointers from the head.",
            "That makes insertion and deletion cheap once you are at the right spot (only pointers change), but random access is slow."
        ],
        "properties": [
            "Dynamic size, no shifting on insert or delete",
            "No random access by index",
            "Extra memory for one pointer per node"
        ],
    },
    "Binary Search Tree": {
        "subtitle": "A binary tree where every left descendant is smaller and every right descendant is larger than its parent.",
        "complexity": [
            ("Search", "O(log n) average, O(n) worst"),
            ("Insert", "O(log n) average, O(n) worst"),
            ("Delete", "O(log n) average, O(n) worst"),
            ("Traversal", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "Each comparison discards one whole subtree, so lookups follow a single path from the root. In-order traversal visits the values in sorted order.",
            "A BST does not rebalance itself. Inserting sorted values produces a long chain and degrades every operation to O(n), which is the problem AVL trees solve."
        ],
        "properties": [
            "Left subtree < node < right subtree",
            "In-order traversal is sorted",
            "Shape depends on insertion order"
        ],
    },
    "AVL Tree": {
        "subtitle": "A self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one.",
        "complexity": [
            ("Search", "O(log n)"), ("Insert", "O(log n)"),
            ("Delete", "O(log n)"), ("Rotation", "O(1)"), ("Space", "O(n)")
        ],
        "explanation": [
            "After every insertion the tree recomputes each node's balance factor (left height minus right height). If a factor leaves the range -1 to 1, rotations restore balance.",
            "Four cases exist: left-left and right-right need a single rotation; left-right and right-left need a double rotation. Rotations only rearrange a few pointers, so the cost stays constant."
        ],
        "properties": [
            "Balance factor of every node is -1, 0 or 1",
            "Height is always O(log n)",
            "Stricter balance than red-black trees, so faster lookups"
        ],
    },
    "B-Tree": {
        "subtitle": "A balanced multiway search tree whose nodes hold several keys, designed to minimise slow disk or page reads.",
        "complexity": [
            ("Search", "O(log n)"), ("Insert", "O(log n)"),
            ("Delete", "O(log n)"), ("Traversal", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "Each node stores many sorted keys and has one more child than keys. Because nodes are wide, the tree stays very shallow and a lookup touches few nodes.",
            "When a node overflows it splits and pushes its median key up, so all leaves always stay at the same depth."
        ],
        "properties": [
            "All leaves are at the same depth",
            "Nodes are kept at least half full (except the root)",
            "Used by databases and file systems"
        ],
    },
    "Heap": {
        "subtitle": "A complete binary tree stored in an array where every parent is smaller than its children (min-heap).",
        "complexity": [
            ("Insert (push)", "O(log n)"), ("Extract min", "O(log n)"),
            ("Peek min", "O(1)"), ("Search", "O(n)"), ("Space", "O(n)")
        ],
        "explanation": [
            "New values are added at the end and bubbled up while they are smaller than their parent. Extracting the minimum swaps the root with the last item and sinks it back down.",
            "Heaps back priority queues and heap sort, and are used inside Dijkstra's algorithm."
        ],
        "properties": [
            "Smallest value is always at the root",
            "Stored compactly in an array",
            "Only the minimum is quickly accessible"
        ],
    },
    "Sorting": {
        "subtitle": "Generate the steps of a sorting algorithm and walk through every comparison and swap.",
        "complexity": [
            ("Bubble sort", "O(n²), best O(n)"),
            ("Selection sort", "O(n²)"),
            ("Insertion sort", "O(n²), best O(n)"),
            ("Merge sort", "O(n log n)"),
            ("Quick sort", "O(n log n) average, O(n²) worst")
        ],
        "explanation": [
            "Bubble, selection and insertion sort compare elements pair by pair and are simple but quadratic. Merge sort and quick sort use divide and conquer to reach O(n log n).",
            "Use Previous and Next to step through the algorithm; highlighted bars are the elements being compared or swapped."
        ],
        "properties": [
            "Merge sort is stable and always O(n log n)",
            "Quick sort is usually fastest in practice",
            "Insertion sort is excellent on nearly sorted data"
        ],
    },
    "Searching": {
        "subtitle": "Run linear or binary search on a list of integers and compare how many comparisons each needs.",
        "complexity": [
            ("Linear search", "O(n)"), ("Binary search", "O(log n)"),
            ("Binary search requirement", "Sorted input")
        ],
        "explanation": [
            "Linear search checks every element until it finds the target. Binary search compares with the middle element and discards half of the remaining range each time.",
            "Binary search is dramatically faster on large lists but only works when the data is already sorted."
        ],
        "properties": [
            "Linear search works on any list",
            "Binary search halves the search range every step",
            "1,000,000 items need at most about 20 binary comparisons"
        ],
    },
    "Graph Lab": {
        "subtitle": "Create a weighted graph and run BFS, DFS, or Dijkstra's algorithm from a start vertex.",
        "complexity": [
            ("BFS", "O(V + E)"), ("DFS", "O(V + E)"),
            ("Dijkstra (binary heap)", "O((V + E) log V)"),
            ("Adjacency list space", "O(V + E)")
        ],
        "explanation": [
            "BFS explores the graph level by level using a queue, DFS dives as deep as possible using a stack or recursion, and Dijkstra repeatedly settles the closest unvisited vertex to find shortest paths.",
            "The start vertex is the value in the From vertex field. Visited vertices are highlighted after a run."
        ],
        "properties": [
            "BFS finds shortest paths in unweighted graphs",
            "Dijkstra requires non-negative weights",
            "Edges here are undirected"
        ],
    },
}

TABS = ["Visualization", "Analysis", "Explanation"]
