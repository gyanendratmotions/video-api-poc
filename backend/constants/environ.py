import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

ASSEMBLY_API_KEY = os.getenv('ASSEMBLY_API_KEY')
print("hbvhhb",ASSEMBLY_API_KEY)