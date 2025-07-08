import requests

ANILIST_API = 'https://graphql.anilist.co'

# GraphQL query to get score format and media list
query = '''
query ($username: String, $page: Int) {
  User(name: $username) {
    mediaListOptions {
      scoreFormat
    }
  }
  Page(page: $page, perPage: 50) {
    pageInfo {
      currentPage
      hasNextPage
    }
    mediaList(userName: $username, type: ANIME) {
      media {
        title {
          romaji
          english
        }
      }
      score
      status
    }
  }
}
'''

# Normalize score based on the user's scoring system
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

def get_all_normalized_scores(username):
    page = 1
    scores = []

    # Initial request to get score format and first page
    variables = {'username': username, 'page': page}
    response = requests.post(ANILIST_API, json={'query': query, 'variables': variables})
    data = response.json()

    score_format = data['data']['User']['mediaListOptions']['scoreFormat']
    print(f"{username}'s score format: {score_format}")

    while True:
        for entry in data['data']['Page']['mediaList']:
            title_data = entry['media']['title']
            title = title_data['english'] or title_data['romaji']
            raw_score = entry['score']
            normalized = normalize_score(raw_score, score_format)

            scores.append({
                'title': title,
                'raw_score': raw_score,
                'normalized_score': normalized,
                'status': entry['status']
            })

        if not data['data']['Page']['pageInfo']['hasNextPage']:
            break
        page += 1
        variables['page'] = page
        response = requests.post(ANILIST_API, json={'query': query, 'variables': variables})
        data = response.json()

    return scores

# Example usage
username = "JellyJelmo"  # Change this to your AniList username
all_scores = get_all_normalized_scores(username)

# Print results
for s in all_scores:
    print(f"{s['title']}: raw={s['raw_score']}, normalized={s['normalized_score']} (status: {s['status']})")
