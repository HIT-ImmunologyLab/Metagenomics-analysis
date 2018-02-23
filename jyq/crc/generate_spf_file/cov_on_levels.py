#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/10/4 10:21
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : cov_on_levels.py
# @Software: PyCharm

"""
Note that this script must run with python3
"""


"""
This part defined some assistant data structure
"""
count = dict()
count2 = dict()
cov = dict()
appear = set()
cov_genus = dict()
cov_familly = dict()
cov_order = dict()
cov_class = dict()
cov_phylum = dict()
genus_species = dict()
familly_genus = dict()
order_familly = dict()
class_order = dict()
phylum_class = dict()


"""
This part built the relationship of cur level and it's sub-level as well as caculate the sum cov of species on per samle
"""
with open("table.csv") as f:
    lines = f.readlines()
    for i in range(1, len(lines)):
        if (lines[i].split(',')[12] != "NA" and lines[i].split(',')[12] != "__Unclassified__"):
            if (lines[i].split(',')[12] not in phylum_class.keys()):
                phylum_class[lines[i].split(',')[12]] = [lines[i].split(',')[13]]
            elif (lines[i].split(',')[13] not in phylum_class[lines[i].split(',')[12]]):
                phylum_class[lines[i].split(',')[12]].append(lines[i].split(',')[13])
        if (lines[i].split(',')[13] != "NA" and lines[i].split(',')[13] != "__Unclassified__"):
            if (lines[i].split(',')[13] not in class_order.keys()):
                class_order[lines[i].split(',')[13]] = [lines[i].split(',')[14]]
            elif (lines[i].split(',')[14] not in class_order[lines[i].split(',')[13]]):
                class_order[lines[i].split(',')[13]].append(lines[i].split(',')[14])
        if (lines[i].split(',')[14] != "NA" and lines[i].split(',')[14] != "__Unclassified__"):
            if (lines[i].split(',')[14] not in order_familly.keys()):
                order_familly[lines[i].split(',')[14]] = [lines[i].split(',')[15]]
            elif (lines[i].split(',')[15] not in order_familly[lines[i].split(',')[14]]):
                order_familly[lines[i].split(',')[14]].append(lines[i].split(',')[15])
        if (lines[i].split(',')[15] != "NA" and lines[i].split(',')[15] != "__Unclassified__"):
            if (lines[i].split(',')[15] not in familly_genus.keys()):
                familly_genus[lines[i].split(',')[15]] = [lines[i].split(',')[16]]
            elif (lines[i].split(',')[16] not in familly_genus[lines[i].split(',')[15]]):
                familly_genus[lines[i].split(',')[15]].append(lines[i].split(',')[16])
        if (lines[i].split(',')[16] != "NA" and lines[i].split(',')[16] != "__Unclassified__"):
            if (lines[i].split(',')[16] not in genus_species.keys()):
                genus_species[lines[i].split(',')[16]] = [lines[i].split(',')[17]]
            elif (lines[i].split(',')[17] not in genus_species[lines[i].split(',')[16]]):
                genus_species[lines[i].split(',')[16]].append(lines[i].split(',')[17])
        if (lines[i].split(',')[17] != "NA" and lines[i].split(',')[17] != "__Unclassified__"):
            if (lines[i].split(',')[17] in appear):
                cov[lines[i].split(',')[17]][:50] = [float(x) + float(y) for x, y in
                                                     zip(cov[lines[i].split(',')[17]][:50], lines[i].split(',')[-50:])]
                count[lines[i].split(',')[17]] += 1
            else:
                appear.add(lines[i].split(',')[17])
                cov[lines[i].split(',')[17]] = [0.0 for i in range(50)]
                cov[lines[i].split(',')[17]][:50] = [float(x) for x in lines[i].split(',')[-50:]]
                count[lines[i].split(',')[17]] = 1

"""
error check
"""
for key in cov.keys():
    if (len(cov[key]) != 50):
        print("WRONG")

"""
caculate the average of species
"""
for key in count.keys():
    cov[key][:50] = [str(float(x) / count[key]) for x in cov[key][:50]]


"""
Caculate cov on other level and write result
"""
for key in genus_species.keys():
    cov_genus[key] = [0.0 for i in range(50)]
for key in genus_species.keys():
    for item in genus_species[key]:
        if (item != "NA" and item != "__Unclassified__"):
            l = [0.0 for i in range(50)]
            for i in range(50):
                # print(item,key)
                l[i] = float(cov[item][i]) + cov_genus[key][i]
            cov_genus[key] = l

for key in familly_genus.keys():
    cov_familly[key] = [0.0 for i in range(50)]
for key in familly_genus.keys():
    for item in familly_genus[key]:
        if (item != "NA" and item != "__Unclassified__"):
            l = [0.0 for i in range(50)]
            for i in range(50):
                # print(key,item)
                l[i] = float(cov_genus[item][i]) + cov_familly[key][i]
            cov_familly[key] = l

for key in order_familly.keys():
    cov_order[key] = [0.0 for i in range(50)]
for key in order_familly.keys():
    for item in order_familly[key]:
        if (item != "NA" and item != "__Unclassified__"):
            l = [0.0 for i in range(50)]
            print(key, item)
            for i in range(50):
                l[i] = float(cov_order[key][i]) + cov_familly[item][i]
            cov_order[key] = l

for key in class_order.keys():
    cov_class[key] = [0.0 for i in range(50)]
for key in class_order.keys():
    for item in class_order[key]:
        if (item != "NA" and item != "__Unclassified__"):
            l = [0.0 for i in range(50)]
            for i in range(50):
                l[i] = float(cov_order[item][i]) + cov_class[key][i]
            cov_class[key] = l

for key in phylum_class.keys():
    cov_phylum[key] = [0.0 for i in range(50)]
for key in phylum_class.keys():
    for item in phylum_class[key]:
        if (item != "NA" and item != "__Unclassified__"):
            l = [0.0 for i in range(50)]
            for i in range(50):
                l[i] = float(cov_phylum[key][i]) + cov_class[item][i]
            cov_phylum[key] = l

header = ["species", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
          "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13", "sample_14",
          "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20", "sample_21", "sample_22",
          "sample_23", "sample_24", "sample_25", "sample_26", "sample_27", "sample_28", "sample_29", "sample_30",
          "sample_31", "sample_32", "sample_33", "sample_34", "sample_35", "sample_36", "sample_37", "sample_38",
          "sample_39", "sample_40", "sample_41", "sample_42", "sample_43", "sample_44", "sample_45", "sample_46",
          "sample_47", "sample_48", "sample_49"]
for key in cov.keys():
    if (len(cov[key]) != 50):
        print("WRONG")

with open("spf_species.txt", "w") as f:
    f.write(('\t').join(header) + '\n')
    for key in cov.keys():
        cov[key] = [str(x) for x in cov[key]]
        f.write(key + '\t' + ('\t').join(cov[key]) + '\n')

header_genus = ["genus", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
                "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13", "sample_14",
                "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20", "sample_21", "sample_22",
                "sample_23", "sample_24", "sample_25", "sample_26", "sample_27", "sample_28", "sample_29", "sample_30",
                "sample_31", "sample_32", "sample_33", "sample_34", "sample_35", "sample_36", "sample_37", "sample_38",
                "sample_39", "sample_40", "sample_41", "sample_42", "sample_43", "sample_44", "sample_45", "sample_46",
                "sample_47", "sample_48", "sample_49"]
for key in cov_genus.keys():
    if (len(cov_genus[key]) != 50):
        print("WRONG")

with open("spf_genus.txt", "w") as f:
    f.write(('\t').join(header_genus) + '\n')
    for key in cov_genus.keys():
        cov_genus[key] = [str(x) for x in cov_genus[key]]
        f.write(key + '\t' + ('\t').join(cov_genus[key]) + '\n')

header_familly = ["familly", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
                  "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13",
                  "sample_14", "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20",
                  "sample_21", "sample_22", "sample_23", "sample_24", "sample_25", "sample_26", "sample_27",
                  "sample_28", "sample_29", "sample_30", "sample_31", "sample_32", "sample_33", "sample_34",
                  "sample_35", "sample_36", "sample_37", "sample_38", "sample_39", "sample_40", "sample_41",
                  "sample_42", "sample_43", "sample_44", "sample_45", "sample_46", "sample_47", "sample_48",
                  "sample_49"]
for key in cov_familly.keys():
    if (len(cov_familly[key]) != 50):
        print("WRONG")

with open("spf_familly.txt", "w") as f:
    f.write(('\t').join(header_familly) + '\n')
    for key in cov_familly.keys():
        cov_familly[key] = [str(x) for x in cov_familly[key]]
        f.write(key + '\t' + ('\t').join(cov_familly[key]) + '\n')

header_order = ["order", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
                "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13", "sample_14",
                "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20", "sample_21", "sample_22",
                "sample_23", "sample_24", "sample_25", "sample_26", "sample_27", "sample_28", "sample_29", "sample_30",
                "sample_31", "sample_32", "sample_33", "sample_34", "sample_35", "sample_36", "sample_37", "sample_38",
                "sample_39", "sample_40", "sample_41", "sample_42", "sample_43", "sample_44", "sample_45", "sample_46",
                "sample_47", "sample_48", "sample_49"]
for key in cov_order.keys():
    if (len(cov_order[key]) != 50):
        print("WRONG")

with open("spf_order.txt", "w") as f:
    f.write(('\t').join(header_order) + '\n')
    for key in cov_order.keys():
        cov_order[key] = [str(x) for x in cov_order[key]]
        f.write(key + '\t' + ('\t').join(cov_order[key]) + '\n')

header_class = ["class", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
                "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13", "sample_14",
                "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20", "sample_21", "sample_22",
                "sample_23", "sample_24", "sample_25", "sample_26", "sample_27", "sample_28", "sample_29", "sample_30",
                "sample_31", "sample_32", "sample_33", "sample_34", "sample_35", "sample_36", "sample_37", "sample_38",
                "sample_39", "sample_40", "sample_41", "sample_42", "sample_43", "sample_44", "sample_45", "sample_46",
                "sample_47", "sample_48", "sample_49"]
for key in cov_class.keys():
    if (len(cov_class[key]) != 50):
        print("WRONG")

with open("spf_class.txt", "w") as f:
    f.write(('\t').join(header_class) + '\n')
    for key in cov_class.keys():
        cov_class[key] = [str(x) for x in cov_class[key]]
        f.write(key + '\t' + ('\t').join(cov_class[key]) + '\n')

header_phylum = ["phylum", "sample_00", "sample_01", "sample_02", "sample_03", "sample_04", "sample_05", "sample_06",
                 "sample_07", "sample_08", "sample_09", "sample_10", "sample_11", "sample_12", "sample_13", "sample_14",
                 "sample_15", "sample_16", "sample_17", "sample_18", "sample_19", "sample_20", "sample_21", "sample_22",
                 "sample_23", "sample_24", "sample_25", "sample_26", "sample_27", "sample_28", "sample_29", "sample_30",
                 "sample_31", "sample_32", "sample_33", "sample_34", "sample_35", "sample_36", "sample_37", "sample_38",
                 "sample_39", "sample_40", "sample_41", "sample_42", "sample_43", "sample_44", "sample_45", "sample_46",
                 "sample_47", "sample_48", "sample_49"]
for key in cov_phylum.keys():
    if (len(cov_phylum[key]) != 50):
        print("WRONG")

with open("spf_phylum.txt", "w") as f:
    f.write(('\t').join(header_phylum) + '\n')
    for key in cov_phylum.keys():
        cov_phylum[key] = [str(x) for x in cov_phylum[key]]
        f.write(key + '\t' + ('\t').join(cov_phylum[key]) + '\n')

