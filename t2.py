def format_report(product_name,res_flags,case_ids,case_descs,testers):
    email_list=[]
    title='%s_%s_测试报告'%(product_name,time.strftime('%Y%m%H%M%S'))
    count=len(res_flags)
    pass_count=res_flags.count('pass')
    fail_count=count-pass_count
    content='''
%s:
    您好，本次测试共运行%s条，通过%s条，失败%S条。
    执行信息如下：
    '''%(testers,count.pass_count,fail_count)
    for case_id,case_desc,res_flag in zip(case_ids,case_descs,res_flags):
        msg="['%s','%s','%s']+\n"%(case_id,case_desc,res_flag)
        content+=msg
    for testers in email_dict:
        email_list.append(email_dict[testers])
    print(content)
    print(email_list)
    send_email(email_user,email_pws,email_list,title,content)
