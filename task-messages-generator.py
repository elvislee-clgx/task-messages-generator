import os
import sys
import yaml

env = sys.argv[1].lower()
pipeline_name = sys.argv[2].strip().lower().replace(' ', '-')
gcs_config_file_path = ''
if env == 'dev':
    gcs_config_file_path = "\"gs://idap-dev-aux-scripts-infrastructure-data/test/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)
elif env == 'int':
    gcs_config_file_path = "\"gs://idap-preprod-aux-scripts-infrastructure-data/int/enriched/dataflow-bigquery-elastic/config/{pipeline_name}/{env}".format(env=env, pipeline_name=pipeline_name)

new_task_message = ("\"[{} Full]\":\n".format(pipeline_name.replace('-', ' ').title()) +
                    "  - taskName: sdp-dataflow-job-launcher\n" +
                    "    command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file=".format(env)  + gcs_config_file_path + "/full-job-parameters.yml\"\n" +
                    "    memory: 4096\n" +
                    "\"[{} Incremental]\":\n".format(pipeline_name.replace('-', ' ').title()) +
                    "  - taskName: sdp-dataflow-job-launcher\n" +
                    "    command: .java-buildpack/open_jdk_jre/bin/java -Dspring.profiles.active=dataapi-{}-west org.springframework.boot.loader.JarLauncher --gcs-config-file=".format(env)  + gcs_config_file_path + "/incremental-job-parameters.yml\"\n" +
                    "    memory: 4096\n")

print(new_task_message)

message = yaml.safe_load(new_task_message)

with open('message.yml', 'a+') as file:
    yaml.dump(message, file)