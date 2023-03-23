import requests
import json
import os

def get_github_repo_info(repo_name, username=None):
    # Recherche des dépôts ayant un nom similaire
    search_url = f"https://api.github.com/search/repositories?q={repo_name}"
    if username:
        search_url += f"+user:{username}"
    response = requests.get(search_url)
    search_results = json.loads(response.text)

       
     # Affichage des dépôts similaires trouvés
    items = search_results['items']
    if len(items) == 0:
        print(f"No deposits found with the name '{repo_name}'.")
        return
    
    # Affichage des dépôts trouvés
    print(f"Here are the similar deposits found for {repo_name}:")
    for index, repo in enumerate(search_results["items"]):
        print(f"{index+1}. {repo['full_name']}")

    # Demande de l'utilisateur pour choisir un dépôt
    selected_index = int(input("Enter the deposit number you wish to display: ")) - 1
    selected_repo = search_results["items"][selected_index]

    # Récupération des informations sur le dépôt
    repo_url = selected_repo["url"]
    response = requests.get(repo_url)
    repo_info = json.loads(response.text)

    # Affichage des informations sur le dépôt
    print(f"\nInformation about {repo_info['name']}:")
    print(f"Nom du dépôt                  ::  {repo_info['name']}")
    print(f"Auteur                        ::  {repo_info['owner']['login']}")
    print(f"Description                   ::  {repo_info['description']}")
    print(f"Nombre d'étoiles              ::  {repo_info['stargazers_count']}")
    print(f"Langage principal             ::  {repo_info['language']}")
    print(f"Date de création              ::  {repo_info['created_at']}")
    print(f"Date de dernière mise à jour  ::  {repo_info['updated_at']}")
    print(f"URL du dépôt                  ::  {repo_info['html_url']}")
    print(f"URL de clonage                ::  {repo_info['clone_url']}")
    print(f"License                       ::  {repo_info['license']['name'] if repo_info['license'] else 'None'}")

    # Demande de l'utilisateur pour choisir la branche
    branches_url = f"{repo_info['url']}/branches"
    response = requests.get(branches_url)
    branches_info = json.loads(response.text)
    print(f"\nVoici les branches du dépôt {repo_info['name']}:")
    for index, branch in enumerate(branches_info):
        print(f"{index+1}. {branch['name']}")
    selected_branch_index = int(input("Entrez le numéro de la branche que vous souhaitez télécharger: ")) - 1
    selected_branch = branches_info[selected_branch_index]['name']

    # Demande de l'utilisateur pour télécharger le dépôt
    download_choice = input("Voulez-vous télécharger ce dépôt ? (y/n) ")
    if download_choice == "y":
        download_url = repo_info["clone_url"]
        download_dir = input("Entrez le répertoire de téléchargement: ")
        download_command = f"git clone -b {selected_branch} {download_url} {download_dir}"
        print(f"Téléchargement en cours avec la commande : {download_command}")
        os.system(download_command)


if __name__ == '__main__':
    repo_name = input("Enter the name of a GitHub repository: ")
    repo_author = input("Enter the name of the author of the repository (for better searching): ")
    get_github_repo_info(repo_name=repo_name,username=repo_author)