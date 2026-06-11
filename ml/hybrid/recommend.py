import logging

log = logging.getLogger(__name__)


def recommend(
    movie_id: int,
    cb,
    cf,
    top_n: int = 10,
    min_ratings: int = 10,
) -> list[dict]:
    if cf.rating_counts.get(movie_id, 0) >= min_ratings:
        return cf.recommend(movie_id, top_n)
    return cb.recommend(movie_id, top_n)


def recommend_multiple(
    movie_ids: list[int],
    cb,
    cf,
    top_n: int = 10,
    min_ratings: int = 10,
) -> list[dict]:
    popular = [
        m
        for m in movie_ids
        if cf.rating_counts.get(m, 0) >= min_ratings
    ]
    rare = [m for m in movie_ids if m not in popular]

    cf_map = _score_map(cf, popular) if popular else {}
    cb_map = _score_map(cb, rare) if rare else {}

    merged = {
        mid: cf_map.get(mid, cb_map.get(mid, 0))
        for mid in set(cf_map) | set(cb_map)
    }

    exclude = set(movie_ids)
    sorted_items = sorted(merged.items(), key=lambda x: x[1], reverse=True)

    results = []
    for mid, score in sorted_items:
        if mid in exclude:
            continue
        results.append({"movie_id": mid, "score": round(score, 2)})
        if len(results) == top_n:
            break
    return results


def _score_map(recommender, movie_ids: list[int]) -> dict:
    if not movie_ids:
        return {}
    indices = []
    for mid in movie_ids:
        try:
            indices.append(recommender.movie_ids.index(mid))
        except ValueError:
            continue
    if not indices:
        return {}
    avg = recommender.similarity_matrix[indices].mean(axis=0)
    return {
        recommender.movie_ids[i]: float(avg[i])
        for i in range(len(recommender.movie_ids))
    }
