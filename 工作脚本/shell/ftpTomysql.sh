#!/bin/sh

#脚本知识点
#1：定义公共处理函数
#2：文件下载转码
#3：awk高级使用（不太好注释，直接看代码吧）

# 配置文件统一外部化，推荐方式
. /dbconf.sh


MYSQL="/home/work/local/mysql/bin/mysql"
CONN_DB="${MYSQL} -q -B -N -h${db_host} -P${db_port} -u${db_user} -p${db_passwd} --default-character-set=utf8 -DtargetDB"

DICT_FILE_PATH="ftp://x.y.z"
DICT_FILE_NAME="ftpFile.txt"

TMP_DIR="/tmp/app_import"
mkdir -p "$TMP_DIR"
# 清除目标目录内的所有现有文件
[ -d "$TMP_DIR" ] && rm -rf "$TMP_DIR"/*


# 定义公共的错误处理函数
function exitOnError() {
	if [ $? -ne 0 ]
	then
		echo "error: $1"
		exit 1
	fi
}

# 下载文件到目标目录
# -P 执行下载目录
# -O 指定下载之后的文件名
wget -P "$TMP_DIR/" -O $DICT_FILE_NAME "$DICT_FILE_PATH/$DICT_FILE_NAME"
exitOnError "Downloading dict file failed."

# 文件从GBK转码为UTF8
iconv -f GBK -t UTF8 "$TMP_DIR/$DICT_FILE_NAME" >"$TMP_DIR/$DICT_FILE_NAME.utf8"

# 下载数据库全量数据
$CONN_DB -e "SELECT appid, apppackage, appname, category FROM app;" >"$TMP_DIR/app.dump"
exitOnError "Dumping apps from DB failed."

# 用awk命令对比下载的文件与数据库导出的文件，生成需要更新的sql文件。
awk -F"\t" '
ARGIND==1{
	dbline[$1]=$0
}
ARGIND==2{
	modifyM(2)
	escape_field(2)
	modifyN(3)
	escape_field(3)
	modifyM(4)
	if(!dbline[$1])
		print "INSERT INTO app(appid, apppackage, appname, category, weight) values ("$1", '\''"$2"'\'', '\''"$3"'\'', "$4", 100);"
	else if(dbline[$1]!=$0)
		{
			split(dbline[$1],arr,"\t")
			if (arr[3]!=$3||arr[2]!=$2) {
				print "UPDATE app SET apppackage='\''"$2"'\'', appname='\''"$3"'\'', category="$4", weight=100 WHERE appid="$1";"
			}
		}
	dictexist[$1]=1
}
END{
	for(appid in dbline) if(!dictexist[appid])
		print "DELETE FROM app WHERE appid="appid";"
}

function modifyM(indexM){
	split($indexM,arr,",")
	$indexM=arr[1]
}

function modifyN(indexN){
	split($indexN,arr,"\\\$@")
	$indexN=arr[1]
}

function escape_field(string_ref){
	gsub("\\\\", "\\\\", $string_ref)
	gsub("'\''", "\\'\''", $string_ref)
}
' "$TMP_DIR/app.dump" "$TMP_DIR/$DICT_FILE_NAME.utf8" > "$TMP_DIR/diff.sql.tmp"

cat "$TMP_DIR/diff.sql.tmp" | grep -E "INSERT|UPDATE|DELETE" > "$TMP_DIR/diff.sql"
rm "$TMP_DIR/diff.sql.tmp"

exitOnError "Generating SQL failed."

# Run sql
$CONN_DB -e "source $TMP_DIR/diff.sql"
exitOnError "Running SQL failed."

# Clear temp files
[ -d "$TMP_DIR" ] && rm -rf "$TMP_DIR"

