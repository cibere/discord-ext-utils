"""
MIT License

Copyright (c) 2023-present cibere

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Literal, Optional, Sequence, Union, overload

from discord.ui import View
from discord.utils import MISSING

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
        "reference": reference,
        "mention_author": mention_author,
        "view": view,
        "suppress_embeds": suppress_embeds,
        "ephemeral": ephemeral,
        "wait": wait,
    }

    if isinstance(dest, commands.Context):
        _pop(kwargs, ["supress_embeds", "wait"])
        switch_to_none(kwargs)
        return await dest.send(**kwargs)
    elif isinstance(dest, discord.abc.Messageable):
        _pop(kwargs, ["supress_embeds", "wait", "ephemeral"])
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
                "reference",
                "supress_embeds",
                "mention_author",
            ],
        )
        return await dest.send(**kwargs)
    else:
        raise TypeError("Unknown destination given")
