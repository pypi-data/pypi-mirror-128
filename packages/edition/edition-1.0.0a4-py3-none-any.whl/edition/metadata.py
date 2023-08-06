from typing import Optional, TypedDict


class Metadata(TypedDict, total=False):
    body: Optional[str]
    css: Optional[str]
    title: Optional[str]
    toc: Optional[str]
