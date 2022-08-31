from datetime import datetime
from lxml import html
import argparse
import requests
import typing


class Reply:
    def __init__(self, author_name: str, reply_text: str, message_url: str) -> None:
        self.author_name = author_name
        self.reply_text = reply_text
        self.message_url = message_url
        pass


class WidgetMessage:
    def __init__(
        self,
        group_name: str,
        message_id: int,
        author_name: str,
        author_url: str,
        message_text: str,
        message_datetime: datetime,
        reply: typing.Optional[Reply],
    ) -> None:
        self.group_name = group_name
        self.message_id = message_id
        self.author_name = author_name
        self.author_url = author_url
        self.message_text = message_text
        self.message_datetime = message_datetime
        self.reply = reply
        pass

    def __str__(self) -> str:
        ret = f"{self.group_name}/{self.message_id}"
        ret += f": {self.author_name} ({self.author_url})"
        ret += f" at {self.message_datetime}"
        if self.reply:
            ret += "\nin reply to"
            ret += f" {self.reply.author_name} ({self.reply.message_url}):"
            ret += f"\n> {self.reply.reply_text}"
        ret += f"\n\n{self.message_text}"
        return ret


AUTHOR_CLASS = "tgme_widget_message_author accent_color"


def request_message(
    s: requests.Session, group_name: str, message_id: int
) -> WidgetMessage:
    r = s.get(f"https://t.me/{group_name}/{message_id}?embed=1")
    tree = html.fromstring(r.text)
    author_name = tree.xpath(f"//div[@class='{AUTHOR_CLASS}']/a[1]/span/text()")[0]
    author_url = tree.xpath(f"//div[@class='{AUTHOR_CLASS}']/a[1]/@href")[0]
    message_text = " ".join(
        tree.xpath("//div[@class='tgme_widget_message_text js-message_text']/text()")
    )
    message_datetime = datetime.fromisoformat(
        tree.xpath(
            "//div[@class='tgme_widget_message_info js-message_info']/span/a/time/@datetime"
        )[0]
    )
    reply = None
    reply_a_children = tree.xpath(f"//a[@class='tgme_widget_message_reply']")
    if len(reply_a_children) != 0:
        reply_a_element = reply_a_children[0]
        reply_url = reply_a_element.get("href")
        reply_author_name = reply_a_element.xpath(
            f"./div[@class='{AUTHOR_CLASS}']/span/text()"
        )[0]
        reply_text = reply_a_element.xpath(
            "./div[@class='tgme_widget_message_text js-message_reply_text']/text()"
        )[0]
        reply = Reply(reply_author_name, reply_text, reply_url)
    return WidgetMessage(
        group_name,
        message_id,
        author_name,
        author_url,
        message_text,
        message_datetime,
        reply,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Parse Telegram messages in public groups through t.me links"
    )
    parser.add_argument(
        "-g",
        "--group-name",
        help="short link of a public group withow @",
        required=True,
    )
    parser.add_argument(
        "-s", "--start-id", help="start message id", type=int, required=True
    )
    parser.add_argument(
        "-c", "--count", help="message count", type=int, required=True
    )
    args = parser.parse_args()

    s = requests.session()
    for message_id in range(args.start_id, args.start_id + args.count):
        try:
            msg = request_message(s, args.group_name, message_id)
            print(msg)
        except Exception as ex:
            print(f"{message_id}: Cannot parse HTML: {ex}")
        print("=====")


if __name__ == "__main__":
    main()
