import aiohttp
import bs4
import pandas as pd
import os
import asyncio
import concurrent.futures
from tqdm import tqdm
from time import time
from multiprocessing import cpu_count, Pool


limit = int(input("Input page number (>1): "))

truyen_title_out = []
truyen_link_out = []
truyen_detail_out = []


async def fetch(session, url, retries=3, delay=0.5):
    for i in range(retries):
        try:
            async with session.get(url, timeout=60) as response:
                content = await response.read()
                decoded_content = content.decode('utf-8', errors='replace')
                return decoded_content
        except asyncio.TimeoutError:
            # print(f"Request to {url} timed out. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)

async def get_truyen_info(url, session, loop):
    html = await fetch(session, url)
    soup = bs4.BeautifulSoup(html, "lxml")
    list_truyen = soup.find('div', class_='list-truyen')

    truyen_titles = [th.text for th in list_truyen.select('h3.truyen-title')]
    truyen_links = [a.get('href') for a in list_truyen.select('a')[::2]]

    truyen_details = await asyncio.gather(*[get_truyen_detail(truyen_url, session) for truyen_url in truyen_links])

    truyen_title_out.extend(truyen_titles)
    truyen_link_out.extend(truyen_links)
    truyen_detail_out.extend(truyen_details)


async def get_truyen_detail(url, session):
    html = await fetch(session, url)
    soup = bs4.BeautifulSoup(html, "lxml")
    list_truyen = soup.find('div', class_='rate')
    truyen_detail = ' '.join(th.text for th in list_truyen.select('div.small')) if list_truyen else 'bug'
    return truyen_detail


async def main():
    async with aiohttp.ClientSession() as session:
        start_time = time()

        for i in range(1, limit+1, 50):
            tasks = [get_truyen_info(f"https://truyenfull.vn/danh-sach/truyen-full/trang-{page_num}", session, asyncio.get_running_loop()) for page_num in range(i, min(i+50, limit+1))]

            with tqdm(total=len(tasks)) as pbar:
                for task in asyncio.as_completed(tasks):
                    await task
                    pbar.update(1)

            if i % 50 == 0:
                print("Delay....")
                await asyncio.sleep(1)

        elapsed_time = time() - start_time
        print(f"Task completed in {elapsed_time:.2f} seconds.")



if __name__ == '__main__':
    asyncio.run(main())

    output_folder = 'output'
    file_name = 'result_' + str(limit) + '_page.xlsx'
    truyen_title_out = [title for i, title in enumerate(truyen_title_out) if i < len(truyen_detail_out)]
    truyen_link_out = [link for i, link in enumerate(truyen_link_out) if i < len(truyen_detail_out)]
    df = pd.DataFrame({'Title': truyen_title_out, 'Link': truyen_link_out, 'Rating_concat': truyen_detail_out})

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with Pool(processes=cpu_count()) as pool:
        pool.apply(df.to_excel, args=(os.path.join(output_folder, file_name),), kwds={'engine': 'xlsxwriter'})