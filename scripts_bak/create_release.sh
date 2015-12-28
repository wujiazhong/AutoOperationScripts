tag_index=$1
release_name=$2
release_msg=$3
ext_name=$4
curl -v "https://api.github.com/repos/ibmpredictiveanalytics/$ext_name/releases?access_token=TOKEN" \
	-X POST \
	-d "{\"tag_name\": \"$tag_index\",\"target_commitish\": \"master\",\"name\": \"$release_name\",\"body\": \"$release_msg\",\"draft\": false,\"prerelease\": false}"
	