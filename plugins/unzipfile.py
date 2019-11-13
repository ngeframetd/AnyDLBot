#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from zipfile import ZipFile
import os
import shutil
import subprocess
import time
from helper_funcs.display_progress import humanbytes, progress_for_pyrogram
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes


extracted = Config.DOWNLOAD_LOCATION + "extracted/"
thumb_image_path = Config.DOWNLOAD_LOCATION + "/thumb_image.jpg"
if not os.path.isdir(extracted):
    os.makedirs(extracted)

@pyrogram.Client.on_message(pyrogram.Filters.command(["zipcikar"]))
async def unzip(bot, update):
    if bot.fwd_from:
        return
    mone = await bot.edit("Processing ...")
    if update.from_user.id not in Config.AUTH_USERS:
        
        await bot.delete_messages(
            chat_id=update.chat.id,
            message_ids=update.message_id,
            revoke=True
        )
        if bot.reply_to_msg_id:
            start = datetime.now()
            reply_message = await bot.get_reply_message()
            try:
                c_time = time.time()
                downloaded_file_name = await bot.download_media(
                    reply_message,
                    Config.TMP_DOWNLOAD_DIRECTORY,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, mone, c_time, "trying to download")
                    )
                )
            except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Stored the zip to `{}` in {} seconds.".format(downloaded_file_name, ms))    
        return
    TRChatBase(update.from_user.id, update.text, "unzip")
    for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                    try:
                        await bot.send_message(
                            event.chat_id,
                            single_file,
                            caption=f"UnZipped `{caption_rts}`",
                            force_document=force_document,
                            supports_streaming=supports_streaming,
                            allow_cache=False,
                            reply_to=event.message.id,
                            attributes=document_attributes,
                            # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            #     progress(d, t, event, c_time, "trying to upload")
                            # )
                        )
                    except Exception as e:
                        await borg.send_message(
                            event.chat_id,
                            "{} caused `{}`".format(caption_rts, str(e)),
                            reply_to=event.message.id
                        )
                    # some media were having some issues
                    continue
                    os.remove(single_file)
            os.remove(downloaded_file_name)
    # reply_message = update.reply_to_message
    # if ((reply_message is not None) and
    #     (reply_message.document is not None) and
    #     (reply_message.document.file_name.endswith(Translation.UNZIP_SUPPORTED_EXTENSIONS))):
    #     a = await bot.send_message(
    #         chat_id=update.chat.id,
    #         text=Translation.DOWNLOAD_START,
    #         reply_to_message_id=update.message_id
    #     )
    #     c_time = time.time()
    #     try:
    #         await bot.download_media(
    #             message=reply_message,
    #             file_name=saved_file_path,
    #             progress=progress_for_pyrogram,
    #             progress_args=(
    #                 Translation.DOWNLOAD_START,
    #                 a,
    #                 c_time
    #             )
    #         )
    #     except (ValueError) as e:
    #         await bot.edit_message_text(
    #             chat_id=update.chat.id,
    #             text=str(e),
    #             message_id=a.message_id
    #         )
    #     else:
    #         await bot.edit_message_text(
    #             chat_id=update.chat.id,
    #             text=Translation.SAVED_RECVD_DOC_FILE,
    #             message_id=a.message_id
    #         )
    #         extract_dir_path = extracted
    #         if not os.path.isdir(extract_dir_path):
    #             os.makedirs(extract_dir_path)
    #         await bot.edit_message_text(
    #             chat_id=update.chat.id,
    #             text=Translation.EXTRACT_ZIP_INTRO_THREE,
    #             message_id=a.message_id
    #         )
            try:
                with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
                    zip_ref.extractall(extracted)
                filename = sorted(get_lst_of_files(extracted, []))
                # https://stackoverflow.com/a/39629367/4723940
                logger.info(command_to_exec)
                t_response = subprocess.check_output(
                    command_to_exec, stderr=subprocess.STDOUT)
                # https://stackoverflow.com/a/26178369/4723940
            except:
                try:
                    os.remove(saved_file_path)
                    shutil.rmtree(extract_dir_path)
                except:
                    pass
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.EXTRACT_ZIP_ERRS_OCCURED,
                    disable_web_page_preview=True,
                    parse_mode="html",
                    message_id=a.message_id
                )
            else:
                os.remove(saved_file_path)
                inline_keyboard = []
                zip_file_contents = os.listdir(extract_dir_path)
                i = 0
                for current_file in zip_file_contents:
                    cb_string = "ZIP:{}:ZIP".format(str(i))
                    inline_keyboard.append([
                        pyrogram.InlineKeyboardButton(
                            current_file,
                            callback_data=cb_string.encode("UTF-8")
                        )
                    ])
                    i = i + 1
                cb_string = "ZIP:{}:ZIP".format("ALL")
                inline_keyboard.append([
                    pyrogram.InlineKeyboardButton(
                        "Upload All Files",
                        callback_data=cb_string.encode("UTF-8")
                    )
                ])
                cb_string = "ZIP:{}:ZIP".format("NONE")
                inline_keyboard.append([
                    pyrogram.InlineKeyboardButton(
                        "Cancel",
                        callback_data=cb_string.encode("UTF-8")
                    )
                ])
                reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.EXTRACT_ZIP_STEP_TWO,
                    message_id=a.message_id,
                    reply_markup=reply_markup,
                )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.EXTRACT_ZIP_INTRO_ONE,
            reply_to_message_id=update.message_id
        )
