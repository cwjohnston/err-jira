from errbot import BotPlugin
import re, requests

class Jira(BotPlugin):
    """A plugin for retrieving ticket info from Atlassian JIRA"""
    min_err_version = '1.6.0'
    max_err_version = ''

    def get_configuration_template(self):
        return {'URL': "http://jira.example.com",
                'USERNAME': 'err',
                'PASSWORD': 'secret',
                'PROJECTS': ['FOO', 'BAR']}

    def get_issue(self, issue_id):
        """Retrieves issue JSON from JIRA"""
        uri = self.config['URL']+'/rest/api/latest/issue/'+issue_id+'.json'
        self.log.debug("Requesting URI: {}".format(uri))
        response = requests.get(uri, auth=(self.config['USERNAME'], self.config['PASSWORD']))
        return response

    def callback_message(self, message):
        if self.config:
            matches = []
            regexes = []

            for project in self.config['PROJECTS']:
                self.log.debug("Appending project {} to search".format(project))
                regexes.append(r"({}\-[0-9]+)".format(project))
            for regex in regexes:
                self.log.debug("Searching for {} in {}".format(regex, message.body))
                matches.extend(re.findall(regex, message.body, flags=re.IGNORECASE))
            if matches:
                # set() gives us uniques, but does not preserve order.
                self.log.debug("Match found!")
                for match in set(matches):
                    issue_id = match
                    self.log.debug("Matched issue_id: {}".format(issue_id))
                    issue_response = self.get_issue(issue_id)
                    if issue_response.status_code in (200,):
                        self.log.debug("Retrieved issue data: {}".format(issue_response))
                        issue_id = issue_id.upper()
                        issue_summary = issue_response.json()['fields']['summary']
                        jira_link = "{}/browse/{}".format(self.config['URL'], issue_id)
                        self.log.debug("Jira returned summary: {}".format(issue_summary))
                        self.send_card(title = "JIRA case: {}".format(issue_id),
                                       body = "JIRA: {}".format(issue_summary),
                                       link = jira_link,
                                       color = 'blue',
                                       in_reply_to = message)
                    elif issue_response.status_code in (401,):
                        self.send(message.frm, "Access Denied")
                    elif issue_response.status_code in (404,):
                        self.send(message.frm, "Issue not found")
                    else:
                        self.log.error("Encountered unknown response status code: {}".format(issue_response.status_code))
                        self.log.error("Response body: {}".format(issue_response.json()))
                        self.send(message.frm, "Recieved an unexpected response, see logs for more detail")
