from utils.OpenAiJourneyUtils import OpenAiJourneyUtils
from utils.HuggingFaceJourneysUtils import HuggingFaceJourneysUtils
class APIJourneyUtils:
    def __init__(self):
        self.ImageGen_connections = {}

    def setup_ImageGen_connection(self, model_name):
        if model_name not in self.ImageGen_connections:
            if model_name == 'dall-e-3':
                connection = OpenAiJourneyUtils()
            elif model_name == 'black-forest-labs/FLUX.1-dev':
                connection = HuggingFaceJourneysUtils(model_name)
            self.ImageGen_connections[model_name] = connection

    def get_ImageGen_connection(self,model_name):
        return self.ImageGen_connections[model_name]

    def get_img(self, model_name, prompt):
        img_url = self.get_ImageGen_connection(model_name).get_img(model_name, prompt)
        return img_url
        