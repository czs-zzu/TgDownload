import time
from telethon import TelegramClient, events
import asyncio

from myConfig import myapi_id,myapi_hash,myproxy

#-------------------
channel_name='eggma'
msg_num=2
#-------------------

filerelativepath = './downloadFile/'
client = TelegramClient('test',myapi_id, myapi_hash,proxy=myproxy)

def createTasks(msg,tasks):
    '''
    通过msgs创建异步task
    :param msgs:获取到的消息列表 :TotalList
    :param tasks:待返回的task列表
    :return:返回tasks
    '''


    if msg.media != None:
        if msg.gif != None:
            filename = filerelativepath + 'gif/'
        elif msg.photo !=None:
            filename = filerelativepath + 'photo/'
        elif msg.video!=None:
            filename = filerelativepath+'video/'
        else:
            return tasks#不是上述三种类型的文件不创建task
        tasks.append(asyncio.create_task(client.download_media(message=msg, file=filename)))
    return tasks

async def IwannaDownload():
    global filerelativepath
    msgs =  await client.get_messages(channel_name,limit=msg_num)
    tasks=[]
    for msg in msgs:
        tasks = createTasks(msg, tasks)
    #task创建完成
    begin_time = time.time()
    print('开始下载：',begin_time)
    for task in tasks:
        await task
    end_time = time.time()
    print('下载结束：',end_time)
    print('用时：{}s'.format(end_time-begin_time))

@client.on(events.NewMessage(chats=channel_name))
async def DownloadforChannalUpdate(event):
    media = event.message
    tasks=[]
    if media!=None:
        tasks = createTasks(media,tasks)
        begin_time = time.time()
        print('开始下载：', begin_time)
        for task in tasks:
            await task
        end_time = time.time()
        print('下载结束：', end_time)
        print('用时：{}s'.format(end_time - begin_time))

def main(arg=0):
    if arg==0:
        client.start()
        client.run_until_disconnected()
    else:
        with client:
            client.loop.run_until_complete(IwannaDownload())

if __name__ == '__main__':
    main()

