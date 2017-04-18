import bs4
import os
import requests


def main():
    # キャンパス一覧
    campuses = ['mito', 'hitachi', 'ami']

    # サークルリスト
    # circles[サークル名]['campuses'] : サークルが活動しているキャンパス一覧
    # circles[サークル名]['url'] : サークルのURL
    circles = dict()

    # 茨城大学公式HPよりサークル一覧を取得し、サークルリストに追加
    for campus in campuses:
        for td in bs4.BeautifulSoup(requests.get('http://www.ibaraki.ac.jp/collegelife/activity/circle/' + campus)
                                            .content.decode('UTF-8'), 'html.parser').find_all('td'):
            # サークル名 (小文字に変換している)
            name = td.text.strip().lower()

            if name:
                circles.setdefault(name, {'campuses': list()})
                circles[name]['campuses'].append(campus)
                if td.find('a'):  # サークルのURLがあるとき
                    circles[name]['url'] = td.find('a').get('href')
                elif 'url' not in circles[name]:  # サークルのURLがないとき
                    circles[name]['url'] = ''

    # 出力内容
    # result['multi'] : 複数キャンパスで活動しているサークルリスト
    # result['mito'] : 水戸キャンパスで活動しているサークルリスト
    # result['hitachi'] : 日立キャンパスで活動しているサークルリスト
    # result['ami'] : 阿見キャンパスで活動しているサークルリスト
    results = dict()

    for campus in ['multi'] + campuses:
        results[campus] = dict()

    # 出力内容を構築
    for name, data in circles.items():
        if len(data['campuses']) == 1:
            results[data['campuses'][0]][name] = data
        else:
            results['multi'][name] = data

    # 出力ディレクトリ
    output_dir = 'results'

    # 出力ディレクトリ作成
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # キャンパスごとにTSV形式で出力
    for kind, data in results.items():
        with open(os.path.join(output_dir, os.extsep.join([kind, 'tsv'])), 'w') as tsv_file:
            tsv_file.write('\t'.join(['サークル名', 'キャンパス', 'URL']) + os.linesep)
            for name, circle in data.items():
                tsv_file.write('\t'.join([name, ', '.join(circle['campuses']), circle['url']]) + os.linesep)


if __name__ == '__main__':
    main()
