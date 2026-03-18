from itertools import product
from collections import Counter
import argparse


def nonzero_columns(m: int):
    cols = []
    for x in range(1, 2 ** m):
        cols.append([(x >> (m - 1 - i)) & 1 for i in range(m)])
    return cols


def build_hamming_parity_check(m: int):
    cols = nonzero_columns(m)
    n = len(cols)
    return [[cols[j][i] for j in range(n)] for i in range(m)]


def rank_mod2(A):
    A = [row[:] for row in A]
    rows, cols = len(A), len(A[0])
    r = 0

    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if A[i][c]:
                pivot = i
                break

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        for i in range(rows):
            if i != r and A[i][c]:
                A[i] = [x ^ y for x, y in zip(A[i], A[r])]

        r += 1
        if r == rows:
            break

    return r


def xor_vectors(a, b):
    return [x ^ y for x, y in zip(a, b)]


def all_dual_codewords(H):
    m = len(H)        
    n = len(H[0])

    words = []
    for coeffs in product([0, 1], repeat=m):
        v = [0] * n
        for bit, row in zip(coeffs, H):
            if bit:
                v = xor_vectors(v, row)
        words.append(v)

    return words


def weight(v):
    return sum(v)


def check_dual_is_simplex(m: int):
    H = build_hamming_parity_check(m)
    n = len(H[0])
    r = rank_mod2(H)

    dual_words = all_dual_codewords(H)
    weights = [weight(v) for v in dual_words]

    nonzero_weights = sorted({w for w in weights if w > 0})
    spectrum = dict(sorted(Counter(weights).items()))

    result = {
        "m": m,
        "n": n,
        "rank(H)": r,
        "dim(Hamming)": n - r,
        "dim(dual)": r,
        "|dual|": len(dual_words),
        "weight_spectrum_dual": spectrum,
        "all_nonzero_weights": nonzero_weights,
        "expected_simplex_weight": 2 ** (m - 1),
        "is_simplex": (r == m and nonzero_weights == [2 ** (m - 1)]),
    }

    return result


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "--m",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help="Диапазон значений m: от START до END включительно"
    )

    return parser.parse_args()


def get_m_values(args):
    start, end = args.m
    if start > end:
        raise ValueError("В диапазоне start должно быть <= end")
    if start < 2:
        raise ValueError("m должно быть >= 2")

    return list(range(start, end + 1))


def main():
    args = parse_args()
    m_values = get_m_values(args)

    for m in m_values:
        res = check_dual_is_simplex(m)
        print(f"m = {res['m']}")
        print(f"n = {res['n']}")
        print(f"rank(H) = {res['rank(H)']}")
        print(f"dim(Hamming) = {res['dim(Hamming)']}")
        print(f"dim(dual) = {res['dim(dual)']}")
        print(f"|dual| = {res['|dual|']}")
        print(f"Весовой спектр дуального кода: {res['weight_spectrum_dual']}")
        print(f"Ненулевые веса: {res['all_nonzero_weights']}")
        print(f"Ожидаемый вес симплекс-кода: {res['expected_simplex_weight']}")
        print(f"Проверка: dual is simplex -> {res['is_simplex']}")
        print("-" * 60)


if __name__ == "__main__":
    main()    
        