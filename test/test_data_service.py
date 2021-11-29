import unittest
import os
from data_service import fetchAll, fetchPage, fetchTicket, getCredentials
from unittest.mock import Mock, patch, mock_open, MagicMock

class BasicTests(unittest.TestCase):
    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_fetchAll_response_with_decorator(self, mock_get):
        """Mocking fetchAll using a decorator"""
        mock_get.return_value.json = MagicMock(return_value={
            'tickets': [
                1, 2, 3
            ],
        })
        # Mock status code of response.
        response = fetchAll()

        print(response)

        # Assert that the request-response cycle completed successfully.
        self.assertNotEqual(len(response['tickets']), 0)
    
    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_fetchPage_response_with_decorator(self, mock_get):
        """Mocking fetchPage using a decorator"""
        mock_get.return_value.json = MagicMock(return_value={
            'tickets': [
                1, 2, 3
            ],
        })
        # Next page exists
        response = fetchPage('https://zccacoderhasnoname.zendesk.com/api/v2/tickets?page%5Bbefore%5D=eyJvIjoibmljZV9pZCIsInYiOiJhUUVBQUFBQUFBQUEifQ%3D%3D&page%5Bsize%5D=25')

        # Assert that the request-response cycle completed successfully.
        self.assertNotEqual(len(response['tickets']), 0)

    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_fetchTicket_response_with_decorator(self, mock_get):
        """Mocking fetchTicket using a decorator"""
        mock_get.return_value.json = MagicMock(return_value={
            'ticket': {
                'id': 2,
            },
        })
        # Next page exists
        response = fetchTicket(3)

        # Assert that the request-response cycle completed successfully.
        self.assertNotEqual(response['ticket'], None)

    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_reportErrorsAndExit_401_response_with_decorator(self, mock_get):
        """Mocking reportErrorsAndExit 401 using a decorator"""
        
        mock_get.return_value.status_code = 401
        with self.assertRaises(SystemExit):
            # Status code 401
            response = fetchTicket(3)

    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_reportErrorsAndExit_403_response_with_decorator(self, mock_get):
        """Mocking reportErrorsAndExit 403 using a decorator"""
        
        mock_get.return_value.status_code = 403
        with self.assertRaises(SystemExit):
            # Status code 401
            response = fetchTicket(3)
            
    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_reportErrorsAndExit_429_response_with_decorator(self, mock_get):
        """Mocking reportErrorsAndExit 403 using a decorator"""
        
        mock_get.return_value.status_code = 429
        with self.assertRaises(SystemExit):
            # Status code 401
            response = fetchTicket(3)
    
    @patch('data_service.requests.get')  # Mock 'requests' module 'get' method.
    def test_reportErrorsAndExit_500_response_with_decorator(self, mock_get):
        """Mocking reportErrorsAndExit 500 using a decorator"""
        
        mock_get.return_value.status_code = 500
        with self.assertRaises(SystemExit):
            # Status code 401
            response = fetchTicket(3)
    
    def test_getCredentials_open_fails(self):
        """Mocking test_getCredentials_open_fails using a decorator"""
        os.rename('config.json', 'test.config.json')

        with self.assertRaises(SystemExit) as se:
            resp = getCredentials()
        
        os.rename('test.config.json', 'config.json')

    @patch('data_service.json.load')
    def test_getCredentials_json_fails(self, mock_load):
        """Mocking test_getCredentials_json_fails using a decorator"""
        mock_load.return_value = {}

        with self.assertRaises(SystemExit) as se:
            resp = getCredentials()


if __name__ == "__main__":
    unittest.main()

