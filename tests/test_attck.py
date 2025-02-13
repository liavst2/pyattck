import os
import random
import tempfile
import pytest


default_config_data = {
    'data_path': os.path.abspath(os.path.expanduser(os.path.expandvars('~/pyattck/data'))),
    'enterprise_attck_json': "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
    'pre_attck_json': "https://raw.githubusercontent.com/mitre/cti/master/pre-attack/pre-attack.json",
    'mobile_attck_json': "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json",
    'nist_controls_json': "https://raw.githubusercontent.com/center-for-threat-informed-defense/attack-control-framework-mappings/master/frameworks/nist800-53-r4/stix/nist800-53-r4-controls.json",
    'generated_attck_json': "https://github.com/swimlane/pyattck/blob/master/generated_attck_data.json?raw=True",
    'generated_nist_json': "https://github.com/swimlane/pyattck/blob/master/attck_to_nist_controls.json?raw=True"
}


def get_random_file_or_url():
    if random.choice(['file', 'url']) == 'file':
        return tempfile.NamedTemporaryFile().name
    else:
        return random.choice(['https://letsautomate.it/article/index.xml', 'https://google.com', 'https://github.com/swimlane/pyattck'])


def test_default_config():
      from pyattck import Attck, Configuration
      attck = Attck()
      assert Configuration.config_data == default_config_data

@pytest.mark.parametrize(
    'target_attribute', 
    ['enterprise_attck_json', 'pre_attck_json', 'mobile_attck_json', 'nist_controls_json', 'generated_attck_json', 'generated_nist_json']
)
def test_setting_json_locations(target_attribute):
      from pyattck import Attck, Configuration

      enterprise_temp_value = get_random_file_or_url()
      pre_attck_temp_value = get_random_file_or_url()
      mobile_temp_value = get_random_file_or_url()
      nist_controls_temp_value = get_random_file_or_url()
      generated_attck_temp_value = get_random_file_or_url()
      generated_nist_temp_value = get_random_file_or_url()

      attck = Attck(
        enterprise_attck_json=enterprise_temp_value
      )
      assert Configuration.enterprise_attck_json == enterprise_temp_value

      attck = Attck(
        pre_attck_json=pre_attck_temp_value
      )
      assert Configuration.pre_attck_json == pre_attck_temp_value

      attck = Attck(
        mobile_attck_json=mobile_temp_value
      )
      assert Configuration.mobile_attck_json == mobile_temp_value

      attck = Attck(
        nist_controls_json=nist_controls_temp_value
      )
      assert Configuration.nist_controls_json == nist_controls_temp_value

      attck = Attck(
        generated_attck_json=generated_attck_temp_value
      )
      assert Configuration.generated_attck_json == generated_attck_temp_value

      attck = Attck(
        generated_nist_json=generated_nist_temp_value
      )
      assert Configuration.generated_nist_json == generated_nist_temp_value

def test_nested_subtechniques():
      from pyattck import Attck
      attck = Attck(nested_subtechniques=False)
      count = 0
      for technique in attck.enterprise.techniques:
          if technique.subtechnique:
              count += 1
      assert count >= 360

def test_passed_kwargs():
      from pyattck import Attck, Configuration
      attck = Attck()
      assert Configuration.requests_kwargs == {}
      args = {
          'verify': False,
          'proxies': {
              'http': 'http://10.10.1.10:3128',
              'https': 'http://10.10.1.10:1080',
          }
      }
      attck = Attck(**args)
      assert Configuration.requests_kwargs == args
