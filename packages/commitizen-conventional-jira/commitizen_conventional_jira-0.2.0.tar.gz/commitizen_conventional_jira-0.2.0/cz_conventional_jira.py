from commitizen.cz import ConventionalCommitsCz


class ConventionalJiraCz(ConventionalCommitsCz):
    def schema_pattern(self) -> str:
        pattern = (
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)"
            r"(\(CC-\d{3,}(:?,CC-\d{3,})*\))?!?:(\s.*)"
        )
        return pattern


discover_this = ConventionalJiraCz
