import json
import os
from click.testing import CliRunner
from elementalcms.management import cli


class TestInitCommandShould:

    @classmethod
    def setup_class(cls) -> None:
        with open('settings/testing.json') as json_data_file:
            cls.settings = json.load(json_data_file)

    def test_exit_early_when_project_is_already_initialized(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            os.makedirs('settings')
            with open('settings/debug.json', 'w') as f:
                f.write(json.dumps(self.settings))
            with open('.elemental', 'w') as e:
                e.write('{}')
            result = runner.invoke(cli, ['init'])
            assert 'Elemental CMS has been already initialized.' in result.output
            assert 'Initializing Elemental CMS' not in result.output
            assert 'Initialization completed...' not in result.output
