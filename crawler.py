# coding=utf-8
import os

import bs4
import requests
import six


def get_circles(campuses):
    """
    Get official circles in Ibaraki University from university's website
    :param campuses: Campuses of Ibaraki University
    :return: Dictionary of official circles in Ibaraki University
    """
    # サークル一覧が記載されているHP
    url = 'http://www.ibaraki.ac.jp/collegelife/activity/circle/'

    # サークルリスト
    circles = dict()

    # 茨城大学公式HPよりサークル一覧を取得し、サークルリストに追加
    for campus in campuses:
        # HPのHTML
        html = requests.get(url + campus).content.decode('UTF-8')

        for td in bs4.BeautifulSoup(html, 'html.parser').find_all('td'):
            # サークル名 (小文字に変換している)
            name = td.text.strip().lower()

            if name:
                circles.setdefault(name, {'campuses': list()})
                circles[name]['campuses'].append(campus)
                if td.find('a'):  # サークルのURLがあるとき
                    circles[name]['url'] = td.find('a').get('href')
                elif 'url' not in circles[name]:  # サークルのURLがないとき
                    circles[name]['url'] = ''

    return circles


def make_circle_list(campuses):
    """
    Make list of official circles in Ibaraki University
    :param campuses: Campuses of Ibaraki University
    :return: List of official circles in Ibaraki University
    """
    # 出力内容
    results = dict()

    for campus in ['multi'] + campuses:
        results[campus] = dict()

    # 出力内容を構築
    for name, data in six.iteritems(get_circles(campuses)):
        if len(data['campuses']) == 1:
            results[data['campuses'][0]][name] = data
        else:
            results['multi'][name] = data

    return results


def main():
    """
    Main function
    """
    # キャンパス一覧
    campuses = ['mito', 'hitachi', 'ami']

    # 出力ディレクトリ
    output_dir = 'results'

    # 出力ディレクトリ作成
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # キャンパスごとにTSV形式で出力
    for kind, data in six.iteritems(make_circle_list(campuses)):
        # TSVファイルのファイル名
        tsv_file_name = os.path.join(output_dir, os.extsep.join([kind, 'tsv']))

        with open(tsv_file_name, 'w') as tsv_file:
            tsv_file.write('\t'.join(['サークル名', 'キャンパス', 'URL']) + os.linesep)
            for name, circle in six.iteritems(data):
                # 出力内容
                outputs = [name, ', '.join(circle['campuses']), circle['url']]

                tsv_file.write('\t'.join(outputs) + os.linesep)


if __name__ == '__main__':
    main()
