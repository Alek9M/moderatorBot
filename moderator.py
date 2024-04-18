# Imports the Google Cloud client library
from google.cloud import language_v1

# Instantiates a client
client = language_v1.LanguageServiceClient()


class Moderator:

    @staticmethod
    def is_harmful(text: str) -> str | None:
        document = language_v1.types.Document(content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT)
        categories = client.moderate_text(request={"document": document}).moderation_categories
        outstanding = ""
        for judgment in categories:
            if judgment.confidence >= 0.15:
                outstanding += judgment.name + ":" + str(judgment.confidence)

        if len(outstanding) > 0:
            return outstanding
        else:
            return None

