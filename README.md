# err-jira

A plugin for [Err](http://github.com/gbin/err) which watches your chat for mention of JIRA tickets. When a ticket is mentioned, the plugin will attempt to retrie ticket details via the configured JIRA REST API endpoint and displaying a link to the ticket along with the ticket summary.

## Config

The plugin needs to know:

* the location of your JIRA installation (`URL`)
* login credentials (`USERNAME` and `PASSWORD`)
* a list of valid keys for your projects (`PROJECTS`)

You can configure your Err bot for this plugin thusly:
`!config JIRA { 'URL': 'https://jira.example.com', 'USERNAME': 'errbot', 'PASSWORD': 'secret', 'PROJECTS': ['FOO','BAR','BAZ']}`

## Licence

Released into public domain. Do with it as you wish!
