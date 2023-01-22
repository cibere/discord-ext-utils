from typing import Literal, Optional, Sequence, Union, overload

import discord
from discord import (
    AllowedMentions,
    Embed,
    File,
    GuildSticker,
    Message,
    MessageReference,
    PartialMessage,
    StickerItem,
)
from discord.ext import commands
from discord.ui import View
from discord.utils import MISSING


def _pop(item: dict, items: list):
    for i in items:
        try:
            item.pop(i)
        except KeyError:
            pass


def switch_to_none(kwargs: dict):
    for item in kwargs:
        if kwargs[item] is MISSING:
            kwargs[item] = None


@overload
async def send_message(
    dest: commands.Context | discord.abc.Messageable,
    /,
    *,
    content: str = MISSING,
    tts: bool = False,
    embed: Embed = MISSING,
    embeds: Sequence[Embed] = MISSING,
    file: File = MISSING,
    files: Sequence[File] = MISSING,
    stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
    delete_after: float = MISSING,
    nonce: Union[str, int] = MISSING,
    allowed_mentions: AllowedMentions = MISSING,
    reference: Union[Message, MessageReference, PartialMessage] = MISSING,
    mention_author: bool = MISSING,
    view: View = MISSING,
    suppress_embeds: bool = False,
    ephemeral: bool = False,
    wait: bool = False,
) -> discord.Message:
    ...


@overload
async def send_message(
    dest: discord.Interaction,
    /,
    *,
    content: str = MISSING,
    tts: bool = False,
    embed: Embed = MISSING,
    embeds: Sequence[Embed] = MISSING,
    file: File = MISSING,
    files: Sequence[File] = MISSING,
    stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
    delete_after: float = MISSING,
    nonce: Union[str, int] = MISSING,
    allowed_mentions: AllowedMentions = MISSING,
    reference: Union[Message, MessageReference, PartialMessage] = MISSING,
    mention_author: bool = MISSING,
    view: View = MISSING,
    suppress_embeds: bool = False,
    ephemeral: bool = False,
    wait: bool = False,
) -> Optional[discord.Message]:
    ...


@overload
async def send_message(
    dest: discord.Webhook,
    /,
    *,
    content: str = MISSING,
    tts: bool = False,
    embed: Embed = MISSING,
    embeds: Sequence[Embed] = MISSING,
    file: File = MISSING,
    files: Sequence[File] = MISSING,
    stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
    delete_after: float = MISSING,
    nonce: Union[str, int] = MISSING,
    allowed_mentions: AllowedMentions = MISSING,
    reference: Union[Message, MessageReference, PartialMessage] = MISSING,
    mention_author: bool = MISSING,
    view: View = MISSING,
    suppress_embeds: bool = False,
    ephemeral: bool = False,
    wait: Literal[True],
) -> discord.Message:
    ...


@overload
async def send_message(
    dest: discord.Webhook,
    /,
    *,
    content: str = MISSING,
    tts: bool = False,
    embed: Embed = MISSING,
    embeds: Sequence[Embed] = MISSING,
    file: File = MISSING,
    files: Sequence[File] = MISSING,
    stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
    delete_after: float = MISSING,
    nonce: Union[str, int] = MISSING,
    allowed_mentions: AllowedMentions = MISSING,
    reference: Union[Message, MessageReference, PartialMessage] = MISSING,
    mention_author: bool = MISSING,
    view: View = MISSING,
    suppress_embeds: bool = False,
    ephemeral: bool = False,
    wait: Literal[False],
) -> discord.Message:
    ...


async def send_message(
    dest: commands.Context
    | discord.Interaction
    | discord.abc.Messageable
    | discord.Webhook,
    /,
    *,
    content: str = MISSING,
    tts: bool = False,
    embed: Embed = MISSING,
    embeds: Sequence[Embed] = MISSING,
    file: File = MISSING,
    files: Sequence[File] = MISSING,
    stickers: Sequence[Union[GuildSticker, StickerItem]] = MISSING,
    delete_after: Optional[float] = None,
    nonce: Union[str, int] = MISSING,
    allowed_mentions: AllowedMentions = MISSING,
    reference: Union[Message, MessageReference, PartialMessage] = MISSING,
    mention_author: bool = MISSING,
    view: View = MISSING,
    suppress_embeds: bool = False,
    ephemeral: bool = False,
    wait: bool = False,
) -> Optional[discord.Message]:
    """A helper func to send messages.

    There are a lot of parameters, and you can read discord.py's documentation on what each of them do. The only custom param is the first pos-only param, which is your destination. Ex: ctx, interaction, channel, webhook, user, etc.
    Also, if a certain send method does not support a param it will be dropped.
    """

    if file:
        files = [file]
    if embed:
        embeds = [embed]

    kwargs = {
        "content": content,
        "tts": tts,
        "embeds": embeds,
        "files": files,
        "stickers": stickers,
        "delete_after": delete_after,
        "nonce": nonce,
        "allow_mentions": allowed_mentions,
        "reference": reference,
        "mention_author": mention_author,
        "view": view,
        "supress_embeds": suppress_embeds,
        "ephemeral": ephemeral,
        "wait": wait,
    }

    if isinstance(dest, commands.Context):
        _pop(kwargs, ["allow_mentions", "supress_embeds", "wait"])
        switch_to_none(kwargs)
        return await dest.send(**kwargs)
    elif isinstance(dest, discord.abc.Messageable):
        _pop(kwargs, ["allow_mentions", "supress_embeds", "wait", "ephemeral"])
        switch_to_none(kwargs)
        return await dest.send(**kwargs)

    elif isinstance(dest, discord.Interaction):
        if dest.response.is_done():
            return await send_message(dest.followup, **kwargs)
        else:
            _pop(
                kwargs,
                [
                    "stickers",
                    "nonce",
                    "allow_mentions",
                    "reference",
                    "mention_author",
                    "supress_embeds",
                    "wait",
                ],
            )
            return await dest.response.send_message(**kwargs)
    elif isinstance(dest, discord.Webhook):
        _pop(
            kwargs,
            [
                "stickers",
                "delete_after",
                "nonce",
                "allow_mentions",
                "reference",
                "supress_embeds",
                "mention_author",
            ],
        )
        return await dest.send(**kwargs)
    else:
        raise TypeError("Unknown destination given")
