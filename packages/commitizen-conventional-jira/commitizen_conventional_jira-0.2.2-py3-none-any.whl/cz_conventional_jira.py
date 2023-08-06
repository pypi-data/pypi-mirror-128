import re
from typing import Pattern, AnyStr

from commitizen import config
from commitizen.cz import ConventionalCommitsCz


class ConventionalJiraCz(ConventionalCommitsCz):
    def schema_pattern(self) -> Pattern[AnyStr]:
        conf = config.read_cfg()
        jira_prefix = conf.settings.get('jira_prefix', None)
        jira_issues_required = conf.settings.get('jira_issues_required', False)
        jira_no_ticket_key = conf.settings.get('jira_no_ticket_key', None)
        if jira_prefix:
            if jira_no_ticket_key:
                issue_pattern = f"{jira_prefix}-(?:\d+(?:,{jira_prefix}-(?:\d+))*|{jira_no_ticket_key})"
            else:
                issue_pattern = f"{jira_prefix}-\d+(?:,{jira_prefix}-(?:\d+))*"
            if jira_issues_required:
                pattern = f"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)" \
                          f"(\({issue_pattern}\))!?:(\s.*)"
            else:
                pattern = f"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)" \
                          f"(\({issue_pattern}\))?!?:(\s.*)"
        else:
            pattern = (
                "(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
                "(\(\S+\))?!?:(\s.*)"
            )
        return re.compile(pattern)


discover_this = ConventionalJiraCz
