
# coding: utf-8

# #  Monitoring Gmail Inbox

# Many automation solutions make use of the functionality provided by mail services as it serves as an important element that allows for communication between humans and the automation process. There are many benefits provided by using Google Mail (Gmail), one of which is cost - for that reason, we will focus on providing a step-by-step guide of how to monitor emails coming into your Gmail inbox, with the ability to monitor specific lables. 

# ## Import Libraries

# In[ ]:


import imaplib, email


# ## Gather Variable Values

# In[ ]:


imap_url = 'imap.gmail.com'

user = input("Please enter your email address: ")
password = input("Please enter your password: ")
lable = input("Please enter the lable that you'd like to search: ")
search_criteria = input("Please enter the subject search criteria: ")


# ## Define Methods

# In[ ]:


# Retrieves email content
def get_body(message): 
    if message.is_multipart(): 
        return get_body(message.get_payload(0)) 
    else: 
        return message.get_payload(None, True) 
    
# Search mailbox (or lable) for a key value pair
def search(key, value, con):  
    result, data = con.search(None, key, '"{}"'.format(value)) 
    return data 
  
# Retrieve the list of emails that meet the search criteria
def get_emails(result_bytes): 
    messages = [] # all the email data are pushed inside an array 
    for num in result_bytes[0].split(): 
        typ, data = con.fetch(num, '(RFC822)') 
        messages.append(data) 
  
    return messages 

# Authenticate
def authenticate(imap_url, user, password, lable):
    
    # SSL connnection with Gmail 
    con = imaplib.IMAP4_SSL(imap_url)  

    # Authenticate the user through login
    con.login(user, password)  

    # Search for mails under this lable
    con.select(lable)


# ## Authenticate

# In[ ]:


authenticate(imap_url, user, password, lable)


# ## Extract Mails

# In[ ]:


# Retrieve mails
search_results = search('Subject', search_criteria, con)
messages = get_emails(searhc_results) 
  
# Uncomment to view the mail results
#print(messages)


# ## Extract Relevant Information From Results

# In[ ]:


for message in messages[::-1]:  
        
    for content in message: 
                       
        if type(content) is tuple:  
  
            # Encoding set as utf-8 
            decoded_content = str(content[1], 'utf-8')  
            data = str(decoded_content) 
            
            # Extracting the subject from the mail content
            subject = data.split('Subject: ')[1].split('Mime-Version')[0]
                                      
            # Handling errors related to unicodenecode 
            try:  
                indexstart = data.find("ltr") 
                
                data2 = data[indexstart + 5: len(data)] 
                
                indexend = data2.find("</div>") 
                
                # Uncomment to see what the content looks like
                #print(data2[0: indexend]) 
  
            except UnicodeEncodeError as e: 
                pass

