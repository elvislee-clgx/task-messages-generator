import os
import sys

# Enter 1.environment 2. pipeline name 3. Absolute path to local repo
env = sys.argv[1].lower()
pipeline_name = sys.argv[2].strip().lower().replace(' ', '-')
local_repo_folder_path = sys.argv[3].strip() + '/idap-kafka-to-scdf-task-launcher'
repo_git_folder = sys.argv[3].strip() + '/.git'

if env == 'dev':
    gcs_config_file_path = "gs://idap-dev-aux-scripts-infrastructure-data/test/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)
    read_file = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-dev-west.yml', 'r')
    write_file = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-dev-west.yml', 'w')

elif env == 'int':
    gcs_config_file_path = "gs://idap-preprod-aux-scripts-infrastructure-data/int/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)
    read_file = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-int-west.yml', 'r')
    write_file = open(local_repo_folder_path + '/idap-kafka-to-scdf-task-launcher-int-west.yml', 'w')

doc_str = read_file.read()
read_file.close()

new_task_message = ('"[{} Full]":\n'.format(pipeline_name.replace('-', ' ').title()) +
                    '      - taskName: sdp-dataflow-job-launcher\n' +
                    '        command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file="'.format(env) + gcs_config_file_path + '/full-job-parameters.yml"\n' +
                    '        memory: 4096\n' +
                    '    "[{} Incremental]":\n'.format(pipeline_name.replace('-', ' ').title()) +
                    '      - taskName: sdp-dataflow-job-launcher\n' +
                    '        command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file="'.format(env) + gcs_config_file_path + '/incremental-job-parameters.yml"\n' +
                    '        memory: 4096\n    ')

insert_position = doc_str.find("\"[AVM snapshot completed FULL]\":")

doc_add_task_message = doc_str[:insert_position] + new_task_message + doc_str[insert_position:]

write_file.write(doc_add_task_message)
write_file.close()

os.system('python3 gitpython-push.py {repo_git_folder} {pipeline_name}'.format(repo_git_folder=repo_git_folder, pipeline_name=pipeline_name))

