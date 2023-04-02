from dotenv import dotenv_values, find_dotenv

class DotEnvHelper:
    BOT_TOKEN_FIELD:str = 'BOT_TOKEN'
    
    def __init__(self):
        self.dotenv_data = dotenv_values(find_dotenv())
        
    def get_value(self, key: str):      
        return self.dotenv_data.get(key)
    
