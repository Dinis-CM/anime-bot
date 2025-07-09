def normalize_score(score, score_format):
    if score_format == 'POINT_100':
        return score
    elif score_format == 'POINT_10':
        return score * 10
    elif score_format == 'POINT_10_DECIMAL':
        return round(score * 10)
    elif score_format == 'POINT_5':
        return score * 20
    elif score_format == 'POINT_3':
        # Typically: 1 = Bad (33), 2 = Average (66), 3 = Good (100)
        return {1: 33, 2: 66, 3: 100}.get(score, 0)
    return 0