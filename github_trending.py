import requests
from datetime import date, timedelta

github_api = 'https://api.github.com'
week_ago = date.today() - timedelta(days=7)
top_size = 20


def get_open_issues_amount(repo_name, repo_owner):
    return len(requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_name, repo_owner)).json())


def format_json_data(json_data):
    # uses get_open_issues_amount to count issues
    repositories = []

    for repo in json_data:
        repository = {
            'repo_name': repo['full_name'].split('/')[0],
            'repo_owner': repo['full_name'].split('/')[1],
            'stars': repo['stargazers_count'],
            'url': repo['html_url'],
            'issues': get_open_issues_amount(repo['full_name'].split('/')[0],
                                             repo['full_name'].split('/')[1])
        }

        repositories.append(repository)

    return repositories


def get_trending_repositories(top_size):
    params = {
        "q": "created:>{}".format(week_ago),
        "sort": "stars",
        "order": "desc",
        "per_page": top_size
    }

    return requests.get(github_api+'/search/repositories', params=params).json()['items']


def pretty_print(repositories):
    print(''.center(60, '='), end='\n')
    print('Currently trending on github'.center(60, ' '), end='\n')
    print(''.center(60, '='), end='\n\n')

    for repo in repositories:
        print('\nUrl: {}\nProject: {}\nAuthor: {}\nStars: {}\nIssues: {}\n'.format
              (repo['url'], repo['repo_name'], repo['repo_owner'], repo['stars'], repo['issues']))


def main():
    json_data = get_trending_repositories(top_size)
    repositories = format_json_data(json_data)
    pretty_print(repositories)

if __name__ == '__main__':
    main()
