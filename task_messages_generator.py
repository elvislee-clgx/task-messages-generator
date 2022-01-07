import os
import sys
from gitpython_push import git_push

def generate_task_message(env, pipeline_name, repo_path, username, password):
    env = env.lower()
    pipeline_folder_name = pipeline_name.strip().lower().replace(' ', '-')
    pipeline_title = pipeline_name.replace('-', ' ').title()
    local_repo_folder_path = repo_path.strip() + '/idap-kafka-to-scdf-task-launcher'
    repo_git_folder = repo_path.strip() + '/.git'

    if env == 'dev':
        gcs_config_file_path = "gs://idap-dev-aux-scripts-infrastructure-data/test/enriched/dataflow-bigquery-elastic/config/{pipeline_folder_name}/{env}".format(env=env, pipeline_folder_name=pipeline_folder_name)
        file_object = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-dev-west.yml', 'r+')
        pcf_url = 'api.sys.pcfusw1dev.solutions.corelogic.com'
        pcf_org = 'Idap_data_api_us-dev'
    elif env == 'int':
        gcs_config_file_path = "gs://idap-preprod-aux-scripts-infrastructure-data/int/enriched/dataflow-bigquery-elastic/config/{pipeline_folder_name}/{env}".format(env=env, pipeline_folder_name=pipeline_folder_name)
        file_object = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-int-west.yml', 'r+')
        pcf_url = 'api.sys.pcfusw1stg.solutions.corelogic.com'
        pcf_org = 'Idap_data_api_us-int'

    doc_str = file_object.read()

    new_task_message = ('"[{} Full]":\n'.format(pipeline_title) +
                        '      - taskName: sdp-dataflow-job-launcher\n' +
                        '        command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file="'.format(env) + gcs_config_file_path + '/full-job-parameters.yml"\n' +
                        '        memory: 4096\n' +
                        '    "[{} Incremental]":\n'.format(pipeline_title) +
                        '      - taskName: sdp-dataflow-job-launcher\n' +
                        '        command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file="'.format(env) + gcs_config_file_path + '/incremental-job-parameters.yml"\n' +
                        '        memory: 4096\n    ')

    if doc_str.find(pipeline_title) != -1:
        file_object.close()
        raise ValueError("This pipeline task message is already in the .yml file")

    insert_position = doc_str.find("\"[AVM snapshot completed FULL]\":")
    if insert_position == -1:
        file_object.close()
        raise ValueError("The insert position cannot be found")

    doc_add_task_message = doc_str[:insert_position] + new_task_message + doc_str[insert_position:]
    file_object.seek(0)
    file_object.write(doc_add_task_message)
    file_object.close()
    git_push(repo_git_folder, env, pipeline_title)

    os.system('cf login -a {pcf_url} -u {username} -p {password} -o {pcf_org} -s Dataloading'.format(pcf_url=pcf_url, username=username, password=password, pcf_org=pcf_org))
    os.system('cf restart idap-kafka-to-scdf-task-launcher')

# Parameters: 1.environment (dev or int) 2. pipeline name 3. the absolute path to local repo 4. PCF username 5. PCF password
generate_task_message('', '', '', '', '')
