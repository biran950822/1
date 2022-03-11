import requests as rqs
from bs4 import BeautifulSoup as bsp

blocks = {  # texts // str
    'title': '',
    'content': '',
    'input': '',
    'output': '',
    'sample_input': '',
    'sample_output': '',
    'hint': ''
}

def process_textp(content, pkeys: list, name: str): # 題目敘述、輸入說明、輸出說明、提示
    pkeys_id = 0
    for id in [0, 1, 2, 5]:
        i = content[id]
        ok = False
        data = i.find_all(name=name)
        if len(data) != 0:
            for j in data:
                img = j.find(name='img')
                if not (img is None):
                    blocks[pkeys[pkeys_id]] += (f"![image]({img.get('src')})" + '\n\n')
                else:
                    blocks[pkeys[pkeys_id]] += (j.text.strip('#') + '\n\n')
                ok = True
        else:
            blocks[pkeys[pkeys_id]] += i.text.strip('#') + '\n\n'
            ok = True

        if ok:
            pkeys_id += 1

def process_textpre(content, pkeys: list, name: str): # 範例輸入、範例輸出
    pkeys_id = 0
    for i in content:
        ok = False
        text = '```\n'
        for j in i.find_all(name=name):
            text_list = j.text.strip().split('\n')
            for t in text_list:
                text += t.strip() + '\n'
            ok = True

        if ok:
            blocks[pkeys[pkeys_id]] += text + '```\n'
            pkeys_id += 1

def main():
    pid='a752'
    url='https://dandanjudge.fdhs.tyc.edu.tw/ShowProblem?problemid={}'
    response = rqs.get(url.format(pid))
    html = bsp(response.text, 'html.parser')
    content = html.find_all(name='div', attrs={'class', 'problembox'})
    
    process_textp(content, ['content', 'input', 'output', 'hint'], 'p')
    
if __name__ == '__main__':
    main()