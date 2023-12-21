# tests/test_delete_vault.py
import unittest
from unittest.mock import patch
from app.delete_vault import delete_vault

class TestDeleteVault(unittest.TestCase):

    @patch('app.delete_vault.boto3.client')
    def test_delete_vault_success(self, mock_client):
        mock_client.return_value.delete_vault.return_value = True
        result = delete_vault('test_vault')
        self.assertTrue(result)

    @patch('app.delete_vault.boto3.client')
    def test_delete_vault_failure(self, mock_client):
        mock_client.return_value.delete_vault.side_effect = Exception("Error")
        result = delete_vault('test_vault')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
