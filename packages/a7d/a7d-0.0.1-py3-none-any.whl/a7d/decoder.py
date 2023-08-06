def decode_content(bts, start=0):
    i = bts.find(b"~ ~ ~\n", start)
    assert i != -1
    return bts[start:i].replace(b"\ ~ ~\n", b" ~ ~\n"), i


def decode_name(bts, start=0):
    i = bts.find(ord("/"), start)
    return bts[start:i], i


def decode_directory(bts, start=0):
    assert bts[start] == ord("/")
    name, i = decode_name(bts, start + 1)
    assert bts[i + 1] == ord("\n")
    nodes, j = decode_nodes(bts, i + 2)
    assert bts[j : j + 2] == b"\\\n"
    return name, nodes, j + 2


def decode_node(bts, start=0):
    t = {ord("@"): "l", ord("!"): "x", ord(":"): "-", ord("/"): "d"}[bts[start]]
    name, i = decode_name(bts, start + 1)
    assert bts[i + 1] == ord("\n")
    if t == "d":
        nodes, j = decode_nodes(bts, i + 2)
        assert bts[j : j + 2] == b"\\\n"
        return name, nodes, j + 2
    content, j = decode_content(bts, i + 2)
    return name, (t, content), j + 6


def decode_nodes(bts, start=0):
    i, nodes = start, {}
    while i < len(bts) and bts[i] != b"\\"[0]:
        name, content, i = decode_node(bts, i)
        nodes[name] = content
    return nodes, i
