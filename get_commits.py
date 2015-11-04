import requests
'''
Creation of a token is documented at
https://help.github.com/articles/creating-an-access-token-for-command-line-use/
'''
#  auth1 = ('user-id', 'token')



def calculate_pages(request):
    for item in request.headers['link'].split(','):
        if 'last' in item.split(';')[1]:
            start = item.split(';')[0].find('page')
            end = item.split(';')[0].find('>')
            return int(item.split(';')[0][start:end].split('=')[1])


def calculate_commits(repos):
    num_of_labs_worked_on = 0
    for repo in repos:
        print "name = %s, id = %s" % (repo['name'], repo['id'])
        url = "%s%s%s" % ('https://api.github.com/repositories/',
                          repo['id'],
                          '/stats/commit_activity')
        print "url = %s" % url
        commit_act = requests.get(url, auth=auth1)
        try:
            total = 0
            for list in commit_act.json():
                total = total + int(list['total'])
            if total > 0:
                num_of_labs_worked_on += total
            print "total = %d" % total
        except Exception:
            print "Exception Total = 0"
    print "no_of_labs = %d" % num_of_labs_worked_on


def get_issues_for_each_repo(repos):
    for repo in repos:
        url = "%s%s%s" % ('https://api.github.com/repositories/',
                          repo['id'],
                          '/issues')
        print url
        print requests.get(url, auth=auth1).json()


def get_commit_info(repos):
    for repo in repos:
        print "name = %s, id = %s" % (repo['name'], repo['id'])
        url = "%s%s%s" % ('https://api.github.com/repositories/',
                          repo['id'],
                          '/commits')
        print "url = %s" % url
        commit_act = requests.get(url, auth=auth1)
        try:
            for list in commit_act.json():
                print "commit sha = %s" % list['sha']
                print "committer = %s" % list['commit']['author']['name']
                print "Date = %s" % list['commit']['author']['date']
        except Exception:
            print "Exception Total = 0"


def get_repos(get_object):
    global repos
    if get_object is None:
        url = 'https://api.github.com/orgs/Virtual-Labs/repos'
        request = requests.get(url, auth=auth1)
        get_repos(request)

    else:
        if 'last' not in get_object.links.keys():
            repos.extend(get_object.json())
            return
        else:
            url = get_object.links['next']['url']
            request = requests.get(url, auth=auth1)
            repos.extend(get_object.json())
            get_repos(request)


if __name__ == '__main__':
    repos = []
    get_repos(None)
    print "length = %s" % len(repos)
    #  calculate_commits(repos)
    get_commit_info(repos)
