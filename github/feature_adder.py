import csv
import pickle

endpoint = 'https://api.github.com/search/repositories'
token = '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'

# Make a request to search for repositories with more than 100,000 stars
params = {'q': 'stars:>1000', 'sort': 'stars', 'per_page': 100, 'page': 1}

repos = []

# Loop through the API responses until we have 1000 repositories
# while len(repos) < 1000:
#     print(f'Fetching page {params["page"]}')
#     response = requests.get(endpoint, params=params)
#     response_json = response.json()
#     repos += response_json['items']
#     params['page'] += 1

# with open('repos.pkl', 'wb') as f:
#     pickle.dump(repos, f)

language_dict = {}

def get_language_int(language):
    if language not in language_dict:
        language_dict[language] = len(language_dict) + 1
    return language_dict[language]
    
with open('repos.pkl', 'rb') as f:
    repos = pickle.load(f)

with open("top_repos_old.csv", 'r') as file:
    reader = csv.reader(file)
    lines = list(reader)  # Read all lines into a list

header = lines[0]  # Get the header
header.extend(["Size", "Language", "Has Issues", "Has Projects", "Has Downloads", "Has Wiki", "Has Pages", "Has Discussions"])  # Add the new column name

for i, repo, line in zip(range(1, len(repos)), repos, lines[1:]):
    size = repo['size']
    # language = get_language_int(repo['language'])
    language = repo['language']
    has_issues = repo['has_issues']
    has_projects = repo['has_projects']
    has_downloads = repo['has_downloads']
    has_wiki = repo['has_wiki']
    has_pages = repo['has_pages']
    has_discussions = repo['has_discussions']

    line.extend([size, language, has_issues, has_projects, has_downloads, has_wiki, has_pages, has_discussions])  # Add the new column value

with open('top_repos.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerows(lines)
    