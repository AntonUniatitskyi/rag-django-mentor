from aiogram.utils.formatting import Text, Bold, as_marked_list


def build_sources_block(sources: list[str]) -> Text | None:
    if not sources:
        return None
    return Text(Bold("Джерела:"), "\n", as_marked_list(*sources))