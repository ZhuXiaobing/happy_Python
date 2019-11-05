#!/bin/bash

# 此文件用来将hdfs上的数据注入mysql.
# 涉及脚本知识
# 1：mysql 命令 -s,-f
# 2：文件转码   -c
# 3：字符串拆分技巧 arr=(${line//\t/ })
# 4: 数组的相关操作  ${#arr[@]}, ${arr[i]}
# 5：字符串截断 total=${num:6}

if [ ! $# == 1 ];then
	echo "Usage: sh $0 20190101"
	exit 0
fi

startDay=$1
host="1.2.3.4"
port="3306"
pw="123456"
user="root"
db="targetdb"
table="targettable"

# -s 静默模式
# -f忽略出现错误的行，强制继续执行
baseSql="mysql -h${host} -u${user} -P${port} -D${db} -s -N -f  "
export MYSQL_PWD=${pw}

while true
do
    hadoop fs -ls hdfs://x.y.z/${startDay}
    ## 没有获取到文件，休息后重试。
	if [ $? != 0 ];then
		sleep 24h
	else
		echo ${startDay}
		hadoop fs -getmerge hdfs://x.y.z/${startDay} ./test.file

        # 此处可能需要对下载下来的文件做转码处理（具体情况，具体分析）
        # -c 忽略转码中不能识别的某些字符
        # cat ./test.file | iconv -f UTF8 -t GBK -c >> target.file

		while read line
		do
		    ## 将读取的文件每行按\t拆分成数组。
			arr=(${line//\t/ })
			## 获取拆分后数组大小
			num=${#arr[@]}
			if [ $num == 5 ];then
			   ## 数组元素赋值
               userid=${arr[0]}
			   tokenId=${arr[2]}
			   # num=$(${baseSql}"select count(*) as count from $table where userid=$userid and token_id=$tokenId;")
			   # 对num 进行截断处理
			   # total=${num:6}
			   # if [ "$total" ==  0 ];then
			   echo "insert into $table (userid,token_id) values ($userid, $tokenId);" >> ./res.sql
               #fi
			fi
		done < ./test.file

		## 批量执行中间结果脚本
		$(${baseSql} < ./res.sql)

		rm ./res.sql
		rm ./test.file

		## 更新startDay 到当前时间的下一天，继续处理。
        startDay=`date -d "$startDay 1 days" +%Y%m%d`
	fi
done
