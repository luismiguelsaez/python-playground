import os
import openai

openai.organization = "org-5j78uhdLbuxeFpiiIK2wdl0G"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

print(models)
