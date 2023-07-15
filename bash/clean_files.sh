#!/usr/bin/env bash
#set -t 

function clean_files()
{
    local delete_files_dir=$1
    local keep_file_seconds=$2
    if [ -d $delete_files_dir ] && [ -x ${delete_files_dir} ] && [ -r ${delete_files_dir} ] && [ -w ${delete_files_dir} ];then
        cd ${delete_files_dir}
        if [ $? -ne 0 ];then
            echo -e "cd ${delete_files_dir} failed with code:$?"
        else
            now=`date "+%s"`
            read_now=`date +"%Y-%m-%d %H:%M:%S"`
            for f in $(ls -t $(pwd))
            do
                local lf=${f}
                if [ -d "${lf}" ] || [ -f "${lf}" ]; then
                    echo
                else
                    echo "${read_now}: $(pwd) ${lf} not exists!!!"
                    continue
                fi

                #echo -e "In pwd:$(pwd), now file: ${lf}" 
                mt=`stat ${lf} -c "%Y"`
                seconds=`expr ${now} - ${mt}`
                if [ ${seconds} -ge ${keep_file_seconds} ];then
                    if [ -d "${lf}" ] && [ ! -L "${lf}" ] && [ "${lf}" != "." ] && [ "${lf}" != ".." ] && [ -r "${lf}" ] && [ -w "${lf}" ] && [ -x "${lf}" ];then
                        rmdir ${lf} > /dev/null
                        if [ $? -eq 0 ];then
                            # removed empty dir.
                            echo -e "${read_now}: rm emtpy dir:${lf}"
                        else
                            # remove dir failed, treat it as dir with content.
                            #pushd "$(pwd)" 1
                            pushd "$(pwd)"  > /dev/null
                            clean_files ${lf} ${keep_file_seconds}
                            #popd 1
                            popd  > /dev/null
                            rmdir "${lf}"  > /dev/null # maybe failed(not empty), maybe succeed, just ignore error msg
                        fi
                    elif [ -f "${lf}" ] && [ -r "${lf}" ] && [ -w "${lf}" ];then
                        if [ "${lf}" == "clean_log.sh" ]; then
                            echo -e "${read_now}: You should not rm youself(bash script):${lf}"
                        else
                            echo -e "${read_now}: rm file:${lf}"
                            rm -f ${lf}
                        fi
                    else
                        if [ "${lf}" != "." ] && [ "${lf}" != ".." ];then
                            echo -e "${read_now}: You have no right to rm: ${lf}"
                        else
                            echo -e "${read_now}: Escape:${lf}"
                        fi
                    fi
                else
                    echo "${read_now}: The new file/dir will not be rm:${lf}"
                fi
            done
        fi
    elif [ -f "${delete_files_dir}" ] && [ -r "${delete_files_dir}" ] && [ -w "${delete_files_dir}" ];then
        if [ "${delete_files_dir}" == "clean_log.sh" ]; then
            echo -e "${read_now}: You should not rm youself(bash script):${delete_files_dir}"
        else
            echo -e "${read_now}: rm file:${delete_files_dir}"
            rm -f ${delete_files_dir}
        fi
    else
        :
    fi
}

#保留日志的天数
if [ $# -ne 2 ]; then
    name=`basename $0`
    echo -e "USAGE:\n\t${name} delete_files_dir keep_files_days"
    echo -e "\nRemove files and subdirs in the delete_files_dir with keep_files_days, just rm old files and subdirs."
    exit 1
fi

delete_files_dir=$1
keep_files_days=$2

expr match "${keep_files_days}" "[0-9]*$" > /dev/null
if [ $? -ne 0 ]; then
    echo -e "The keep_files_days must be integer number!"
    exit 1
else
    keep_files_days=`expr $keep_files_days`
    if [ ${keep_files_days} -gt 0 ];then
        let "keep_file_seconds=$keep_files_days*24*3600"
        clean_files ${delete_files_dir} ${keep_file_seconds}
        exit 0
    else
        echo "At least keep file one day."
        exit 1
    fi
fi
