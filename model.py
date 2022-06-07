from dataclasses import dataclass, field


@dataclass(frozen=True)
class NewsOverview:
    press: str = field(repr=True, hash=True)
    link: str = field(repr=False, hash=False)
    title: str = field(repr=True, hash=True)
