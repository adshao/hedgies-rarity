#!/usr/bin/env python


from gettext import find
import json
import os
import csv
from typing import OrderedDict


def parse_json(dir_path):
    print(dir_path)
    files = os.listdir(dir_path)
    l = []
    for file in files:
        if '.' not in file and not file.startswith("_"):
            with open(os.path.join(dir_path, file)) as json_file:
                data = json.load(json_file)
                o = {
                    'id': file,
                }
                for item in data['attributes']:
                    for k,v in item.items():
                        o[k] = v
                    # o[item['trait_type']] = item['value']
                # o["Num"] = len(data['attributes'])
                l.append(o)
    return l


def count_occurrence(l):
    c = {}
    for item in l:
        for k, v in item.items():
            if k == 'id':
                continue
            if k in c:
                if v in c[k]:
                    c[k][v] += 1
                else:
                    c[k][v] = 1
            else:
                c[k] = {v: 1}
    return c


def to_score(o, c):
    score = {}
    for k, v in o.items():
        if k == 'id':
            continue
        score[k] = sum(c[k].values()) / (len(c[k].values())) / c[k][v]
    total_score = sum(score.values())
    score["total"] = total_score
    score["id"] = o["id"]
    # score["num"] = o["Num"]
    return score


def find_key(l, key):
    ids = []
    for item in l:
        for k, v in item.items():
            if v == key:
                ids.append(item['id'])
    return sorted(ids)


def main():
    l = parse_json('./QmYH1S2vsRFUCQDGzEyNwBeFYdEKTp2HVnJhjj4p7Qugit')
    c = count_occurrence(l)
    for k, v in c.items():
        print(k)
        print(v)
        print()

    with open('hedgies.csv', 'w', newline='') as csvfile:
        fieldnames = ['id']
        for k, v in c.items():
            fieldnames.append(k)
        fieldnames.append('total')

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for o in l:
            score = to_score(o, c)
            d = OrderedDict(id=score["id"])
            i = 1
            while i < len(fieldnames):
                k = fieldnames[i]
                if k in score:
                    d[k] = score[k]
                else:
                    d[k] = 0
                i += 1
            d["total"] = score["total"]
            writer.writerow(d)


if __name__ == '__main__':
    main()
