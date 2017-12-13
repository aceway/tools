#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: settings.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年01月01日 星期二 16时31分10秒
#########################################################
g_debug = True # False #
g_check_times=2
g_check_timeout=2
g_ip_http_svr="http://members.3322.org/dyndns/getip"
g_ip_file="/tmp/.WAN_IP_ADDR"
g_port=19806
g_url = "http://www.xxxx.com/submit/"
g_token="6cbe1908f69add6a7871c69305f22f5a"

g_notify_to_emails="iuway@qq.com,upython@qq.com"
g_from_email=""
g_from_email_pwd=""
g_smtp_server=""
g_smtp_port=465


def submmit_info(the_url=None, params={}):
    import urllib.urlencode
    import urllib.request
    result = {'code':-1, 'desc': __name__ + ':post_to_auth_server. ', 'data':None,}
    try:
        if the_url is None or not isinstance(params, dict):
            result['code'] = -1
            result['desc'] += "Function parameters error, to API desc."
            result['data'] = None
        else:
            for (k, v) in params.items():
                if isinstance(v, unicode):
                    params[k] = v.encode('utf-8')
            params = urllib.urlencode(params)
            urlfile= urllib.request.urlopen(the_url, params)
            result = urlfile.read()
    except Exception as e:
        result['code'] = -1
        result['desc'] += e.message
        result['data'] = None
    if g_debug:
        print (result)
    return result
    

def send_str_to_email(the_subject, str_message, to_emails, from_email, from_email_pwd, smtp_server, smtp_port=None):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(str_message)
    msg['Subject'] = the_subject
    msg['From'] = from_email
    msg['To'] = to_emails
    if isinstance(smtp_port, int) and smtp_port and smtp_port != 465:
        s = smtplib.SMTP(smtp_server, smtp_port)
    else:
        s = smtplib.SMTP_SSL(smtp_server, 0)
    s.set_debuglevel(1)
    s.docmd('EHLO', from_email)
    s.login(g_from_email, from_email_pwd)
    s.sendmail(from_email, to_emails.split(','), msg.as_string())
    s.quit()
    if g_debug: print ("send message [", str_message, "] to mails:",  to_emails)

def send_file_to_email(the_subject, the_file, to_emails, from_email, from_email_pwd, smtp_server, smtp_port=None):
    import smtplib
    from email.mime.text import MIMEText
    with open(the_file, 'r') as fp:
        msg = MIMEText(fp.read())
    msg['Subject'] = the_subject
    msg['From'] = from_email
    msg['To'] = to_emails
    if smtp_port is not None:
        s = smtplib.SMTP(smtp_server)
    else:
        s = smtplib.SMTP_SSL(smtp_server, smtp_port)
    s.docmd('EHLO', from_email)
    s.login(g_from_email, from_email_pwd)
    s.sendmail(from_email, to_emails.split(','), msg.as_string())
    s.quit()
    if g_debug: print ("send file [", the_file, "] to mails:",  to_emails)

def notify_wan_ip_with_httpsvr(http_server="http://members.3322.org/dyndns/getip", tmp_ip_file="/tmp/.WAN_IP_ADDR"):
    import urllib.request
    import os
    ipInfo = urllib.request.urlopen(http_server)
    new_ip = "{ip}".format(ip=ipInfo.read().strip())
    str_msg = "New ip {ip}\n".format(ip=str(new_ip))
    if os.path.exists(tmp_ip_file):
        with open(tmp_ip_file, 'r') as fp:
            old_ip = "{ip}".format(ip=fp.read().strip())
        if g_debug: print ("OLD  IP:", old_ip, "\nNEW  IP:", new_ip)
        if old_ip == new_ip:
            if g_debug: print ("SAME IP, HAVE NOT BEEN CHANGED, DO NOTHING.")
        else:
            if g_debug: print ("THE IP HAVE BEEN CHANGED, RESET IP FILE, NOTIFY TO:", g_notify_to_emails)
            with open(tmp_ip_file, 'w') as fp:
                fp.write(str(new_ip))
            send_str_to_email("THE NEW IP", str_msg, g_notify_to_emails, g_from_email, g_from_email_pwd, g_smtp_server, g_smtp_port)
    else:
        with open (tmp_ip_file, 'w') as fp:
            fp.write(str(new_ip))
            if g_debug: print ("no old ip, new ip:", new_ip)
            if g_debug: print ("Get the IP first time, notify to:", g_notify_to_emails)
        send_str_to_email("THE NEW IP", str_msg, g_notify_to_emails, g_from_email, g_from_email_pwd, g_smtp_server, g_smtp_port)
    ipInfo.close()

  
def ping(ip,count=2,timeout=5):  
    import os  
    try: 
        cmd = "ping %s -c %d -W %d > /dev/null 2>&1" %(ip, count, timeout)
        if g_debug: print (cmd)
        status = os.system(cmd)
        if status == 0 :  
            if g_debug: print ("ALIVE IP:", ip)
            return True
        else:  
            if g_debug: print ("DEAD IP:", ip)
            return False
    except Exception as e:  
        if g_debug: print ("ERROR:%s" %e)
        return False  

def check_file_ip_alive(the_ip_file, count=2, timeout=5):
    import os
    if os.path.exists(the_ip_file):
        with open(the_ip_file) as fp:
            ip = fp.read()
            return ping(ip.strip(), count, timeout)
        return False
    else:
        return False
    
def main():
    if check_file_ip_alive(g_ip_file, g_check_times, g_check_timeout):
        pass
    else:
        notify_wan_ip_with_httpsvr(http_server=g_ip_http_svr, tmp_ip_file=g_ip_file)

if __name__ == '__main__':
    main()
