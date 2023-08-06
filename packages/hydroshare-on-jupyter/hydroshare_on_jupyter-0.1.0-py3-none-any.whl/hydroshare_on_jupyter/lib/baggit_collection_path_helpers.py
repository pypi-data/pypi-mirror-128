import re


class BaggitCollectionPathUtilities:
    """Utility methods for modifying Baggit Collection filesystem paths."""

    BAGGIT_PREFIX_RE = r"^/?data/contents/?"
    BAGGIT_PREFIX_MATCHER = re.compile(BAGGIT_PREFIX_RE)
    BAGGIT_PREFIX = "/data/contents/"

    @staticmethod
    def truncate_baggit_prefix(file_path: str) -> str:
        baggit_prefix_match = BaggitCollectionPathUtilities.BAGGIT_PREFIX_MATCHER.match(
            file_path
        )

        if baggit_prefix_match is not None:
            # left-truncate baggit prefix path
            file_path = file_path[baggit_prefix_match.end() :]

        return file_path

    @staticmethod
    def prepend_baggit_prefix(file_path: str) -> str:
        # remove existing prefix to sanitize the input
        left_truncated_path = BaggitCollectionPathUtilities._truncate_baggit_prefix(
            file_path
        )

        return f"{BaggitCollectionPathUtilities.BAGGIT_PREFIX}{left_truncated_path}"
