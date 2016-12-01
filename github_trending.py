import requests
from datetime import date, timedelta


def get_trending_repositories(time_period, amount):

    payload = {
        "q": "created:>{}".format(time_period),
        "sort": "stars",
        "order": "desc",
        "per_page": amount
    }

    repositories_data = requests.get('https://api.github.com/search/repositories', payload).json()['items']
    return [name for name in repositories_data]


def get_open_issues_amount(repo_name, repo_owner):
    open_issues = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_name, repo_owner)).json()

    return len(open_issues)


def main():
    week_ago = date.today() - timedelta(days=7)

    print()
    print('Most popular projects @ github:')
    print()

    try:
        for name in get_trending_repositories(week_ago, 20):
            repo_name, repo_owner = name['full_name'].split('/')

            print('https://api.github.com/repos/{}/{}/issues'.format(repo_name, repo_owner))
            print(repo_name, 'by', repo_owner)
            print('stars: ', name['stargazers_count'])
            print('issues:', get_open_issues_amount(repo_name, repo_owner))
            print()
    except Exception as error:
        print('An error has occurred:', error)

if __name__ == '__main__':
    main()
