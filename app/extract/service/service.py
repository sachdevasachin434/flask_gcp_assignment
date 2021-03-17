"""
    Service Layer for book detail extraction.
"""
import requests

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
        return output_dict