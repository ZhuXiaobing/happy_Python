#!/bin/bash

#脚本知识点
# 启动脚本参数的处理（个数校验，参数值校验）
# 函数参数个数判断， $#, 函数参数获取 $N
# 字符串是否是数字校验：
#
# if grep '^[[:digit:]]*$' <<< $planidTmp;then
#	constructSql $puserid $planidTmp
# fi


# 校验输入参数
if [ ! $# == 1 ];then
	echo "Usage: sh $0 <dbconf|dbconf_dev> &"
	exit 0
else
	if [ $1 == "dbconf" -o $1 == "dbconf_dev" ];then
	    # 加载数据库配置
		. ./$1.sh
	else
		echo "Usage: sh $0 <dbconf|dbconf_dev> &"
		exit 0
	fi
fi


baseSql="mysql -h${host} -u${user} -P${port} -D${db} -e  "
export MYSQL_PWD=${pw}

ftpPath="ftp://x/y/"
ftpFile="ftpfile.txt"


# 自定义函数
function constructSql(){
	if [ $# == 2 ];then
		numofplaninfo=$(${baseSql}"select count(*) as count from planinfo where userid=$1 and planid=$2 and isdel=0;")
		totalofplaninfo=${numofplaninfo:6}
		if [ $totalofplaninfo != 0 ];then
			numofrta=$(${baseSql}"select count(*) as count from plansetting where userid=$1 and planid=$2 and stype=10;")
			totalofrta=${numofrta:6}
			if [ $totalofrta == 0 ];then
				insertTime=`date +"%Y-%m-%d %H:%M:%S"`
     			echo "insert into plansetting (planid,userid,stype,content,addtime,modtime) values ($2,$1,10,\"1\",\"$insertTime\",\"$insertTime\");" >> ./plansetting.sql
			fi
		else
			echo "total ==========="$total
		fi
	fi
}


while true
do
	wget $ftpPath$ftpFile -O ftp.txt

	if [ $? != 0 ];then
		sleep 2h
	else
		while read line
		do
			arr=(${line//\t/ })
			num=${#arr[@]}
			if [ $num == 2 ];then
               puserid=${arr[0]}
			   pplanid=${arr[1]}
			   if [ $pplanid == 0 ];then
				   	${baseSql} "select planid from planinfo where userid=$puserid and isdel=0;"  >> ./planid.tmp
                    while read planidTmp
					do
					    # 参数是否是数字校验
						if grep '^[[:digit:]]*$' <<< $planidTmp;then
							constructSql $puserid $planidTmp
						fi
					done <./planid.tmp
					rm ./planid.tmp
			   else
			        # 注意函数传参的方式（函数名 + 参数列表）
			   		constructSql $puserid $pplanid
		   	   fi
			fi
		done < ./ftp.txt

        if [ -f ./plansetting.sql ];then
		    $(${baseSql} < ./plansetting.sql)  >> /dev/null 2>&1
			rm  ./plansetting.sql
	    fi

		rm ./ftp.txt
        sleep 2h
		exit
	fi
done
