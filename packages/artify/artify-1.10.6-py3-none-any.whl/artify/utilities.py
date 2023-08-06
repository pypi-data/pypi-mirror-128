import __main__
from artify import change_version

def get_current_application_version(path):
    projectfile = ''
    if __main__.os.path.exists(__main__.os.path.join(path,'build.gradle')):
        __main__.arch_type = 'gradle'
        filepath = __main__.os.path.join(path,'build.gradle')
        return change_version.get_version(filepath, 'standard')
        
    if __main__.os.path.exists(__main__.os.path.join(path, 'app', 'build.gradle')):
        __main__.arch_type = 'gradle'
        filepath = __main__.os.path.join(path, 'app', 'build.gradle')
        return change_version.get_version(filepath, 'standard')
        
    if __main__.os.path.exists(__main__.os.path.join(path,'package.json')):
        __main__.arch_type = 'npm'
        filepath = __main__.os.path.join(__main__.path, 'package.json')
        return change_version.get_version(filepath, 'standard')

    if __main__.os.path.exists(__main__.os.path.join(path,'pom.xml')):
        __main__.arch_type = 'maven'
        filepath = __main__.os.path.join(path,'pom.xml')
        return change_version.get_version(filepath, 'standard')

    if __main__.os.path.exists(__main__.os.path.join(path,'pubspec.yaml')):
        __main__.arch_type = 'flutter'
        filepath = __main__.os.path.join(path,'pubspec.yaml')
        return change_version.get_version(filepath, 'standard')
    
    if __main__.os.path.exists(__main__.os.path.join(path, 'setup.py')):
        __main__.arch_type = 'other'
        filepath = __main__.os.path.join(path, 'setup.py')
        return change_version.get_version(filepath, 'custom')
            
    if __main__.os.path.exists(__main__.os.path.join(path, 'config/app.php')):
        __main__.arch_type = 'other'
        filepath = __main__.os.path.join(path, 'config/app.php')
        return change_version.get_version(filepath, 'custom')
            
    if __main__.os.path.exists(__main__.os.path.join(path, 'config/app_config.php')):
        __main__.arch_type = 'other'
        filepath = __main__.os.path.join(path, 'config/app.php_config')
        return change_version.get_version(filepath, 'custom')
    
    file_list = change_version.glob('*.sln')
    if (len(file_list)) == 1: #-solution_name
        __main__.arch_type = 'dotnet'
        if (__main__.debug == 1):
            print("DEBUG: Solution file found:: ",file_list)
        flnme, extn = file_list[0].split('.')
        #project name
        if __main__.project_name != '':
            projectfile = [__main__.os.path.join(__main__.project_name,__main__.project_name+'.csproj')]
        else:
            projectfile = change_version.glob(__main__.os.path.join(flnme,'*.csproj'))
        
        if __main__.debug == 1:
            print("DEBUG: Project file found:: ", projectfile)

        if len(projectfile) == 1:
            filepath = __main__.os.path.join(path, projectfile[0])
            return change_version.get_version(filepath, 'custom')
        
    file_list_proj = change_version.glob('*.csproj')
    if (len(file_list_proj)) == 1: #-project_name
        __main__.arch_type = 'dotnet'
        if (__main__.debug == 1):
            print("DEBUG: Project file found:: ",file_list_proj)
           
        if __main__.project_name != '':
            projfile = [__main__.project_name + '.csproj']
        else:
            projfile = file_list_proj

        if len(projfile) == 1:
            filepath = __main__.os.path.join(path, projfile[0])
            return change_version.get_version(filepath, 'custom')
            
    # To-do Extract version number for .NET type project
    return None
