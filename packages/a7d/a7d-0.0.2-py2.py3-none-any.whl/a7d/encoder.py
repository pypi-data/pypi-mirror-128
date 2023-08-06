def encode_node(name, content):
    if isinstance(content, dict):
        return b"/" + name + b"/\n" + encode_nodes(content) + b"\\\n"
    t, content = {"-": b":", "x": b"!", "l": b"@"}[content[0]], content[1]
    content = content.replace(b" ~ ~\n", b"\ ~ ~\n") + b"~ ~ ~\n"
    return t + name + b"/\n" + content


def encode_nodes(nodes):
    return b"".join(encode_node(name, c) for name, c in sorted(nodes.items()))
