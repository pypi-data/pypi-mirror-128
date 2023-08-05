#!/usr/bin/env python3

from configparser import ConfigParser
import os

"""
This handles all of our config needs for UNGI
"""


def config(section, option, filename):
    """
    Used to load the config and parse its values
    """
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        val = parser.get(section, option)
        return val


def list_index(section, filename):
    """
    used to list es indexes from ini file
    """
    parser = ConfigParser()
    parser.read(filename)
    index_list = []
    for x in parser[f"{section}"]:
        index_list.append(parser.get(f"{section}", x))
    return index_list


def auto_load(str_in=None):
    """
    used to load the config. the str_in is to be used for the path
    if it is None (when the user does not pass a argument) it will
    load the path from the env var UNGI_CONFIG
    """
    if str_in:
        return str_in
    else:
        config_path = os.environ["UNGI_CONFIG"]
        return config_path


class UngiConfig:
    """
    A Common config class used for bots and ungi cli tools
    only input is a path to the ini file
    """
    def __init__(self, path):

        # CONFIGURATION FOR BOTS
        self.config_path = path
        self.es_host = config("ES", "host", self.config_path) # elasticsearch
        self.db_path = config("DB", "path", self.config_path) # loot db path
        self.sql_script = config("DB", "script", self.config_path) #sql script
        self.discord = config("INDEX", "discord", self.config_path) #discord index
        self.reddit = config("INDEX", "reddit", self.config_path) #reddit index
        self.telegram = config("INDEX", "telegram", self.config_path) #telegram index
        self.loot = config("INDEX", "loot", self.config_path) # loot index
        self.reddit_client_id = config("REDDIT", "client_id", self.config_path)
        self.reddit_client_secret = config("REDDIT", "client_secret", self.config_path)
        self.reddit_client_username = config("REDDIT", "username", self.config_path)
        self.reddit_client_password = config("REDDIT", "password", self.config_path)
        self.reddit_client_user_agent = config("REDDIT", "user_agent", self.config_path)
        self.telegram_api_id = int(config("TELEGRAM", "api_id", self.config_path))
        self.telegram_api_hash = config("TELEGRAM", "api_hash", self.config_path)
        self.telegram_session = config("TELEGRAM", "session_file", self.config_path)
        self.telegram_media = config("TELEGRAM", "media", self.config_path)
        self.telegram_store_media = config("TELEGRAM", "store_media", self.config_path)
        self.timezone = config("TIME", "timezone", self.config_path)
        self.twitter = config("INDEX", "twitter", self.config_path)
        if self.telegram_store_media == "True" or self.telegram_store_media == "true":
            self.telegram_store_media = True
        else:
            self.telegram_store_media = False

        # CONFIGURATION FOR SERVER
        self.broker = config("CELERY", "broker_url", self.config_path)
        self.alert_type = config("ALERTS", "type", self.config_path)
        self.server_port = config("SERVER", "server_port", self.config_path)
        self.project_name = config("APP", "name", self.config_path) #to name the project
        self.project_description = config("APP", "description", self.config_path)
        # used for bots
        self.server_host = config("SERVER", "server_host", self.config_path)

        # email config
        self.smtp_host = config("ALERTS", "smtp_host", self.config_path)
        self.smtp_port = config("ALERTS", "smtp_port", self.config_path)
        self.smtp_username = config("ALERTS", "smtp_username", self.config_path)
        self.smtp_password = config("ALERTS", "smtp_password", self.config_path)
        self.to_email = config("ALERTS", "to_email", self.config_path)
        self.from_email = config("ALERTS", "from_email", self.config_path)

        # Discord Bot config (for alerts)
        self.alert_discord = config("ALERTS", "discord-token", self.config_path)

        # matrix config
        self.matrix_config = config("ALERTS", "matrix_config", self.config_path)
        self.matrix_username = config("ALERTS", "matrix_username", self.config_path)
        self.matrix_password = config("ALERTS", "matrix_password", self.config_path)
        self.matrix_session_name = config("ALERTS", "matrix_session_name", self.config_path)
        self.matrix_roomid = config("ALERTS", "matrix_roomid", self.config_path)
        self.matrix_rooms = []
        try:
            for roomid in self.matrix_roomid.split(","):
                self.matrix_rooms.append(roomid.rstrip())
        except ValueError:
            self.matrix_rooms.append(self.matrix_roomid.rstrip())
        self.matrix_home_server = config("ALERTS", "matrix_home_server", self.config_path)

        self.webhook = config("ALERTS", "webhook", self.config_path).rstrip()
        self.webhooks = []
        for endpoint in self.webhook.split(","):
            self.webhooks.append(endpoint)

        if self.alert_type == "all":
            self.use_email = True
            self.use_matrix = True
            self.use_telegram = True
            self.use_discord = True
            self.use_webhooks = True

        if self.alert_type == "email":
            self.use_email = True
        if self.alert_type == "matrix":
            self.use_matrix = True
        if self.alert_type == "discord":
            self.use_discord = True
        if self.alert_type == "telegram":
            self.use_telegram = True
        if self.alert_type == "webhooks":
            self.use_webhooks = True
        # twitter bot stuff

        self.proxy_type = config("TWITTER", "proxy_type", self.config_path)
        self.proxy_host = config("TWITTER", "proxy_type", self.config_path)
        self.proxy_port = config("TWITTER", "proxy_type", self.config_path)
        self.tor_control_port = config("TOR", "control_port", self.config_path)
        self.tor_pass = config("TOR", "pass", self.config_path)
        self.imgbb_api = config("API", "imgbb", self.config_path)


        # Stuff Used for ungi chat bots, so users can search the backend
        self.search_bot_email("SEARCH_BOT", "email", self.config_path) # guilded
        self.search_bot_password("SEARCH_BOT", "password", self.config_path) # guilded
        self.search_bot_discord("SEARCH_BOT", "discord_token", self.config_path)
