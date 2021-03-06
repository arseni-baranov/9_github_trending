import requests
from datetime import date, timedelta


def format_json_data(json_data):
    # uses get_open_issues_amount to count issues
    repositories = []

    for repo in json_data:
        repository = {
            'repo_name': repo['full_name'].split('/')[0],
            'repo_owner': repo['full_name'].split('/')[1],
            'stars': repo['stargazers_count'],
            'url': repo['html_url'],
            'issues': repo['open_issues_count'],
        }

        repositories.append(repository)

    return repositories


def get_trending_repositories(top_size=20):
    params = {
        "q": "created:>{}".format(date.today() - timedelta(days=7)),
        "sort": "stars",
        "order": "desc",
        "per_page": top_size
    }

    return requests.get('https://api.github.com/search/repositories', params=params).json()['items']


def pretty_print(repositories):
    print(''.center(60, '='), end='\n')
    print('Currently trending on github'.center(60, ' '), end='\n')
    print(''.center(60, '='), end='\n\n')

    for repo in repositories:
        print('\nUrl: {}\nProject: {}\nAuthor: {}\nStars: {}\nIssues: {}\n'.format
              (repo['url'], repo['repo_name'], repo['repo_owner'], repo['stars'], repo['issues']))


def main():
    json_data = get_trending_repositories()
    repositories = format_json_data(json_data)
    pretty_print(repositories)

if __name__ == '__main__':
    main()
