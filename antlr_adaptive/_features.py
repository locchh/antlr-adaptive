"""Feature extraction from ANTLR parse state."""

N_DECISIONS   = 270   # covers SQLite's 263; tune up for larger grammars
N_TOKEN_TYPES = 120
N_STATE_BITS  = 64
FEATURE_DIM   = N_DECISIONS + 3 * N_TOKEN_TYPES + N_STATE_BITS  # 694


def extract_features(input_stream, decision: int, ctx) -> list:
    """
    Build a fixed-length feature vector from the current parse state.

    Layout:
      [0..N_DECISIONS)           one-hot of decision index
      [N_DECISIONS..+3*N_TOKEN)  one-hot of LA(1), LA(2), LA(3) token types
      [N_DECISIONS+3*N_TOKEN..)  invoking state mod N_STATE_BITS
    """
    f = [0.0] * FEATURE_DIM

    if 0 <= decision < N_DECISIONS:
        f[decision] = 1.0

    offset = N_DECISIONS
    for k in range(1, 4):
        try:
            t = input_stream.LA(k)
            if t is not None and 0 <= t < N_TOKEN_TYPES:
                f[offset + (k - 1) * N_TOKEN_TYPES + t] = 1.0
        except Exception:
            pass

    if ctx is not None and ctx.invokingState >= 0:
        f[N_DECISIONS + 3 * N_TOKEN_TYPES + (ctx.invokingState % N_STATE_BITS)] = 1.0

    return f
