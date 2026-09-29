import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('fim', REPO / 'file-integrity-monitor/fim.py')
fim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fim)


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'files'
        self.root.mkdir()
        self.db = Path(self.temp.name) / 'baseline.sqlite'

    def test_lifecycle_and_baseline_preserved(self):
        (self.root / 'changed.txt').write_text('before')
        (self.root / 'deleted.txt').write_text('original')
        fim.run(self.root, self.db, True)
        self.assertEqual(fim.run(self.root, self.db)['events'], [])
        (self.root / 'changed.txt').write_text('after')
        (self.root / 'deleted.txt').unlink()
        (self.root / 'added.txt').write_text('new')
        expected = [{'kind': 'ADDED', 'path': 'added.txt'},
                    {'kind': 'MODIFIED', 'path': 'changed.txt'},
                    {'kind': 'DELETED', 'path': 'deleted.txt'}]
        self.assertEqual(fim.run(self.root, self.db)['events'], expected)
        self.assertEqual(fim.run(self.root, self.db)['events'], expected)
        with self.assertRaises(ValueError):
            fim.run(self.root, self.db, True)

    def test_guards(self):
        with self.assertRaises(ValueError):
            fim.run(self.root, self.root / 'bad.sqlite', True)
        with self.assertRaises(ValueError):
            fim.run(self.root, self.db)
        fim.run(self.root, self.db, True)
        other = Path(self.temp.name) / 'other'
        other.mkdir()
        with self.assertRaises(ValueError):
            fim.run(other, self.db)

    def test_symlink_rejected(self):
        (self.root / 'link').symlink_to(self.db)
        with self.assertRaises(ValueError):
            fim.run(self.root, self.db, True)
        self.assertFalse(self.db.exists())

    def test_cli_exit_codes(self):
        command = ['python3', str(REPO / 'file-integrity-monitor/fim.py')]
        for action, expected in [('check', 2), ('init', 0), ('check', 0)]:
            result = subprocess.run(command + [action, str(self.root), '--database', str(self.db)], capture_output=True)
            self.assertEqual(result.returncode, expected)
        (self.root / 'new').write_text('changed')
        result = subprocess.run(command + ['check', str(self.root), '--database', str(self.db)], capture_output=True)
        self.assertEqual(result.returncode, 1)


class LogTests(unittest.TestCase):
    def test_compiled_analyzer(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = str(Path(directory) / 'analyzer')
            subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-Werror',
                            str(REPO / 'security-log-analyzer/security_log_analyzer.cpp'), '-o', binary], check=True)
            sample = REPO / 'security-log-analyzer/samples/auth.log'
            result = subprocess.run([binary, str(sample)], capture_output=True, text=True, check=True)
            self.assertIn('[ALERT] 192.0.2.10: 3 failures', result.stdout)
            self.assertNotIn('[ALERT] 198.51.100.20', result.stdout)
            self.assertIn('Malformed lines ignored: 1', result.stdout)
            self.assertEqual(subprocess.run([binary, str(sample) + '.missing'], capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
