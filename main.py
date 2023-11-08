"""
TODO:
- Add stage from issue
UPDATE ISSUES
1. Get credentials from .env
2. Get issues with 'tracked/yes' from kubernetes/enhancements
3. Push issues to Notion - fields include: stage, name, number

UPDATE STATUS
1. Check each row for k/k column
2. Update status to `tracked` if all merged
"""
import requests, json
def getGithubIssues():
    params = {"labels":"tracked/yes", "per_page":"200"}
    url = "https://api.github.com/repos/kubernetes/enhancements/issues"
    issues = requests.get(url, params=params).json()
    return list(reversed(issues))

def putIssuesInNotion(issues):
    url = "https://api.notion.com/v1/pages"
    params = {"Authorization":"Bearer secret_<redacted>", 
            "Content-Type":"application/json",
            "Notion-Version":"2021-05-13"}

    for i in issues:
      print(i)
      issueURL = i['html_url']
      issueTitle = i['title']
      issueNumber = int(i['number'])
      data = {
        "parent": {"database_id":"<redacted>"}, 
        "properties": {
          "Name" : {
            "title": [
              {"text": {"content": issueTitle}}
            ]
          },
          "Issue Number" : {
            "number": issueNumber
          },
          "Issue URL": {
            "url": issueURL
          }
        }            
      }
      res = requests.post(url, headers=params, data = json.dumps(data))

def getNotionPages():
    import requests

    url = "https://api.notion.com/v1/databases/<redacted>/query"

    payload = {"page_size": 1}
    headers = {
                "Accept": "application/json",
                    "Notion-Version": "2022-02-22",
                        "Content-Type": "application/json",
                            "Authorization": "Bearer secret_<redacted>"
                            }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

def validatePR():
    return 0

issues = getGithubIssues()
putIssuesInNotion(issues)
# getNotionPages()
