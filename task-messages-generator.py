import os
import sys

env = sys.argv[1].lower()
pipeline_name = sys.argv[2].strip().lower().replace(' ', '-')
gcs_config_file_path = ''
doc_str = ''

if env == 'dev':
    gcs_config_file_path = "gs://idap-dev-aux-scripts-infrastructure-data/test/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)
    read_file = open('idap-kafka-to-scdf-task-launcher-dev-west.yml', 'r')

elif env == 'int':
    gcs_config_file_path = "gs://idap-preprod-aux-scripts-infrastructure-data/int/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)
    read_file = open('idap-kafka-to-scdf-task-launcher-int-west.yml', 'r')

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

if env == 'dev':
    write_file = open('idap-kafka-to-scdf-task-launcher-dev-west2.yml', 'w')
elif env == 'int':
    write_file = open('idap-kafka-to-scdf-task-launcher-int-west2.yml', 'w')

write_file.write(doc_add_task_message)
write_file.close()

