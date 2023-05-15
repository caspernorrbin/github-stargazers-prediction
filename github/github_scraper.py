import requests
import csv
import re
from bs4 import BeautifulSoup as bs
import pickle

endpoint = 'https://api.github.com/search/repositories'
token = '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'

# Make a request to search for repositories with more than 100,000 stars
params = {'q': 'stars:>1000', 'sort': 'stars', 'per_page': 100, 'page': 1}
# response = requests.get(endpoint + '/search/repositories', params=params)
# repositories = response.json()['items']

# print(repositories)

repos = []

# # Loop through the API responses until we have 1000 repositories
# while len(repos) < 1000:
#     print(f'Fetching page {params["page"]}')
#     response = requests.get(endpoint, params=params)
#     response_json = response.json()
#     repos += response_json['items']
#     params['page'] += 1

# with open('repos.pkl', 'wb') as f:
#     pickle.dump(repos, f)
    
with open('repos.pkl', 'rb') as f:
    repos = pickle.load(f)

with open('top_repos.csv', mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    # writer.writerow(['Name', 'Forks', 'Watchers', 'Contributors', 'Commits', 'Branches', 'Open Issues', 'Closed Issues', 'Open PRs', 'Closed PRs', 'Stargazers'])
    
    for i, repo in enumerate(repos[200:]):
        print(f'Fetching repo {i+1}, {repo["name"]}')
        repo_url = repo['url']
        repo_response = requests.get(
            repo_url, headers={'Authorization': f'token {token}'})
        repo_json = repo_response.json()
        
        url = repo_json['html_url']
        name = repo_json['name']
        stargazers_count = repo_json['stargazers_count']
        forks_count = repo_json['forks_count']
        watchers_count = repo_json['subscribers_count']
        
        has_issues = repo_json['has_issues']

        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        contributors_s = soup.select_one(
            'a:contains("Contributors") span.Counter')

        if contributors_s is None:
            contributors = 1
        else:
            contributors_s = contributors_s.text
            if contributors_s != '5,000+':
                contributors = int(contributors_s.replace(',', ''))
            else:
                contributors_s = soup.select_one('a:contains(" contributors")')
                contributors_s = contributors_s.text.translate({ord(i): None for i in '+,\n contributors'})
                contributors = int(contributors_s) + 11

        commits_span = soup.find(
            'span', class_="color-fg-muted d-none d-lg-inline")

        num_commits_s = commits_span.find_previous_sibling(
            'strong').text.replace(',', '')
        num_commits = int(num_commits_s)

        branches_span = soup.find('span', text="branches")
        if branches_span is None:
            branches_span = soup.find('span', text="branch")
        # print(branches_span)
        num_branches_s = branches_span.find_previous_sibling(
            'strong').text.replace(',', '')
        num_branches = int(num_branches_s)
        
        open_issues_count = None
        closed_issues_count = None
        if has_issues == "true":
            issues_url = url + '/issues'
            response = requests.get(issues_url)
            soup = bs(response.text, 'html.parser')
            
            issues_div = soup.find(
                'div', class_='table-list-header-toggle states flex-auto pl-0')
            
            issues_counts_a = issues_div.find_all('a')
            
            open_issues_s = issues_counts_a[0].text
            closed_issues_s = issues_counts_a[1].text
            
            open_issues_s = open_issues_s.translate({ord(i): None for i in ' Open,\n'})
            closed_issues_s = closed_issues_s.translate({ord(i): None for i in ' Closed,\n'})
            
            open_issues_count = int(open_issues_s)
            closed_issues_count = int(closed_issues_s)
        
        pr_url = url + '/pulls'
        response = requests.get(pr_url)
        soup = bs(response.text, 'html.parser')
        
        pr_div = soup.find(
            'div', class_='table-list-header-toggle states flex-auto pl-0')
        
        pr_counts_a = pr_div.find_all('a')
        
        open_pr_s = pr_counts_a[0].text
        closed_pr_s = pr_counts_a[1].text
        
        open_pr_s = open_pr_s.translate({ord(i): None for i in ' Open,\n'})
        closed_pr_s = closed_pr_s.translate({ord(i): None for i in ' Closed,\n'})
        
        open_pr_count = int(open_pr_s)
        closed_pr_count = int(closed_pr_s)
        
        writer.writerow([name, forks_count, watchers_count, contributors, num_commits, num_branches, open_issues_count, closed_issues_count, open_pr_count, closed_pr_count, stargazers_count])
    