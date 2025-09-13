import requests
import json
from typing import Dict, Any, Optional


class PollyClient:
    """
    Client for the Polly API to interact with polls and votes.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the Polly API client.

        Args:
            base_url: The base URL of the Polly API. Defaults to http://localhost:8000.
        """
        self.base_url = base_url
        self.token = None

    def set_token(self, token: str) -> None:
        """
        Set the authentication token for API requests.

        Args:
            token: The JWT token received after login.
        """
        self.token = token

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Log in to the Polly API and set the authentication token.

        Args:
            username: The user's username.
            password: The user's password.

        Returns:
            Dict containing the access token and token type.

        Raises:
            requests.exceptions.HTTPError: If login fails.
        """
        url = f"{self.base_url}/login"
        response = requests.post(
            url,
            data={"username": username, "password": password}
        )
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses

        token_data = response.json()
        self.set_token(token_data["access_token"])
        return token_data

    def vote_on_poll(self, poll_id: int, option_id: int) -> Dict[str, Any]:
        """
        Cast a vote on an existing poll.

        Args:
            poll_id: The ID of the poll to vote on.
            option_id: The ID of the selected option.

        Returns:
            Dict containing the vote information including id, user_id, option_id, and created_at.

        Raises:
            ValueError: If no authentication token is set.
            requests.exceptions.HTTPError: If the request fails.
        """
        if not self.token:
            raise ValueError("Authentication token is required. Please login first.")

        url = f"{self.base_url}/polls/{poll_id}/vote"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {"option_id": option_id}

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses

        return response.json()

    def get_polls(self, skip: int = 0, limit: int = 10) -> list:
        """
        Get a list of polls.

        Args:
            skip: Number of items to skip.
            limit: Maximum number of items to return.

        Returns:
            List of polls.
        """
        url = f"{self.base_url}/polls"
        params = {"skip": skip, "limit": limit}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_poll(self, poll_id: int) -> Dict[str, Any]:
        """
        Get a specific poll by ID.

        Args:
            poll_id: The ID of the poll to retrieve.

        Returns:
            Dict containing the poll information.

        Raises:
            requests.exceptions.HTTPError: If the poll is not found.
        """
        url = f"{self.base_url}/polls/{poll_id}"

        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    def get_poll_results(self, poll_id: int) -> Dict[str, Any]:
        """
        Get the results of a specific poll.

        Args:
            poll_id: The ID of the poll to get results for.

        Returns:
            Dict containing the poll results with vote counts for each option.

        Raises:
            requests.exceptions.HTTPError: If the poll is not found.
        """
        url = f"{self.base_url}/polls/{poll_id}/results"

        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    def create_poll(self, question: str, options: list) -> Dict[str, Any]:
        """
        Create a new poll.

        Args:
            question: The poll question.
            options: List of option texts.

        Returns:
            Dict containing the created poll information.

        Raises:
            ValueError: If no authentication token is set.
            requests.exceptions.HTTPError: If the request fails.
        """
        if not self.token:
            raise ValueError("Authentication token is required. Please login first.")

        url = f"{self.base_url}/polls"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "question": question,
            "options": options
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        return response.json()

    def delete_poll(self, poll_id: int) -> None:
        """
        Delete a poll.

        Args:
            poll_id: The ID of the poll to delete.

        Raises:
            ValueError: If no authentication token is set.
            requests.exceptions.HTTPError: If the poll is not found or user is not authorized.
        """
        if not self.token:
            raise ValueError("Authentication token is required. Please login first.")

        url = f"{self.base_url}/polls/{poll_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
