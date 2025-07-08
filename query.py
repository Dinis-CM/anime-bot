import requests

def get_media_details(API, title, category):
    query = '''
    query ($search: String) {
      Media(search: $search, type: $category) {
        id
        title {
          romaji
          english
        }
      }
    }
    '''
    variables = {"search": title, "type": category.upper()}
    response = requests.post(API, json={"query": query, "variables": variables})
    response.raise_for_status()
    media_id = response.json()['data']['Media']['id']

    query = '''
    query ($id: Int) {
      Media(id: $id, type: $category) {
        id
        title {
          romaji
          english
          native
        }
        format
        status
        season
        seasonYear
        episodes
        duration
        averageScore
        popularity
        favourites
        genres
        description(asHtml: false)
        coverImage {
          large
        }
      }
    }
    '''
    variables = {"id": media_id, "category": category.upper()}
    response = requests.post(API, json={"query": query, "variables": variables})
    response.raise_for_status()
    return response.json()['data']['Media']