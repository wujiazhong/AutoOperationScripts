tag_index=$1
ext_name=$2
curl -vi "https://api.github.com/repos/ibmpredictiveanalytics/$ext_name/releases/tags/$tag_index?access_token=TOKEN" \
	 -X GET 