from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class KeywordNote:
    keyword: str
    category: str
    related_url: str
    tags: List[str] = field(default_factory=list)
    description: str = ""
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote):
        self.notes.append(note)

    def filter_by_category(self, category: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.category == category]

    def search_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]


def format_notes_table(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无笔记）"

    lines = []
    lines.append(f"{'关键词':<20} {'分类':<12} {'URL':<40} {'标签':<30} {'描述':<30}")
    lines.append("-" * 132)
    for note in notes:
        tags_str = ", ".join(note.tags) if note.tags else ""
        desc_short = note.description[:28] + ".." if len(note.description) > 28 else note.description
        lines.append(f"{note.keyword:<20} {note.category:<12} {note.related_url:<40} {tags_str:<30} {desc_short:<30}")
    return "\n".join(lines)


def format_notes_summary(notes: List[KeywordNote]) -> str:
    if not notes:
        return "暂无笔记记录。"

    result = []
    for i, note in enumerate(notes, 1):
        result.append(f"{i}. [{note.keyword}] ({note.category})")
        result.append(f"   URL: {note.related_url}")
        if note.tags:
            result.append(f"   标签: {', '.join(note.tags)}")
        if note.description:
            result.append(f"   说明: {note.description}")
        result.append(f"   创建时间: {note.created_at}")
        result.append("")
    return "\n".join(result)


def main():
    collection = NoteCollection()

    sample_data = [
        KeywordNote(
            keyword="爱游戏体育",
            category="体育平台",
            related_url="https://webs-igamesports.com",
            tags=["体育", "电竞", "在线"],
            description="专注于爱游戏体育的综合体育资讯与赛事平台"
        ),
        KeywordNote(
            keyword="电竞比赛",
            category="赛事",
            related_url="https://webs-igamesports.com/esports",
            tags=["电竞", "赛事", "直播"],
            description="提供最新电竞赛事信息和比分"
        ),
        KeywordNote(
            keyword="体育新闻",
            category="资讯",
            related_url="https://webs-igamesports.com/news",
            tags=["体育", "新闻", "快讯"],
            description="每日体育新闻更新"
        ),
    ]

    for note in sample_data:
        collection.add(note)

    print("=== 关键词笔记（表格格式）===")
    print(format_notes_table(collection.notes))

    print("\n=== 关键词笔记（摘要格式）===")
    print(format_notes_summary(collection.notes))

    print("\n=== 分类筛选（体育平台）===")
    filtered = collection.filter_by_category("体育平台")
    print(format_notes_table(filtered))

    print("\n=== 关键词搜索（爱游戏）===")
    searched = collection.search_by_keyword("爱游戏")
    print(format_notes_summary(searched))


if __name__ == "__main__":
    main()