import __main__
from datetime import date
from artify import utilities



def checkFileExists(filename):
    return __main__.os.path.exists(filename)

def append_file_content(filename, content):
    fullpath = __main__.os.path.join(__main__.path, filename)
    f = open(fullpath, "a+")
    f.write(content)
    f.close()


def create_file(filename, content):
    fullpath = __main__.os.path.join(__main__.path, filename)
    f = open(fullpath, "w+")
    f.write(content)
    f.close()

def fetch_commit_messages():
    git_branch_command = "git rev-parse --abbrev-ref HEAD"
    branchobj = __main__.Popen(git_branch_command, shell=True, stdout=__main__.PIPE, cwd=__main__.path)
    outb, errb = branchobj.communicate()
    branch = outb.decode('utf-8').strip()
    git_log_command = "git log {} --not origin/{} --pretty=%B".format(branch, branch)
    procobj = __main__.Popen(git_log_command, shell=True, stdout=__main__.PIPE, cwd=__main__.path)
    outl, errl = procobj.communicate()
    return outl.decode('utf-8').split("\n\n")
    

def update_changelog():
    chglogfname = "CHANGELOG.md"
    basetext = "# Change Log\n\nAll notable changes to this project will be documented in this file."
    release_date = date.today().strftime("%b-%d-%Y")
    current_version = utilities.get_current_application_version(__main__.path)
    added_list = fetch_commit_messages()
    if __main__.debug == 1:
        print("DEBUG: Changes ::: "," ".join(added_list))
    added_list = list(filter(None, added_list))
    #changed_list = "Authentication framework was updated from Oauth2 to KeyCloak 14"
    changed_list = " ... "
    content = "\n\n============================\n\n[{}] - [{}] \n### Added\n- {}\n\n### Changed\n- {}!".format(current_version, release_date, "\n- ".join(added_list), changed_list)

    if checkFileExists(chglogfname):
        if __main__.debug:
            print("DEBUG: File CHANGELOG.md exist. Updating file")
        else:
            print("INFO: Updating CHANGELOG.md file")
        append_file_content(chglogfname, content)
    else:
        if __main__.debug:
            print("DEBUG: File CHANGELOG.md does not exist. Creating file")
        else:
            print("INFO: Creating CHANGELOG.md file.")
        create_file(chglogfname, basetext)
        append_file_content(chglogfname, content)


