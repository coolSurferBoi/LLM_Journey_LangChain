from utils.OpenAiJourneyUtils import OpenAiJourneyUtils
from utils.HuggingFaceJourneysUtils import HuggingFaceJourneysUtils
class APIJourneyUtils:
    """
    Factory and orchestration utility for image generation backends used in the journey game.
    It lazily initializes and caches image-generation clients per model, providing a unified
    interface for generating images regardless of the underlying provider.
    """

    def __init__(self):
        """
        Initializes the APIJourneyUtils with an empty connection registry.
        Connections to image-generation providers are created on demand
        and cached for reuse across requests.
        """
        self.ImageGen_connections = {}

    def setup_ImageGen_connection(self, model_name):
        """
        Creates and stores an image-generation client for the given model
        if one does not already exist. Selects the appropriate backend
        implementation based on the model name.
        """
        if model_name not in self.ImageGen_connections:
            if model_name == 'dall-e-3':
                connection = OpenAiJourneyUtils()
            elif model_name == 'black-forest-labs/FLUX.1-dev':
                connection = HuggingFaceJourneysUtils(model_name)
            self.ImageGen_connections[model_name] = connection

    def get_ImageGen_connection(self, model_name):
        """
        Retrieves the cached image-generation client for the specified model.
        Assumes the connection has already been initialized via setup_ImageGen_connection.
        """
        return self.ImageGen_connections[model_name]

    def get_img(self, model_name, prompt):
        """
        Generates an image for the given prompt using the specified model.
        Delegates image creation to the appropriate cached backend and
        returns the resulting image URL or static path.
        """
        img_url = self.get_ImageGen_connection(model_name).get_img(model_name, prompt)
        return img_url
