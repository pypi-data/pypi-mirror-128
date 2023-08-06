# Relative import
import sys, pathlib
sys.path.insert(1, str(pathlib.Path(__file__).parent.parent.parent.resolve()))
from sail import cli, util
import sail

import io, os
import click
import unittest
import subprocess
import requests
import json
from click.testing import CliRunner
from unittest.mock import Mock, patch

# Skip some tests if true
work_in_progress = False

# Some commands use os.execlp to pass control to the
# child process, which stops test execution after the
# spawned process exits. We can mock it and just pipe
# to a regular subprocess.
def _execlp_side_effect(*args, **kwargs):
	print(subprocess.check_output(args[1:], encoding='utf8'))

_execlp = Mock(side_effect=_execlp_side_effect)

@patch('os.execlp', _execlp)
@unittest.skipIf(__name__ != '__main__', 'Slow test, must run explicitly')
class TestEnd2End(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.runner = CliRunner(mix_stderr=False)
		# cls.fs = cls.runner.isolated_filesystem()
		# cls.fs.__enter__()
		cls.home = None

	@classmethod
	def tearDownClass(cls):
		# cls.fs.__exit__(None, None, None)
		pass

	def setUp(self):
		self.home = self.__class__.home

	def test_002_wp_home(self):
		result = self.runner.invoke(cli, ['wp', 'option', 'get', 'home'])
		self.assertEqual(result.exit_code, 0)
		self.__class__.home = result.output.strip()

	def test_018_deployignore(self):
		with open('.deployignore', 'w+') as f:
			f.write('# this is a comment\n')
			f.write('node_modules\n')
			f.write('debug.log\n')
			f.write('/readme.html\n')
			f.write('*.sql\n')
			f.write('!important.sql\n')

		pathlib.Path('not-ignored.txt').touch()
		pathlib.Path('important.sql').touch()
		pathlib.Path('backup.sql').touch()
		pathlib.Path('node_modules/one/two/three').mkdir(parents=True, exist_ok=True)
		pathlib.Path('node_modules/one/two/three/four').touch()
		pathlib.Path('wp-content/node_modules/one/two/three').mkdir(parents=True, exist_ok=True)
		pathlib.Path('wp-content/node_modules/one/two/three/four').touch()
		pathlib.Path('debug.log').touch()
		pathlib.Path('wp-content/debug.log').touch()
		pathlib.Path('readme.html').touch()
		pathlib.Path('wp-content/readme.html').touch()

		result = self.runner.invoke(cli, ['diff', '--raw'])
		self.assertEqual(result.exit_code, 0)
		diff = result.output.split('\n')

		self.assertIn('not-ignored.txt', diff)
		self.assertIn('important.sql', diff)
		self.assertNotIn('backup.sql', diff)
		self.assertNotIn('node_modules/one/two/three', diff)
		self.assertNotIn('node_modules/one/two/three/four', diff)
		self.assertNotIn('wp-content/node_modules/one/two/three', diff)
		self.assertNotIn('wp-content/node_modules/one/two/three/four', diff)
		self.assertNotIn('debug.log', diff)
		self.assertNotIn('wp-content/debug.log', diff)
		self.assertNotIn('readme.html', diff)
		self.assertIn('wp-content/readme.html', diff)

if __name__ == '__main__':
	unittest.main()
