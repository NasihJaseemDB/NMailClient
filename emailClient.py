#Nzy/MailClient

import smtplib
import getpass
from email.message import EmailMessage
import pdb
import os,sys


class send:
    
    def __init__(self):
        self.smtp_object= smtplib.SMTP('smtp.gmail.com',587)
        self.smtp_object.ehlo()
        status=self.smtp_object.starttls()
        print(status)
        self.login()
        self.v='y'
        while(self.v=='y'):
            self.v=self.sender()
        
        self.smtp_object.quit()
    
    def login(self):
        try:
            self.email=getpass.getpass("Enter the gmail: ")
            self.pw=getpass.getpass("Enter the password: ")


        except Exception as e:
            print(f"Invalid field inputs\n{e}")
            sys.exit()
            

        self.smtp_object.login(self.email,self.pw)
    
    def filetype(self,name):
        named=os.path.basename(name)
        exten=named.split('.')[-1]

        if exten == 'jpg' or exten == 'jpeg':
            main_type='image'
            file_type='jpeg'

        elif exten == 'png':
            main_type='image'
            file_type='png'

        elif exten == 'pdf' or exten=='txt' or exten=='log' or exten=='html':
            main_type='application'
            file_type='octet-stream'
    
        return (main_type,file_type,named)

    def sender(self):
        print("\n\nWelcome to NMail Client\n","="*20,"\n")
        #Adding details to message header
        msg=EmailMessage()
        msg['Subject']= input("Enter the subject line: ")
        msg['From']=self.email
        msg['To']=input("Enter the recepient email [seperate by comma]: ").split(',')
        # msg['To']=self.email
        msg.set_content(input("Enter the message: "))
        files=input("If you have attachments [Else press enter]\nEnter the file paths [seperated by comma]: ").split(',')
        
        #Checking the attachments
        counthtml=0
        countfile=0
        self.html=''
        for file in files:
            if 'html' in file:
                counthtml+=1
                
                fc=file

            else:
                countfile+=1

        if files.index(fc) != 0:
            files.remove(fc)
            files.insert(0,fc)

        if len(files):

            print(files)

            for file in files:

                if 'html' in file and counthtml <=1 and countfile >=1:
                    #one attachment and one embedding
                    self.html=file  #To add to iter object in the final segment
                    # files.remove(file)
                elif 'html' in file and counthtml <=1 and countfile ==0:
                    #Embedding attachment on to mail
                    print("\nEmbedding\n")
                    with open(file) as f:
                        file_data=f.read()
                        msg.add_alternative(file_data,subtype='html')
                else:
                    #Add Everything as an attachment
                    print('\nAttaching\n')
                    with open(file,'rb') as f:
                        file_data=f.read()
                        main_type,file_type,file_name=self.filetype(file)
                        

                        try:
                            msg.add_attachment(file_data,maintype=main_type,subtype=file_type,filename=file_name)
                        except Exception as e:
                            print(f'Error Occured!\n{e}')
                            pdb.set_trace()

        if self.html != '':
            with open(self.html) as f:
                file_data=f.read()
            #Add alternative instead of text along with attachments
            iter = list(msg.iter_parts())
            iter[0].add_alternative(file_data, subtype='html')
 
        status=self.smtp_object.send_message(msg)
        if not len(status):
            print('The mail has been sent successfully!')
        else:
            print('Error Occured!',status)

        self.v=input("Do you want to send another email? y/n: ")
        return self.v[0].lower()
        
        
if __name__=="__main__":
    send1=send()