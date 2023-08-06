import json
import logging
import os

from django.apps import AppConfig
from django.utils.autoreload import autoreload_started

from pathlib import Path

logger = logging.getLogger(__name__)

MODULE_NAME = 'claim_ai'

DEFAULT_CONFIG = {
    'authentication': [],
    'claim_response_url': 'http://localhost:8000/claim_ai/ClaimResponse',
    'ai_model_file': "joblib_Voting_Model.pkl",
    'ai_scaler_file': "scaler.pkl",
    'ai_encoder_file': "Encoder.obj",
    'claim_response_organization': 'openIMIS-Claim-AI',
    'date_format': '%Y-%m-%d',
    'first_date': '2016-01-01'
}


def get_module_config_path():
    abs_path = Path(__file__).absolute().parent.parent
    return F'{abs_path}/module_config.json'


def config_autoreloader(sender, **kwargs):
    sender.watch_file(get_module_config_path())


if os.environ.get('NO_DATABASE_ENGINE', False) or os.environ.get('NO_DATABASE', False):
    path = get_module_config_path()
    with open(path) as json_file:
        DEFAULT_CONFIG = json.load(json_file)


class ClaimAiConfig(AppConfig):
    name = MODULE_NAME

    authentication = DEFAULT_CONFIG['authentication']
    ai_model_file = DEFAULT_CONFIG['ai_model_file']
    ai_encoder_file = DEFAULT_CONFIG['ai_encoder_file']
    ai_scaler_file = DEFAULT_CONFIG['ai_scaler_file']
    claim_response_organization = DEFAULT_CONFIG['claim_response_organization']
    claim_response_url = DEFAULT_CONFIG['claim_response_url']
    date_format = DEFAULT_CONFIG['date_format']
    first_date = DEFAULT_CONFIG['first_date']

    def _configure_perms(self, cfg):
        for config, config_value in cfg.items():
            setattr(ClaimAiConfig, config, config_value)

    def ready(self):
        from core.models import ModuleConfiguration
        try:
            if os.environ.get('NO_DATABASE_ENGINE', False) or os.environ.get('NO_DATABASE', False): 
                autoreload_started.connect(config_autoreloader)
                path = get_module_config_path()
                with open(path) as json_file:
                    cfg = json.load(json_file)
            else:
                cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CONFIG)
            self._configure_perms(cfg)
        except Exception as e:
            logger.error('Loading configuration for claim_ai failed, using default')
            self._configure_perms(DEFAULT_CONFIG)
