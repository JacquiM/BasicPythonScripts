
# coding: utf-8

# # Spinning up a Web API to interface with an existing SQL Server Database
# 
# For more information on how to further customise the creation of the project, please go to:
# https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-new#webapi

# ## Import libraries needed

# In[1]:


from datetime import datetime

import os


# ## Initialise the variables needed

# In[2]:


project_path = r"{}\Projects".format(os.getcwd()) # points to a folder named projects created in the same directory as this script
project_name = "TestScriptWebAPI" # the name of the project (and file that groups the project/solution files together)

start_directory = os.getcwd() # the directory of the script
start_time = datetime.now() # the time that process started


# ## Create the project
# 
# Ensure that the dotnet CLI has been installed: https://dotnet.microsoft.com/download/dotnet-core/thank-you/sdk-3.1.201-windows-x64-installer

# In[3]:


# this method is reusable for all commands (dotnet commands in this project)
# this method first changes the path to the required file path and then executes the command
def ExecuteCommand(command, file_path):
    
    # if the file path exists and is not empty, change to the directory else return False and "File path not valid"
    if file_path != None and os.path.exists(file_path):

        os.chdir(file_path)

    else:

        return False, "File path not valid" # False depicts that the command did not run successfully due to the invalid file path

    command_output = os.popen(command).read() # command is executed

    return True, command_output # True depicts that the command was executed successfully, however, it might not be the desired out put which is why the command_output is also returned


# In[4]:


# this method is used to create the project, the solution and the linkage between the two
def CreateWebAPI(project_name, project_path):
    
    # create the solution path if it doesn't exist yet
    solution_path = r"{}\{}".format(project_path, project_name)
    
    if (os.path.exists(solution_path) == False):
        
        os.mkdir(solution_path)

    # this is the command that will be run in order to create a new project.  Customising the project before creation would occur here
    command = "dotnet.exe new webapi --name {} --force".format(project_name)

    result = ExecuteCommand(command, project_path)[0]
    
    if result:
        
        print("Project successfully created")
        
    else:
        
        print("Project not created")

    # this is the command that will be run in order to create a new sln.  Customising the project before creation would occur here
    command = "dotnet.exe new sln --name {} --force".format(project_name)

    result = ExecuteCommand(command, solution_path)[0]
    
    if result:
        
        print("Solution successfully created")
        
    else:
        
        print("Solution not created")
            
    # this is the command used to add the project to the solution
    csproj_path = r"{0}\{1}\{1}.csproj".format(project_path, project_name)
    command = 'dotnet.exe sln add "{}"'.format(csproj_path)
    solution_path = r"{}\{}".format(project_path, project_name)
    
    result = ExecuteCommand(command, solution_path)[0]
    
    if result:
        
        print("Project successfully added to solution")
        
    else:
        
        print("Project not added to solution")


# In[5]:


CreateWebAPI(project_name, project_path)


# ## Delete the default template content

# In[6]:


# this method deletes the template model and controller files that have been created with the project
def DeleteTemplateFiles(project_path, project_name):

    # delete the template WeatherForecast.cs Model class
    template_model = r"{}\{}\WeatherForecast.cs".format(project_path, project_name)

    if os.path.isfile(template_model):
        os.remove(template_model)

    # delete the template WeatherForecast.cs Controller class
    template_controller = r"{}\{}\Controllers\WeatherForecastController.cs".format(project_path, project_name)

    if os.path.isfile(template_controller):
        os.remove(template_controller)


# In[7]:


DeleteTemplateFiles(project_path, project_name)


# ## Scaffold the database

# In[8]:


# this method compiles the command string from the database connection and tables
def CompileCommandStrings(auth, server, database, tables, username, password):
    
    # the models are created in the Models folder
    # the context is created in the Data folder

    if auth == 'Windows':
        
        connection_string = text = '"ConnectionStrings": \n\t{"DefaultConnection": "Initial Catalog=' + database + ';Data Source=' + server + '; Trusted_Connection=true;"},\n"Logging"'
        command = 'dotnet.exe ef dbcontext scaffold "Initial Catalog={};Data Source={}; Trusted_Connection=true;" Microsoft.EntityFrameworkCore.SqlServer -o Models --context-dir Data'.format(database, server)

    if auth == 'SQL':

        connection_string = text = '"ConnectionStrings": {\n\t"DefaultConnection": "Password=' + password + ';Persist Security Info=True;User ID=' + username + ';Initial Catalog=' + database + ';Data Source=' + server + '"},\n"Logging"'
        command = 'dotnet.exe ef dbcontext scaffold "Password={};Persist Security Info=True;User ID={};Initial Catalog={};Data Source={}" Microsoft.EntityFrameworkCore.SqlServer -o Models --context-dir Data'.format(password, username, database, server)

    if tables != '':

        split_table = []

        tables.replace(' ','')

        if ',' in tables:

            split_table = tables.split(',')

        if ';' in tables:

            split_table = tables.split(';')

        for table in split_table:

            command += ' -t {}'.format(table)

    command += ' -f'
    
    return command, connection_string


# In[9]:


# this method installs the desired packages
def InstallPackages(solution_path):
    
    # Install SqlServer
    command = "dotnet add package Microsoft.EntityFrameworkCore.SqlServer -v 3.1.1"
    command_result = ExecuteCommand(command, solution_path)
    
    # Install EF Design
    command = "dotnet add package Microsoft.EntityFrameworkCore.Design -v 3.1.1"
    command_result = ExecuteCommand(command, solution_path)
    
    # Install EF Tools
    command = "dotnet add package Microsoft.EntityFrameworkCore.Tools -v 3.1.1"
    command_result = ExecuteCommand(command, solution_path)


# In[10]:


# this method is used to scaffold the database into the project
def ScaffoldDatabase(auth, server, database, tables, username, password, project_path):
    
    solution_path = r"{}\{}".format(project_path, project_name)
    
    InstallPackages(solution_path)
    
    result = CompileCommandStrings(auth, server, database, tables, username, password)
    command = result[0]
    connection_string = result[1]
        
    command_result = ExecuteCommand(command, solution_path)
    
    print(command_result)


# In[11]:


ScaffoldDatabase('Windows', 'JACQUELINEMULLE\\LOCAL', 'RPAQA', 'ProjectCreation', None, None, project_path)


# ## Create Controllers

# In[12]:


# this method gets the context class name
def GetContext(file_path):
    
    # the file path should be the path to where the context class was created    
    f = open(file_path, "r")

    context_name = None
    
    for line in f.readlines():

        if '_context' in str(line) and 'private readonly' in str(line):
            
            line = line.replace('  ', '')
            context_name = line.split(' ')[2]
            
    return context_name


# In[13]:


# this method gets the model class and returns the class name, attribute as well as the namespace
def GetModel(file_path):

    # file path should depict the path to the Model folder
    f = open(file_path, "r")

    class_name = None
    attributes = []
    namespace = None

    # for each line in the model class, extract the class name, the attributes and the namespace
    for line in f.readlines():

        if 'namespace' in str(line):

            namespace = line.split(' ')[1].split('.')[0]

        if 'public' in str(line):

            line = line.replace('  ', '')

            split_line = line.split(' ')

            if split_line[2] == 'class':

                class_name = split_line[3].replace('\n','')

            else:

                attributes.append(split_line[2])
                                                
    return class_name, attributes, namespace


# In[14]:


# this method compiles the controller class from the controller template
def CompileControllerTemplate(model, attributes, file_path, template_file_path, namespace, context_name, id):

    file = open(file_path, "w+")

    template_file = open(template_file_path, "r+")

    template = template_file.read()

    template = template.replace('FillNamespace', namespace)
    template = template.replace('FillContext', context_name)
    template = template.replace('FillModel', model)
    template = template.replace('fillModel', model[0].lower() + model[1:])
    template = template.replace('FillId', id)

    file.writelines(template)

    file.close()
    template_file.close()


# In[15]:


# this method creates the controllers
def CreateControllers(solution_path):

    # initialise the model_file_path
    model_file_path = r"{}\Models".format(solution_path)
    
    # for each model found in the model file, get the model info and use it to create the controller
    for file in os.listdir(model_file_path):

        if file != 'ErrorViewModel.cs':

            file_path = "{}\..\Data".format(model_file_path)

            for context in os.listdir(file_path):

                context_name = context.replace('.cs','')

            file_path = '{}\{}'.format(model_file_path, file)

            model_result = GetModel(file_path)

            model = model_result[0]
            attributes = model_result[1]
            id = attributes[0]
            namespace = model_result[2]            
            path = r'{}\Controllers'.format(solution_path)
            file_path = r"{}\{}Controller.cs".format(path, model)
                        
            template_file_path = r"{}\APIControllerTemplate.cs".format(start_directory)

            if os.path.exists(path) == False:

                os.mkdir(path)

            CompileControllerTemplate(model, attributes, file_path, template_file_path, namespace, context_name, id)


# In[16]:


solution_path = r"{}\{}".format(project_path, project_name)

CreateControllers(solution_path)


# In[17]:


# calculate the duration

end_time = datetime.now()

duration = end_time - start_time

print(duration.total_seconds())

