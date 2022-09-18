#  Terroriser CID: UUQiojTHkAvFvdCSajklqUXA
#  Nogla Upload PlayList ID:  UUvPW1W4WlpTgNezZzwIstLA
#  Test Upload ID ~ Pastaroni Ravioli: UUATTw05PU3RYx0KqC1gAlhA

import os
import googleapiclient.discovery
import sys
import secrets


def parser(channel_id, keyword, youtube):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=channel_id
    )
    response = request.execute()

    requests_quantity = int((response['pageInfo']['totalResults']) / 50)

    keyword_count = 0

    for x in range(requests_quantity + 1):
        for y in range(len(response['items'])):
            title = str((response['items'][y]['snippet']['title']).lower()).split()

            if keyword in title:
                with open('terroriser_titles.txt', 'a') as file:
                    file.write(f"{title}\n")

                file.close()

                keyword_count += 1

        try:
            page_token = response['nextPageToken']

            request = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId=channel_id,
                pageToken=page_token
            )
        except KeyError:
            request = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId=channel_id,
            )

        response = request.execute()

    return keyword_count

def setup(channel_id, keyword):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = secrets.YOUTUBE_API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    return parser(channel_id, keyword, youtube)


if __name__ == "__main__":
    args = sys.argv
    keyword_count = setup(args[1], args[2])
    print(keyword_count)
