from errbot import BotPlugin, botcmd
import config

import re

class Jira(BotPlugin):
    """An Err plugin skeleton"""
    min_err_version = '1.6.0' # Optional, but recommended
    max_err_version = '2.0.0' # Optional, but recommended

    def get_configuration_template(self):
        """Defines the configuration structure this plugin supports"""
        return {'URL': "http://jira.example.com",
                'PROJECTS': ['FOO', 'BAR'] }

    def callback_message(self, conn, mess):
        """A callback which responds with links to JIRA issues"""
        message = ""
        for project in self.config['PROJECTS']:
            regex = r'%s\-[0-9]+' % project
            match = re.match(regex, mess.getBody(), flags=re.IGNORECASE)
            if match:
                message += "%s: %s/browse/%s" % (match.group(0), self.config['URL'], match.group(0),)
            if message:
                self.send(mess.getFrom(), message, message_type=mess.getType())
                return
