"""
Twitter APIでTweet検索を実行する
https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
https://github.com/twitterdev/Twitter-API-v2-sample-code

Bearer Tokenはdotfiles (.bash_profile) に記述
"""

import requests
import os
import json

class TwitterSearch():
    def __init__(self) -> None:
        self.bearer_token = os.environ.get("BEARER_TOKEN")

    def bearer_oauth(self, r: requests.Request):
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        # r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        # r.headers["User-Agent"] = "v2SpacesSearchPython"
        return r

    def connect_to_endpoint(self, url: str, params: dict) -> dict:
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        print('HTTP STATUS:', response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

def main():
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    # search_url = "https://api.twitter.com/2/tweets/search/all"
    # search_url = "https://api.twitter.com/2/spaces/search"

    query = '(-is:retweet has:media lang:ja) (油絵 OR 油彩)'
    expansions = 'attachments.media_keys,referenced_tweets.id'
    media_fields = 'type,url,height,width'
    tweet_fields = 'created_at,entities,public_metrics'
    query_params = {'query': query, 'max_results': 50, 'expansions': expansions, 'media.fields': media_fields, 'tweet.fields': tweet_fields}

    twitter = TwitterSearch()
    json_response = twitter.connect_to_endpoint(search_url, query_params)
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    indices = []
    for (index, tweet) in enumerate(json_response['data']):
        if tweet['public_metrics']['like_count'] < 10:
            indices.append(index)

    for index in reversed(indices):
        del json_response['data'][index]
        del json_response['includes']['media'][index]

    with open('./test.json', 'w', encoding='utf8') as f:
        json.dump(json_response, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    main()
