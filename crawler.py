# coding=utf-8
import os

import bs4
import requests
import six


def make_circle_data(circle_data, circle_name, campus, table_cell):
    """
    Make circle data
    :param circle_data: Circle data
    :param circle_name: Circle name
    :param campus: Campus
    :param table_cell: Table cell of HTML
    """
    if circle_name not in circle_data:
        circle_data[circle_name] = {'campuses': list()}

    circle_data[circle_name]['campuses'].append(campus)

    if table_cell.find('a') and table_cell.find('a').get('href'):
        circle_data[circle_name]['url'] = table_cell.find('a').get('href')
    else:
        circle_data[circle_name]['url'] = ''


class CircleList:
    """
    List of official circles in Ibaraki University
    """

    def __init__(self):
        # キャンパス一覧
        self._campuses = ['mito', 'hitachi', 'ami']

        # サークル一覧が記載されているHP
        self._url = 'http://www.ibaraki.ac.jp/collegelife/activity/circle/'

        # サークルリスト
        self._circle_list = {'circle': dict(), 'campus': dict()}

    def get(self):
        """
        Get list of official circles in Ibaraki University
        :return: List of official circles in Ibaraki University
        """
        # 茨城大学公式HPからスクレイピングを行う
        self._scraping()

        # キャンパスごとのサークル情報
        campus_data = self._circle_list['campus']

        for campus in ['multi'] + self._campuses:
            campus_data[campus] = dict()

        # 出力内容を構築
        for name, data in six.iteritems(self._circle_list['circle']):
            if len(data['campuses']) == 1:
                campus_data[data['campuses'][0]][name] = data
            else:
                campus_data['multi'][name] = data

        return campus_data

    def _scraping(self):
        """
        Do scraping to university's website
        """
        for campus in self._campuses:
            # 茨城大学公式HPのHTML
            html = requests.get(self._url + campus).content

            self._add(html, campus)

    def _add(self, html, campus):
        """
        Add official circles in Ibaraki University to list
        :param html: HTML of university's website
        :param campus: Campus of Ibaraki University
        """
        for td in bs4.BeautifulSoup(html, 'html.parser').find_all('td'):
            # サークル名 (小文字に変換している)
            name = td.text.strip().lower()

            if name:
                make_circle_data(self._circle_list['circle'], name, campus, td)


def main():
    """
    Main function
    """
    # 出力ディレクトリ
    output_dir = 'results'

    # 出力ディレクトリ作成
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # キャンパスごとにTSV形式で出力
    for kind, data in six.iteritems(CircleList().get()):
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
