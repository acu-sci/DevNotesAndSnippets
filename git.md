# Git Concepts and Commands

## Basic Setup

- Set user name and email (to show up in commits):
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

- Generate an SSH key for your local machine (if it doesn't already have one):
    ```bash
    ssh-keygen -t rsa -C "your.email@example.com"
    ```

- Display the SSH key to copy it:
    ```bash
    cat ~/.ssh/id_rsa.pub
    ```

Then you can paste the SSH key into your GitLab, GitHub, or other Git provider's SSH key section. 

## Working with Repositories

- To clone a repository into a specific location:
    ```bash
    cd path/to/your/folder
    git clone git@example.com:username/repository.git
    ```

## Updating Your Repository

- Check the changes made to your files:
    ```bash
    git status
    ```

- Add the files to staging:
    ```bash
    git add FILE-NAME
    ```

   Or add all files:
    ```bash
    git add *
    ```

- Commit the changes:
    ```bash
    git commit -m "Your awesome commit message here"
    ```

- Send changes to the branch:
    ```bash
    git push origin BRANCH-NAME
    ```

## Pulling Changes

'Safe' variation:

- Download information from the branch:
    ```bash
    git fetch origin master
    ```

- Merge with the local changes:
    ```bash
    git merge origin master
    ```

'Fast' variation: 
```bash
git pull origin master
```

## Branch Management

- To see all branches of a git project:
    ```bash
    git branch -r
    ```

- To create a new branch and switch to it:
    ```bash
    git checkout -b new_branch_name
    ```
    
## Checking Out and Merging Branches
<br>

- Check out a branch:
    ```bash
    git checkout BRANCH-NAME
    ```

- Merge the master branch into a specific branch:
  
  First, check out the branch you want to merge into:
    ```bash
    git checkout BRANCH-NAME
    ```
  
  Then, pull changes from the master branch:
    ```bash
    git pull origin master
    ```
  Alternatively, you can use the `merge` command to combine the master branch into your current branch:
    ```bash
    git merge master
    ```

- Merge a specific branch into the master branch:

  First, check out the master branch:
    ```bash
    git checkout master
    ```

  Then, pull changes from the specific branch:
    ```bash
    git pull origin BRANCH-NAME
    ```
  Alternatively, you can use the `merge` command to combine your specific branch into the master branch:
    ```bash
    git merge BRANCH-NAME
    ```


## Resetting Changes

- To reset a single file to its state in the last commit:
    ```bash
    git checkout -- file_name
    ```

## Viewing Differences

- To view the differences between two branches:
    ```bash
    git diff branch1 branch2
    ```

## Remote URL Management

- Get the remote URL of the repository:
    ```bash
    git remote get-url origin
    ```

- Change the remote URL of the repository:
    ```bash
    git remote set-url origin new-url
    ```
