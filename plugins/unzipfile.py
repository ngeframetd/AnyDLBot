""" command: .unzip
coded by @By_Azade
code rewritten my SnapDragon7410
"""

import asyncio
import logging
import os
import shutil
import subprocess
import time
import zipfile
from datetime import datetime
from zipfile import ZipFile

import pyrogram
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import humanbytes, progress_for_pyrogram
# the Strings used for this "thing"
from translation import Translation

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from sample_config import Config


logging.getLogger("pyrogram").setLevel(logging.WARNING)





extracted = Config.DOWNLOAD_LOCATION + "extracted/"
thumb_image_path = Config.DOWNLOAD_LOCATION + "/thumb_image.jpg"
if not os.path.isdir(extracted):
    os.makedirs(extracted)


@pyrogram.Client.on_message(pyrogram.Filters.command(["zipcikar"]))
async def unzip(bot, update):
    if bot.fwd_from:
        return
    mone = await bot.edit_message_text("Processing ...")
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    if bot.reply_to_msg_id:
        start = datetime.now()
        reply_message = await bot.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.DOWNLOAD_LOCATION,
                progress_callback=lambda d, t: asyncio.get_bot_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Stored the zip to `{}` in {} seconds.".format(downloaded_file_name, ms))

        with zipfile.ZipFile(downloaded_file_name, 'r') as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        #filename = filename + "/"
        await bot.edit_message_text("Unzipping now")
        # r=root, d=directories, f = files
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
                    await bot.send_file(
                        bot.chat_id,
                        single_file,
                        caption=f"UnZipped `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=bot.message.id,
                        attributes=document_attributes,
                        # progress_callback=lambda d, t: asyncio.get_bot_loop().create_task(
                        #     progress(d, t, bot, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await bot.send_message(
                        bot.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=bot.message.id
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)







def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst
