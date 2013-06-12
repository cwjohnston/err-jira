from errbot import BotPlugin
import logging
import re
import requests


class Jira(BotPlugin):
    """A plugin for interacting with Atlassian JIRA"""
    min_err_version = '1.6.0'  # Optional, but recommended
    max_err_version = '2.0.0'  # Optional, but recommended

    def get_configuration_template(self):
        """Defines the configuration structure this plugin supports"""
        return {'URL': "http://jira.example.com",
                'USERNAME': 'err',
                'PASSWORD': 'secret',
                'PROJECTS': ['FOO', 'BAR']}

    def get_issue(self, issue_id):
        """Retrieves issue JSON from JIRA"""
        response = requests.get(
            self.config['URL']+'/rest/api/latest/issue/'+issue_id+'.json',
            auth=(self.config['USERNAME'], self.config['PASSWORD']))
        return response

    def callback_message(self, conn, mess):
        """A callback which responds to mention of JIRA issues"""
        for project in self.config['PROJECTS']:
            regex = r'^.*(%s\-[0-9]+).*$' % project
            match = re.match(regex, mess.getBody(), flags=re.IGNORECASE)
            if match:
                issue_id = match.group(1).upper()
                logging.debug("[JIRA] matched issue_id: %s" % issue_id)
                issue_response = self.get_issue(issue_id)
                if issue_response.status_code in (200,):
                    logging.debug("[JIRA] retrieved issue data: %s" % issue_response)
                    issue_summary = issue_response.json()['fields']['summary']
                    html_message = "<html><body><a href=\"%s/browse/%s\">%s</a>: %s</body></html>" % (self.config['URL'], issue_id, issue_id, issue_summary,)
                    self.send(mess.getFrom(), html_message, message_type=mess.getType())
                elif issue_response.status_code in (401,):
                    self.send(mess.getFrom(), "Access Denied", message_type=mess.getType())
                elif issue_response.status_code in (404,):
                    self.send(mess.getFrom(), "Issue not found", message_type=mess.getType())
                else:
                    logging.error("[JIRA] encountered unknown response status code: %s" % issue_response.status_code)
                    logging.error("[JIRA] response body: %s" % issue_response.json())
                    self.send(mess.getFrom(), "Recieved an unexpected response, see logs for more detail", message_type=mess.getType())
