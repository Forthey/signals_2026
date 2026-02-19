from itertools import product


def matmul_gf2(vec: list[int], G: list[list[int]]) -> list[int]:
    k = len(vec)
    n = len(G[0])
    out = [0] * n
    for j in range(n):
        s = 0
        for i in range(k):
            s ^= (vec[i] & G[i][j])
        out[j] = s
    return out


def hamming_weight(x: list[int]) -> int:
    return sum(x)


def hamming_distance(a: list[int], b: list[int]) -> int:
    return sum((ai ^ bi) for ai, bi in zip(a, b))


def all_codewords(G: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    k = len(G)
    msgs = [list(m) for m in product([0, 1], repeat=k)]
    cws = [matmul_gf2(m, G) for m in msgs]
    return msgs, cws


def min_distance(codewords: list[list[int]]) -> int:
    dmin = None
    m = len(codewords)
    for i in range(m):
        for j in range(i + 1, m):
            d = hamming_distance(codewords[i], codewords[j])
            if dmin is None or d < dmin:
                dmin = d
    return 0 if dmin is None else dmin


def distance_matrix(codewords: list[list[int]]) -> list[list]:
    m = len(codewords)
    D = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            d = hamming_distance(codewords[i], codewords[j])
            D[i][j] = d
            D[j][i] = d
    return D


def format_bits(x: list[int]) -> str:
    return " ".join(str(b) for b in x)


def main():
    G = [
        [1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 1, 1, 1, 0],
    ]

    msgs, cws = all_codewords(G)

    weights = [hamming_weight(c) for c in cws]

    dmin = min_distance(cws)

    D = distance_matrix(cws)

    print("G (k x n):")
    for row in G:
        print("  ", format_bits(row))
    print()

    print(f"Количество кодовых слов: {len(cws)} (2^{len(G)})")
    print(f"d_min: {dmin}")
    print()

    print("Кодовые слова")
    for i, (m, c, w) in enumerate(zip(msgs, cws, weights)):
        print(f"{i}:\t{format_bits(m)} -> {format_bits(c)}  [w={w}]")
    print()

    print("Расстояния между кодовыми словами:")
    header = "\t" + " ".join(f"{i:2d}" for i in range(len(cws)))
    print(header)
    for i, row in enumerate(D):
        print(f"{i:2d}:\t" + " ".join(f"{d:2d}" for d in row))


if __name__ == "__main__":
    main()
