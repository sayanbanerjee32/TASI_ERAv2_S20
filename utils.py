import regex as re

def get_stats(ids, counts= None):
    counts = {} if counts is None else counts
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts

def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(ids[i])
            i += 1
    return newids

def _encode_chunk(text_bytes, merges):
        # return the token ids
        # let's begin. first, convert all bytes to integers in range 0..255
        ids = list(text_bytes)
        while len(ids) >= 2:
            # find the pair with the lowest merge index
            stats = get_stats(ids)
            pair = min(stats, key=lambda p: merges.get(p, float("inf")))
            # subtle: if there are no more merges available, the key will
            # result in an inf for every single pair, and the min will be
            # just the first pair in the list, arbitrarily
            # we can detect this terminating case by a membership check
            if pair not in merges:
                break # nothing else can be merged anymore
            # otherwise let's merge the best pair (lowest merge index)
            idx = merges[pair]
            ids = merge(ids, pair, idx)
        return ids

def encode(text, regex_pat, merges):
    # split text into chunks of text by categories defined in regex pattern
    text_chunks = re.findall(regex_pat, text)
    # all chunks of text are encoded separately, then results are joined
    ids = []
    for chunk in text_chunks:
        chunk_bytes = chunk.encode("utf-8") # raw bytes
        chunk_ids = _encode_chunk(chunk_bytes, merges)
        ids.extend(chunk_ids)
    return ids

def decode(ids, vocab):
    # given ids (list of integers), return Python string
    part_bytes = []
    for idx in ids:
        if idx in vocab:
            part_bytes.append(vocab[idx])
        else:
            raise ValueError(f"invalid token id: {idx}")
    text_bytes = b"".join(part_bytes)
    text = text_bytes.decode("utf-8", errors="replace")
    return text
