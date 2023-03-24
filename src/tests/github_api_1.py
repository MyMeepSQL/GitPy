import src.tools.requests as requests
import json
import subprocess

def get_github_repo_info(repo_name):
    # Recherche des dépôts avec le nom donné
    search_url = f'https://api.github.com/search/repositories?q={repo_name}'
    response = requests.get(search_url)
    response_json = json.loads(response.text)

    # Affichage des dépôts similaires trouvés
    items = response_json['items']
    if len(items) == 0:
        print(f"No deposits found with the name '{repo_name}'.")
        return

    print(f"Here are the similar deposits found for '{repo_name}':\n")
    for i, item in enumerate(items):
        print(f"{i+1}. {item['full_name']}")

    # Demande de choix de dépôt à l'utilisateur
    while True:
        choice = input("\nEnter the deposit number you wish to display: ")
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(items):
            print(f"Invalid choice. Please enter a number between 1 and {len(items)}.")
        else:
            break

    # Récupération des informations sur le dépôt choisi
    selected_repo = items[int(choice)-1]
    repo_url = selected_repo['url']
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(repo_url, headers=headers)
    repo_info = json.loads(response.text)

    # Affiche les informations du dépôt
    print(f"\nInformation about {repo_info['name']}:")
    print(f"Author: {repo_info['owner']['login']}")
    print(f"Description: {repo_info['description']}")
    print(f"Language: {repo_info['language']}")
    print(f"Number of stars: {repo_info['stargazers_count']}")
    print(f"Number of forks: {repo_info['forks_count']}")
    print(f"Creation date: {repo_info['created_at']}")
    print(f"Last update: {repo_info['updated_at']}")
    print(f"URL: {repo_info['html_url']}")
    print(f"License: {repo_info['license']['name'] if repo_info['license'] else 'None'}")

    # Download the repo
    download_url = repo_info['clone_url']
    choice = input(' Do you want to download the repo? (y/n)')
    if choice == 'y':

        print('where do you want to download the repo? (default: current directory)')
        path = input(' > ')

        if path:

            print(" Downloading %s in %s..." % (repo_info['name'],path))

            subprocess.run('git clone %s %s' % (download_url, path), shell=True)

            print(' Done!')

        else:
            print(" Downloading %s in the current directory..." % repo_info['name'])

            subprocess.run('git clone %s' % download_url, shell=True)

            print(' Done!')

    else:

        print(' Ok.')

if __name__ == '__main__':
    repo_name = input("Enter the name of a GitHub repository: ")
    get_github_repo_info(repo_name)