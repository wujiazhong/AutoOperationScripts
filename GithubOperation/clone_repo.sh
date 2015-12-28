# clone repository from Github

# --- command line
save_folder=$1
owner=$2
repo_name=$3

# --- Permission check
chmod u+w "$save_folder"
if [ ! -w "$save_folder" ]; then
	echo "Need write permission in $save_folder!" >&2
	exit 1
fi

# --- clone repo from Github
cd $save_folder
git clone git@github.com:$owner/$repo_name.git
if [ "$?" != "0" ]; then
	echo "Fail to clone '$repo_name'! Please check whether owner and repo exist." >&2
	exit 1
fi

# --- finished
exit 0