import re

import requests
import zstandard


def main():
    with zstandard.open('added/j0u_posts_251126_items.txt.zst', 'r') as f:
        boards = {line.split(':')[1] for line in f}
    items = set()
    for board in sorted(boards):
        print('Processing board {}.'.format(board))
        while True:
            try:
                response = requests.get(
                    'https://jjang0u.com/board/list/{}/0?list_size=20000'.format(board),
                    timeout=30
                )
                break
            except Exception:
                print('Retrying.')
        for b, i in re.findall('/board/view/([^/]+)/([0-9]+)', response.text):
            items.add('doc:{}:{}'.format(b, i))
        print('Total items {}.'.format(len(items)))
    with open('doc_ids_20251214.txt', 'w') as f:
        f.write('\n'.join(sorted(items))+'\n')

if __name__ == '__main__':
    main()

