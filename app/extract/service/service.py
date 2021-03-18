"""
    Service Layer for book detail extraction.
"""
import requests
import os
import pickle
from google.cloud import pubsub_v1

class GetBookData:
    """
    Class for the service layer.
    """

    @staticmethod
    def fetch_json(q_value):
        """Method to fetch data from mentioned endpoint and build required output.

        Args:
            q_value (string): q value to pass as query parameter to mentioned API.

        Returns:
            Dict: contains output to be returned from flask endpoint.
        """
        resp = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": q_value})
        recieved_json = resp.json()
        output_dict = {"input": q_value, "output": []}
        for i in recieved_json["items"]:
            book_info = {"title": None, "author": None, "description": None}
            if "title" in i["volumeInfo"]:
                book_info["title"] = i["volumeInfo"]["title"]
            if "author" in i["volumeInfo"]:
                book_info["author"] = i["volumeInfo"]["author"]
            if "description" in i["volumeInfo"]:
                book_info["description"] = i["volumeInfo"]["description"]
            output_dict["output"].append(book_info)

        os.system('python gsc_sub.py')
        os.system('python datastore_sub.py')
        os.system('python bigquery_sub.py')
        PublishMessages.publish_messages(os.getenv('PROJECT_ID'), os.getenv('PUBSUB_TOPIC_BigQuery'), output_dict)
        PublishMessages.publish_messages(os.getenv('PROJECT_ID'), os.getenv('PUBSUB_TOPIC_Datastore'), output_dict)
        PublishMessages.publish_messages(os.getenv('PROJECT_ID'), os.getenv('PUBSUB_TOPIC_GCS'), output_dict)
        return output_dict


class PublishMessages:

    @staticmethod
    def publish_messages(project_id, topic_id, data):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)

        # Data must be a bytestring
        data = pickle.dumps(data).encode('base64', 'strict')
        # color = pickle.loads(b64_color.decode('base64', 'strict'))
        data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())

        print(f"Published messages to {topic_path}.")
