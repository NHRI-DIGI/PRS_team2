Input_dir='/staging2/reserve/flagship/u3121714/kenny/Input/BaseData/hg38/HBOC_110/convert_vcf/'
filename='HBOC_base.list'

## Check for dir, if not found create it using the mkdir ##
score_dir='/staging2/reserve/flagship/u3121714/kenny/Input/BaseData/hg38/HBOC_110/score_vcf/'
[ ! -d "$score_dir" ] && mkdir -p "$score_dir"

mkdir ${score_dir}process
cd ${score_dir}process

while IFS='' read -r line || [[ -n "$line" ]]; do
	# Check file exist or not
        echo "==> $line"
        echo -e "`ls ${Input_dir} | grep ${line}`"
  # remove header
  sed '/^##/d' "${Input_dir}${line}".vcf > "${line}"_no_header.vcf
  # filter chr, pos, ref, alt, sample
  awk '{print$1"\t"$2"\t"$4"\t"$5"\t"$10}' "${line}"_no_header.vcf > "${line}"_no_header_filter.vcf
  # extract header
  awk 'NR==1{print$1"\t"$2"\t"$3"\t"$4"\t"$5}' "${line}"_no_header_filter.vcf > "${line}"_filter_header.txt
  # remove # from header
  sed -e 's/^#//' -i "${line}"_filter_header.txt
  # filter sample column and extract before :
  awk 'NR!=1' "${line}"_no_header_filter.vcf | cut -f 1 -d : > "${line}"_no_header_filter_sample.vcf
  # combine header and filter vcf
  cat "${line}"_filter_header.txt "${line}"_no_header_filter_sample.vcf > "${score_dir}${line}"_complete.vcf
done < ${Input_dir}${filename}

mv ${score_dir}process ../../log
