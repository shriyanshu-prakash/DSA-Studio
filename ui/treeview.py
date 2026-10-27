from ui.widgets import mix


def layout(root):
    """Hierarchical layout: leaves get consecutive slots, parents sit above
    their children. Returns ({id(node): (slot, depth)}, leaf_count, max_depth)."""
    pos = {}
    counter = [0]
    deepest = [0]

    def visit(node, depth):
        if node is None:
            return None
        deepest[0] = max(deepest[0], depth)

        if not node.left and not node.right:
            x = counter[0]
            counter[0] += 1
        else:
            lx = visit(node.left, depth + 1)
            rx = visit(node.right, depth + 1)
            if lx is not None and rx is not None:
                x = (lx + rx) / 2
            else:
                x = lx if lx is not None else rx
        pos[id(node)] = (x, depth)
        return x

    visit(root, 0)
    return pos, counter[0], deepest[0]


def draw_tree(view, t, root, highlight=None, balance=None):
    c = view.canvas
    pos, count, max_depth = layout(root)
    w, h = view.w, view.h

    unit = max(52, min(95, (w - 80) / max(1, count)))
    span = (count - 1) * unit
    x0 = (w - span) / 2 if span <= w - 80 else 40
    vgap = max(60, min(85, (h - 140) / max(1, max_depth)))
    radius = 21

    coords = {}
    nodes = []

    def collect(node):
        if node is None:
            return
        slot, depth = pos[id(node)]
        coords[id(node)] = (x0 + slot * unit, 70 + depth * vgap)
        nodes.append(node)
        collect(node.left)
        collect(node.right)

    collect(root)
    s = view.s

    # edges (smooth S-curves from the bottom dot to the top dot)
    for node in nodes:
        x, y = coords[id(node)]
        for child in (node.left, node.right):
            if child is None:
                continue
            cx, cy = coords[id(child)]
            my = (y + radius + cy - radius) / 2
            pts = [
                view.tx(x, y + radius), view.tx(x, my),
                view.tx(cx, my), view.tx(cx, cy - radius)
            ]
            flat = [v for p in pts for v in p]
            kw = {"dash": (5, 4)} if child.value == highlight else {}
            c.create_line(
                *flat, smooth=True, splinesteps=24,
                fill=t["muted"], width=max(1, 2 * s), **kw
            )

    # nodes
    for node in nodes:
        x, y = coords[id(node)]
        sx, sy = view.tx(x, y)
        r = radius * s
        is_hot = node.value == highlight

        if is_hot:
            for grow, amount in ((14, 0.12), (9, 0.2), (5, 0.32)):
                g = (r + grow * s)
                c.create_oval(
                    sx - g, sy - g, sx + g, sy + g, outline="",
                    fill=mix(t["accent"], t["canvas"], amount)
                )

        c.create_oval(
            sx - r, sy - r, sx + r, sy + r, outline="",
            fill=t["accent"] if is_hot else t["node"]
        )
        c.create_text(
            sx, sy, text=str(node.value), fill="white",
            font=view.font(11)
        )

        dot = max(2, 2.6 * s)
        for dy in (-r, r):
            c.create_oval(
                sx - dot, sy + dy - dot, sx + dot, sy + dy + dot,
                fill=t["text"], outline=""
            )

        if balance is not None:
            c.create_text(
                sx + r + 6 * s, sy, text=f"BF {balance(node)}",
                fill=t["muted"], font=view.font(8, "normal"), anchor="w"
            )
