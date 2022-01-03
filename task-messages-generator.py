import os
import sys

env = sys.argv[1].lower()
pipeline_name = sys.argv[2].strip().upper().replace('-', ' ')

print(env, pipeline_name)