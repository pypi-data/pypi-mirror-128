#!/usr/bin/env python3

import sys

import json


def engine_phrases_to_es_cats(json_lines):
    concats = []
    for json_line in json_lines:
        engine_reply = json.loads(json_line)
        if engine_reply.get('final'):
            concats += engine_reply.get('phrases', '')

    return {'cats': concats}
    # return {'cats': json.dumps(concats)}


def main():
    print(json.dumps(engine_phrases_to_es_cats(sys.stdin)))


if __name__ == '__main__':
    main()
