import subprocess

def check_remote(target_directory):
    """
    checks if the target directory has remote repo or not
    """
    remote = subprocess.run(["git", "remote"],capture_output=True,cwd=target_directory,text=True)    
    if remote.stdout.strip():
        return True
    else:
        return False

def get_unpushed_hashes(target_directory):
   """
   returns only local hases into an list
   """
   local_hashs = subprocess.run(["git", "log", "--branches", "--not","--remotes", "--format=%h"],capture_output=True,text=True,cwd=target_directory)
   if local_hashs.returncode != 0:
       return []
         
   return local_hashs.stdout.splitlines()

def is_valid_repo(target_directory):
    """
    Checks if the target directory is actually a Git repository.
    """
    check = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=target_directory,
        capture_output=True,
        text=True
    )
    
    return check.returncode == 0

def get_logs(target_directory):
    """
    returns git logs include commit hash(%h), commit date(%cd) and subject(%s)
    checks if the given dir has initialized git or not
    """
    git_log = subprocess.run(["git", "log", "-n", "5", "--pretty=format:%h|%cd|%s"],cwd=target_directory, capture_output=True, text=True)
    if git_log.returncode != 0:
        print(f"Git error:{git_log.stderr.strip()}")
    return git_log.stdout
    
def split_lines(log_text,check_remote,unpushed_list):
    """
    split the log lines into three parts that include the commit line,date and the message
    """
    lines = log_text.splitlines()
    result = []
    for line in lines:
        #handle blank lines and whitespace-only lines
        if not line.strip():
            continue

        parts = line.split("|",2)

        if len(parts) != 3:
            print(f"Warning: Malformed commit data rejected -> {line}")
            continue
        
        current_hashes = parts[0]
        current_status = ""
        if check_remote == False:
            current_status = "local only"
        elif check_remote == True and current_hashes in unpushed_list:
            current_status = "unpushed" 
        elif check_remote == True and current_hashes not in unpushed_list:
            current_status = "pushed"

        result.append({
            "commit": parts[0],
            "date": parts[1],
            "message": parts[2],
            "status": current_status
            })
    return result
