# delete specified tag from local and remote

# --- command line
repo_folder=$1
tag_name=$2
branch_name=$3

cd $repo_folder
# --- pull tag from remote
git pull origin $branch_name --tag
if [ "$?" != 0 ]; then
	echo "Fail to pull tag from remote."
	exit 1
fi

# --- check whether tag exists
res=$(git tag | grep $tag_name)
if [ -z "$res" ]; then
	echo "$tag_name does not exist!"
	exit 1
fi

# --- delete tag from local
git tag -d $tag_name
if [ "$?" != 0 ]; then
	echo "Fail to delete tag from local."
	exit 1
fi

# --- push to remote repo
git push origin $branch_name :refs/tags/$tag_name
if [ "$?" != 0 ]; then
	echo "Fail to push tag to remote."
	exit 1
fi

# --- finished
exit 0
