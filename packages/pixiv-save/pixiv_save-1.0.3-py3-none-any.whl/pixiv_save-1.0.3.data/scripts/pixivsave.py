import argparse
import os
import time
from pixivpy3 import AppPixivAPI
from json import load

def read_config():
    with open('config.json',encoding='utf-8') as json_file:
        config = load(json_file)
    return config

def url_adder(_user_illusts):
    urls = []
    for _ill in _user_illusts['illusts']:
        # 单图和多图的源连接位置不同
        if _ill['page_count']==1:
            urls.append(_ill['meta_single_page']['original_image_url'])
        else:
            for imgs in _ill['meta_pages']:
                urls.append(imgs['image_urls']['original'])
    return urls

def get_user_all_illusts(user_id,refresh_token,path_download='./download',proxy=None,separate = False):
    # 登录
    api = AppPixivAPI(proxies=proxy)
    retry = 0
    max_login_retry = 5
    while True:
        try:
            api.auth(refresh_token=refresh_token)
            break
        except:
            if retry > max_login_retry:
                print('[ERR] 下载失败')
                return None
            retry +=1
            print(f'登录失败,1s后重试...{retry}/{max_login_retry}次')
            time.sleep(1)
    
    # 初始化设置
    offset = 0
    # 获取作者所有图片链接
    img_url_list = []
    user_illusts = api.user_illusts(user_id)
    while True:
    # 添加连接
        img_url_list.extend(url_adder(user_illusts))
        if user_illusts['next_url'] is None:
            break
    # 继续下一组
        offset+=30
        user_illusts = api.user_illusts(user_id=user_id,offset=offset)

    print('添加图片完成,开始下载')
    # 创建下载目录
    user_detial = api.user_detail(user_id)
    folder_name = '{}-{}({})'.format(user_detial['user']['name'],user_detial['user']['account'],user_detial['user']['id'])
    path_download = os.path.join(path_download,folder_name)
    os.mkdir(path_download)

    counter = 0
    total = len(img_url_list)
    for img_url in img_url_list:
        counter+=1
        print('[{}/{}] 开始下载:{}'.format(counter,total,img_url))
        retry = 0
        max_download_retry = 5
        while True:
            try:
                api.download(url=img_url,path=path_download)
                break
            except:
                if retry > max_download_retry:
                    print('[ERR] 下载失败')
                    return None
                retry +=1
                print(f'下载失败,1s后重试...{retry}/{max_download_retry}次')
                time.sleep(1)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--userid',type=int,help='pixiv userid which you want to download pictures from.')
    parser.add_argument('-t','--token',help='your pixiv refresh token.once you run this program,it will be saved in config.json file.you dont need to input it last time.',type=str)
    parser.add_argument('-p','--proxy',help='proxy like 127.0.0.1:7890.once you run this program,it will be saved in config.json file.you dont need to input it last time.',type=str)
    parser.add_argument('-d','--downloadto',help='download path.',type=str)
    parser.add_argument('-s','--separate',action='store_true',help='if make directory for every illusts.')
    parser.add_argument('-c','--config',action='store_true',help='load config.json file')

    args = parser.parse_args()
    if args.config:
        config = read_config()
        user_id = config['user_id']
        token = config['refresh_token']
        proxy = config['proxy']
        downloadto = config['downloadto']
    else:
        if args.userid:
            user_id = args.userid
        if args.token:
            token = args.token
        if args.proxy:
            proxy = {
                'http': f'http://{args.proxy}',
                'https': f'http://{args.proxy}'
            }
        if args.downloadto:
            downloadto = args.downloadto
        if args.separate:
            spereate = args.separate

    print(f'[DEBUG]user_id={user_id},\r\nrefresh_token={token},\r\npath_download={downloadto},\r\nproxy={proxy}')
    # main logic
    get_user_all_illusts(user_id=user_id,refresh_token=token,path_download=downloadto,proxy=proxy)

