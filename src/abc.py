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
from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

import discord
from discord import Interaction, ui
from discord.ext import commands
from discord.ui.item import Item

if TYPE_CHECKING:
    from discord.types.interactions import (
        ModalSubmitComponentInteractionData as ModalSubmitComponentInteractionDataPayload,
    )

__all__ = ["View", "Modal"]

Client = discord.Client | commands.Bot
_client_log = logging.getLogger("discord.Client")


class View(ui.View):
    """Represents a UI view.

    This object must be inherited to create a UI within Discord.

    .. versionadded:: 2.0

    Parameters
    -----------
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.

    DOCSTRING WAS TAKEN FROM DISCORD.PY'S MODAL ON 1/19/2023
    """

    async def _interaction_check(self, interaction: discord.Interaction) -> bool:
        if hasattr(interaction.client, "interaction_check"):
            global_check = getattr(interaction.client, "interaction_check")
            global_ = await global_check(interaction)
            if not global_:
                return False

        single = await self.interaction_check(interaction)
        return single

    async def _scheduled_task(self, item: Item, interaction: Interaction):
        """Overriding `_scheduled_task` so we can dispatch the `view_error` event before triggering `view.on_error`, and make a global `interaction_check`."""

        try:
            item._refresh_state(interaction, interaction.data)  # type: ignore

            allow = await self._interaction_check(interaction)
            if not allow:
                return

            if self.timeout:
                self.__timeout_expiry = time.monotonic() + self.timeout

            await item.callback(interaction)
        except Exception as e:
            interaction.client.dispatch("view_error", interaction, e, item)
            return await self.on_error(interaction, e, item)

    async def on_error(
        self, interaction: Interaction, error: Exception, item: Item[Any], /
    ) -> None:
        """|coro|

        A callback that is called when an item's callback or :meth:`interaction_check`
        fails with an error.

        The default implementation logs to the library logger.

        Parameters
        -----------
        interaction: :class:`~discord.Interaction`
            The interaction that led to the failure.
        error: :class:`Exception`
            The exception that was raised.
        item: :class:`Item`
            The item that failed the dispatch.

        DOCSTRING WAS TAKEN FROM DISCORD.PY'S MODAL ON 1/19/2023
        """

        _client_log.error(
            "Ignoring exception in view %r for item %r", self, item, exc_info=error
        )


class Modal(ui.Modal):
    """Represents a UI modal.

    This object must be inherited to create a modal popup window within discord.

    .. versionadded:: 2.0

    Examples
    ----------

    .. code-block:: python3

        from discord import ui

        class Questionnaire(ui.Modal, title='Questionnaire Response'):
            name = ui.TextInput(label='Name')
            answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

    Parameters
    -----------
    title: :class:`str`
        The title of the modal. Can only be up to 45 characters.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    custom_id: :class:`str`
        The ID of the modal that gets received during an interaction.
        If not given then one is generated for you.
        Can only be up to 100 characters.

    Attributes
    ------------
    title: :class:`str`
        The title of the modal.
    custom_id: :class:`str`
        The ID of the modal that gets received during an interaction.

    DOCSTRING WAS TAKEN FROM DISCORD.PY'S MODAL ON 1/19/2023
    """

    async def _scheduled_task(
        self,
        interaction: Interaction,
        components: list[ModalSubmitComponentInteractionDataPayload],
    ):
        """Overriding `_scheduled_task` so we can dispatch the `modal_error` event before triggering `modal.on_error`"""

        try:
            self._refresh_timeout()
            self._refresh(interaction, components)

            allow = await self.interaction_check(interaction)
            if not allow:
                return

            await self.on_submit(interaction)
        except Exception as e:
            interaction.client.dispatch("modal_error", interaction, e)
            return await self.on_error(interaction, e)
        else:
            # No error, so assume this will always happen
            # In the future, maybe this will require checking if we set an error response.
            self.stop()

    async def on_error(self, interaction: Interaction, error: Exception, /) -> None:
        """|coro|

        A callback that is called when :meth:`on_submit`
        fails with an error.

        The default implementation logs to the library logger.

        Parameters
        -----------
        interaction: :class:`~discord.Interaction`
            The interaction that led to the failure.
        error: :class:`Exception`
            The exception that was raised.

        DOCSTRING WAS TAKEN FROM DISCORD.PY'S MODAL ON 1/19/2023
        """

        _client_log.error("Ignoring exception in modal %r:", self, exc_info=error)
