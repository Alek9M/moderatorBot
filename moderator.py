# Imports the Google Cloud client library
import logging

from google.cloud import language_v1

# Instantiates a client
client = language_v1.LanguageServiceClient()


class Moderator:

    @staticmethod
    def is_harmful(text: str) -> str | None:
        logging.warning("Moderator: " + len(text).__str__())
        document = language_v1.types.Document(content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT)
        categories = client.moderate_text(request={"document": document}).moderation_categories
        outstanding = ""
        for judgment in categories:
            if judgment.name  != "Finance" and judgment.name != "Legal" and judgment.name != "Politics" and judgment.name != "Health" and judgment.name != "Illicit Drugs" and judgment.name != "Religion & Belief" and judgment.name != "Sexual":
                if judgment.confidence >= 0.35:
                    outstanding += judgment.name + ":" + "{:.0f}%".format(judgment.confidence * 100) + "\n"

        if len(outstanding) > 0:
            return outstanding
        else:
            return None

