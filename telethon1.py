import time
from telethon import TelegramClient
import asyncio

from myConfig import myapi_id,myapi_hash,myproxy

#-------------------
channel_name='jianhuangfabu'
msg_num=22
#-------------------

filerelativepath = './downloadFile/'
client = TelegramClient('test',myapi_id, myapi_hash,proxy=myproxy)

async def main():
    global filerelativepath
    filecnt_video=filecnt_photo=filecnt_gif=1
    msgs =  await client.get_messages(channel_name,limit=msg_num)
    tasks=[]
    for msg in msgs:
        if msg.media != None:
            if msg.gif != None:
                #print('检测到第{}个{}'.format(filecnt_gif, 'gif'))
                filecnt_gif += 1
                filename = filerelativepath + 'gif/'
            elif msg.photo !=None:
                #print('检测到第{}个{}'.format(filecnt_photo, 'photo'));
                filecnt_photo+=1
                filename = filerelativepath + 'photo/'
            elif msg.video!=None:
                #print('检测到第{}个{}'.format(filecnt_video, 'video'));
                filecnt_video+=1
                filename = filerelativepath+'video/'
            else:
                continue
            tasks.append(asyncio.create_task(client.download_media(message=msg, file=filename)))

    #task创建完成
    print('共检测到视频：{}个，照片：{}个，gif：{}个'.format(filecnt_video,filecnt_photo,filecnt_gif))
    begin_time = time.time()
    print('开始下载：',begin_time)
    for task in tasks:
        await task
    end_time = time.time()
    print('下载结束：',end_time)
    print('用时：{}s'.format(end_time-begin_time))

with client:
    client.loop.run_until_complete(main())

