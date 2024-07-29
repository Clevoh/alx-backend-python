#!/usr/bin/env python3
"""
Tests for GithubOrgClient class methods
"""
import unittest
from unittest.mock import MagicMock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from typing import Dict, List
from client import GithubOrgClient
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Defines tests for GithubOrgClient class
    """

    @parameterized.expand(["google", "abc"])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get_json: MagicMock) -> None:
        """
        Tests the org property of GithubOrgClient class
        Args:
            org (str): organization name
            mock_get_json (MagicMock): a MagicMock object of `get_json` function
        Returns:
            None
        """
        client_instance = GithubOrgClient(org)
        self.assertEqual(client_instance.org, mock_get_json.return_value)
        mock_get_json.assert_called_once_with(client_instance.ORG_URL.format(org=org))

    def test_public_repos_url(self) -> None:
        """
        Test _public_repos_url property
        """
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/alx/repos'}
            client_instance = GithubOrgClient('alx')
            self.assertEqual(client_instance._public_repos_url, mock_org.return_value['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        Test public_repos method
        """
        mock_get_json.return_value = [
            {'name': 'repo1', 'license': {'key': 'license1'}},
            {'name': 'repo2', 'license': {'key': 'license2'}},
            {'name': 'repo3', 'license': {'key': 'license1'}}
        ]
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'https://api.github.com/orgs/test-org/repos'
            client_instance = GithubOrgClient('test-org')
            self.assertEqual(client_instance.public_repos(), ['repo1', 'repo2', 'repo3'])
            mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """
        Test has_license method
        Args:
            repo (Dict): repository dictionary
            license_key (str): license key to check
            expected (bool): expected result
        Returns:
            None
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        SetUp class method to mock requests.get
        """
        cls.get_patcher = patch('requests.get', side_effect=cls.mocked_requests_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        TearDown class method to stop the patcher
        """
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests_get(url):
        """
        Mock requests.get method
        """
        if url == GithubOrgClient.ORG_URL.format(org="google"):
            return MockResponse(org_payload)
        elif url == "https://api.github.com/orgs/google/repos":
            return MockResponse(repos_payload)
        return MockResponse(None, 404)

    def test_public_repos(self) -> None:
        """
        Test public_repos method without license
        """
        client_instance = GithubOrgClient('google')
        self.assertEqual(client_instance.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test public_repos method with license
        """
        client_instance = GithubOrgClient('google')
        self.assertEqual(client_instance.public_repos(license="apache-2.0"), self.apache2_repos)


class MockResponse:
    """
    Mock response for requests.get
    """
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


if __name__ == '__main__':
    unittest.main()