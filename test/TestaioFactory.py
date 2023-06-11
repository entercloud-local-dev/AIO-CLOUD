import unittest
from unittest.mock import patch
import AIO-cloud

class TestAioFactory(unittest.TestCase):
    @patch('subprocess.run')
    def test_aioFactory_calls_three_scripts(self, mock_subprocess):
        aioFactory.run_aioFactory(['AIO-aws.py', 'AIO-az.py', 'AIO-gcp.py'])

        # Ensure the subprocess.run function was called three times
        self.assertEqual(mock_subprocess.call_count, 3)
        
        # Ensure each expected script was called
        mock_subprocess.assert_any_call(['python', 'AIO-aws.py'], check=True)
        mock_subprocess.assert_any_call(['python', 'AIO-az.py'], check=True)
        mock_subprocess.assert_any_call(['python', 'AIO-gcp.py'], check=True)

if __name__ == '__main__':
    unittest.main()
