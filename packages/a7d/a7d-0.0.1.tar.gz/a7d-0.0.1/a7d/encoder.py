def encode_node(name, content):
    if isinstance(content, dict):
        return b"/" + name + b"/\n" + encode_nodes(content) + b"\\\n"
    t, content = {"-": b":", "x": b"!", "l": b"@"}[content[0]], content[1]
    return t + name + b"/\n" + content.replace(b" ~ ~", b"\ ~ ~") + b"~ ~ ~\n"


def encode_nodes(nodes):
    return b"".join(encode_node(name, c) for name, c in sorted(nodes.items()))
