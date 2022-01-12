"""This script is launched regularly by CRON job"""
import requests
import json
import os
import keepvariable.keepvariable_core as kv
import datetime
from credentials import SERVER,SLACK_WEBHOOK_URL


os.chdir(".")

response=requests.get("http://"+SERVER+"/api/users",verify=True)
if response.ok:
    output=json.loads(response.text)
 
try:
    previous_number_of_users=kv.load_variable()
except FileNotFoundError:   
    previous_number_of_users=0
    

number_of_users=len(output)

refresh_hour=datetime.datetime.now().hour
if refresh_hour==9:
    refresh_time=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
    text=refresh_time+" - Forloop.ai bot health: 100%"
    data="{'text':'"+text+"'}"    
    requests.post(SLACK_WEBHOOK_URL,data=data) #customer-processes-monitoring

if previous_number_of_users<number_of_users:

    
    number_of_newly_registered_users=number_of_users-previous_number_of_users
    for i in range(number_of_newly_registered_users):
        
        last_user_email=output[-1-i]["email"]
        last_user_email_ciphered=last_user_email[0]+(len(last_user_email.split("@")[0])-1)*"*"+"@"+last_user_email.split("@")[1]
        
        print(last_user_email_ciphered)
        print(len(output))
        
        """SLACK NOTIFICATION"""
        
        try:
            
            
            refresh_time=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            text=refresh_time+" - A new user registered at Forloop.ai platform: "+last_user_email_ciphered
            data="{'text':'"+text+"'}"
            
            requests.post(SLACK_WEBHOOK_URL,data=data) #customer-processes-monitoring
        
        except:
            print("Slack notification wasnt created")
    """SLACK NOTIFICATION"""   
    try:
        
        
        refresh_time=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        text=refresh_time+" - Total registered users: "+str(len(output))
        data="{'text':'"+text+"'}"
        
        requests.post(SLACK_WEBHOOK_URL,data=data) #customer-processes-monitoring
    
    except:
        print("Slack notification wasnt created")        
    
else:
    print(f"No new user previously: {previous_number_of_users}, now: {number_of_users}")

previous_number_of_users=number_of_users
previous_number_of_users=kv.Var(previous_number_of_users)

kv.save_variables(kv.kept_variables)
