# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 10:39:12 2018

@author: Ivan
"""

from bs4 import BeautifulSoup
import urllib
import json
import csv




def download_icd10_v2016():
    url_base="http://apps.who.int/classifications/icd10/browse/2016/en/"
    url_root_concepts_json=url_base+"JsonGetRootConcepts?useHtml=false"
    url_children_concepts_json=url_base+"JsonGetChildrenConcepts?ConceptId={}&useHtml=false"
    url_concepts_html=url_base+"GetConcept?ConceptId={}"
    root_concepts=urllib.request.urlopen(url_root_concepts_json)
    root_concepts=json.loads(root_concepts.read())
    
    csvfile = open('data.csv','w',newline='',encoding='utf-8')
    writer = csv.writer(csvfile)
    for lv1_concept in root_concepts:    
        lv1_concept_id=lv1_concept['ID']  # 'I'
        lv1_concept_label=lv1_concept['label']
        print(lv1_concept_label)
        lv2_concepts=json.loads(
                    urllib.request.urlopen(
                    url_children_concepts_json
                    .format(lv1_concept_id)
                    ).read()
                    )
        for lv2_concept in lv2_concepts:
            lv2_concept_id=lv2_concept['ID']  #'A00-A09'
            lv2_concept_label=lv2_concept['label']
            print(lv2_concept_label)
            lv3_html=urllib.request.urlopen(
                        url_concepts_html
                        .format(lv2_concept_id)
                        ).read()
            
            #已经提取html
            #下一步：解析html
            bs=BeautifulSoup(lv3_html, "html.parser")
            li=bs.find_all(class_=lambda x:x=='Category1' or x=='Category2')
            rows=[]
            for i in li:
                row=[lv1_concept_id,lv1_concept_label,
                     lv2_concept_id,lv2_concept_label,
                     i.a.attrs['name'],
                     i.span.text.replace('\r','').replace('\n','').replace(' ','')
                        ]
                print('.',end='')
                rows.append(row)
            writer.writerows(rows)
            print('done')
    csvfile.close()
download_icd10_v2016()

'''
    key_first=14
    count=0
    cc=0
    while(count<num):
        cc=0
        site=base_site+str_first.format(key_first)
        resp=urllib.urlopen(site)
        html=resp.read()
        bs=BeautifulSoup(html, "html.parser")
        for tag_img in bs.find_all(name="img"):
            src=tag_img.get("src")
            if src[-7:-4]!="pid":
                continue
            print count,src
            urllib.urlretrieve(src, 'download\\%02d.jpg'%count)
            count+=1
            cc+=1
            if cc>=20:
                break
        
        key_first+=35
        
dpfbing("giraffe",1000)

'''