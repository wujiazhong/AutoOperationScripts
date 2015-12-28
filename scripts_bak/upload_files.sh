tar_file=$1
release_id=$2
file_name=$3
ext_name=$4
curl -v "https://uploads.github.com/repos/ibmpredictiveanalytics/$ext_name/releases/$release_id/assets?name=$file_name&access_token=TOKEN" \
	-X POST \
	-H "Content-Type:application/spe" \
	-T "$tar_file"