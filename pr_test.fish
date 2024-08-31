#!/usr/bin/env fish

# Ensure GITHUB_TOKEN is set
if test -z "$GITHUB_TOKEN"
    echo "Error: GITHUB_TOKEN is not set."
    exit 1
end

# Set up variables
set REPO "seanchatmangpt/hello"
set LOCAL_REPO "hello"
set FEATURE_BRANCH "feature-branch"
set BASE_BRANCH "main"

# Clean up any previous clone
if test -d $LOCAL_REPO
    rm -rf $LOCAL_REPO
end

# Clone the repository
git clone https://github.com/$REPO.git

# Navigate to the repo directory
cd $LOCAL_REPO

# Initialize the repository and push the base branch
echo "Initializing repository..."
touch README.md
git add README.md
git commit -m "Initial commit"
git branch -M $BASE_BRANCH
git push -u origin $BASE_BRANCH

# Create and push the feature branch
git checkout -b $FEATURE_BRANCH
git push -u origin $FEATURE_BRANCH

# Create a new pull request
sungen pr create -t "Test PR" -b "This is a test pull request created by the sungen CLI" -h $FEATURE_BRANCH -r $REPO

# List open pull requests
sungen pr list -r $REPO

# Assuming PR #1 exists, run the following commands
set PR_NUMBER 1

# Merge PR #1
sungen pr merge -n $PR_NUMBER -m "merge" -r $REPO

# Close PR #1
sungen pr close -n $PR_NUMBER -r $REPO

# Comment on PR #1
sungen pr comment -n $PR_NUMBER -b "This is a comment added by the sungen CLI" -r $REPO

# Update the title of PR #1
sungen pr update -n $PR_NUMBER -t "Updated PR Title" -r $REPO

# Assign PR #1 to the user
sungen pr assign -n $PR_NUMBER -a "seanchatmangpt" -r $REPO

# Add labels to PR #1
sungen pr labels -n $PR_NUMBER --add "bug" --add "enhancement" -r $REPO

# Remove a label from PR #1
sungen pr labels -n $PR_NUMBER --remove "bug" -r $REPO

# Cleanup
cd ..
rm -rf $LOCAL_REPO
