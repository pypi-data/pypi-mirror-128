# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 07:15:17 2021

@author: tommy
"""

#%% libs

import re
import time
import smtplib
import traceback
import pandas as pd
from tabulate import tabulate
from datetime import timedelta
from email.mime.text import MIMEText
from inspect import signature, getfullargspec
from email.mime.multipart import MIMEMultipart

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  

#%% helpers 

def _parse_stack(function):
    stack = traceback.extract_stack()
    #TODO: logic for finding correct lvl, maybe have user pass it, 
    # while fn_name != fn_name_guess
    _, _, _, code = stack[-4] 
    #fn_name_guess = re.search( r"\=?([^\s|=]+)\(", code).group(1)
    fn_name = function.__name__
    return code, fn_name

def _parse_fn_signature(function):
    fn_signature = str(signature(function))
    params = re.findall(r'([^\s|^,|^\(|^\)]+)', fn_signature)
    params = [re.sub(r'=.+', '', f) for f in params]
    
    #TODO: this is same thing?
    argspec = getfullargspec(function)
    params = argspec.args
    
    return params
               
def _log_msg(logger, printf, msg, err_traceback = None):
        
    if logger is not None:
        if err_traceback is None:
            logger.info(msg, stacklevel=5) # for stack frame of org caller
        else:
            logger.error(msg)
            
    if printf:
        print(f"{pd.to_datetime('today').strftime('[%y%m%d %H:%m:%S]')} {msg}")

def _custom_obj_str(obj):
    strg = str(obj)[0:50] if hasattr(obj, '__str__') else None
    if type(obj) == pd.DataFrame:
        strg = f"cols: {', '.join(obj.columns.values)[0:50]}..." 
    return strg

def _len(obj):
    try:
        length = len(obj)
    except:
        length = None
    return length

def _fn_meta(function, args, kwargs, result):
    params = getfullargspec(function).args
    all_args = dict(zip(params[0:len(args)], args))
    all_args.update(kwargs)
    all_args.update({'return': result})
    all_args = pd.DataFrame({'var':all_args.keys(), 'val':all_args.values()})
    all_args['type'] = all_args.val.apply(lambda x: type(x))
    all_args['len'] = all_args.val.apply(_len)
    all_args['str'] = all_args.val.apply(_custom_obj_str)
    all_args = all_args.drop(columns = 'val')    
    return all_args

def _email_inputs(fn_meta, fn_name, latest_error, min_exec_tm,
                  code, start_time, end_time, err_traceback):
    
    status = 'Successfully' if latest_error is None else 'w/ Errors'
    subject = f'TheLogger: {fn_name} Executed {status} ({min_exec_tm})'
    

    if latest_error is not None:
        err_tb = err_traceback.replace('\n', '<br>')
        err_tb = err_tb.replace('Traceback (most recent call last):',
                         '<b>Exception Traceback (most recent call last):</b>')
        err_tb = f'{err_tb}<br>'
        
    else:
        err_tb = ''
        
    body = f"""\
    <html>
      <head></head>
      <body>
        <p><b>Executed:</b> {code}...<br><br>
           <b>Start Time:</b> {start_time}<br>
           <b>End Time:</b> {end_time}<br>
           <b>Elasped Time:</b> {min_exec_tm}<br><br>
           <b>Inputs and Output of <i>{fn_name}</i>:</b>
           {fn_meta.to_html(index = False)}<br>
           {err_tb}
           --<br>
           <b>See The Docs:</b> <a href="https://www.python.org/">TheLogger</a> 
        </p>
      </body>
    </html>
    """
    
    return  subject, body

def _send_email(email, host, fn_meta, fn_name, latest_error, min_exec_tm, code, 
                start_time, end_time, err_traceback):
    
    if email is None:
        return None
    
    subject, body = _email_inputs(fn_meta, fn_name, latest_error, min_exec_tm,
                                  code, start_time, end_time, err_traceback)
    
    emsg = MIMEMultipart()
    if host is None:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls() 
        s.login('py.notify1@gmail.com', 'ytbxunbpmabkvmhn')
        emsg['From'] = 'py.notify1@gmail.com' 
    else:
        s = smtplib.SMTP(host=host)
        emsg['From'] = email        
        
    emsg['To'] = email
    emsg['Subject'] = subject
    emsg.attach(MIMEText(body, 'html'))
    s.send_message(emsg)
    s.quit()

def _format_msg(fn_meta, fn_name, min_exec_tm):
    fn_meta_txt = tabulate(fn_meta, tablefmt="github", numalign = 'left',
                           headers = fn_meta.columns, showindex = False)
    msg = f"Inputs and Output of {fn_name}:\n{fn_meta_txt}"
    msg = f"{msg}\nElapsed Time: {min_exec_tm}"
    return msg

#%% exec_func

def _exec_func(function, email, timeit, logger, printf, notes, error, host, 
               *args, **kwargs):
    
    code, fn_name = _parse_stack(function)
    exec_times, latest_error, err_traceback = [], None, None
    for i in range(1,timeit+1):
        _log_msg(logger, printf, f"Starting: {code}...")
        try:
            t1, start_time = time.perf_counter(), pd.to_datetime('today') 
            result = function(*args, **kwargs)
        except Exception as err:
            latest_error = err
            err_traceback = traceback.format_exc() 
        _log_msg(logger, printf, f"Finished: {code}...")
        exec_times.append(time.perf_counter() - t1)
        end_time = pd.to_datetime('today')
    min_exec_tm = str(timedelta(seconds = min(exec_times))).rstrip('0')
    result = result if latest_error is None else latest_error

    fn_meta = _fn_meta(function, args, kwargs, result)
    _log_msg(logger, printf, _format_msg(fn_meta, fn_name, min_exec_tm))
    _send_email(email, host, fn_meta, fn_name, latest_error, min_exec_tm, code, 
                start_time, end_time, err_traceback)
        
    if latest_error is not None:
        _log_msg(logger, printf, f"Error in {code}...\n{err_traceback}", 
                 err_traceback)
        if error:
            raise latest_error
    
    return result


