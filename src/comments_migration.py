import os
import glob
import shutil
import argparse
import json
from collections import defaultdict
from jsonschema import validate


def validate_human_comments(human_comments:str) -> bool:
    human_comments_schema_file = "../assets/templates/human_annotations-schema.json"

    with open(human_comments_schema_file) as schema_file:
        schema_json = json.load(schema_file)
        print(schema_json)  
        json_data = json.loads(human_comments)
        print("-------------")
        print(json_data)
        try:
            validate(instance=json_data, schema=schema_json)
            return True
        except jsonschema.exceptions.ValidationError as ex:
            print(ex)
            return False

'''
extract human annotations from db and returns an array of jsons containing human annotations in assets/templates templates/human_annotations-schema.json json schema

'''
def extract_human_comments_from_db(db_file:str, project:str, commit_id:str):
    f = open(db_file)
    data = json.load(f)
    docs = []
    annotated_dict = {}
    annotated_dict['gitRepoUrl']= project
    annotated_dict['commitId']= commit_id
    annotated_dict['humanFuncDescription']=[]

    for k in data["_default"].keys():
        try:
            full_desc = data["_default"][k]
            #print("full_desc")
            #print(full_desc)
            #docs.append(full_desc)
            filePath = full_desc['File']
            funcName = full_desc['funcName']
            startLine = full_desc['startLine']
            endLine = full_desc['endLine']
            human_desc_arr  = full_desc["humanFuncDescription"]
            for desc_json in human_desc_arr:
                if "description" in desc_json:
                    #print("description")
                    #print(desc_json["description"])
                    desc = desc_json["description"]
                    if desc != "":
                        comment_dict={}
                        comment_dict['filePath']= filePath
                        comment_dict['funcName']= funcName 
                        comment_dict['startLine']= startLine
                        comment_dict['endLine'] = endLine
                        comment_dict['description'] = desc
                        comment_dict['author'] = desc_json['author']
                        comment_dict['authorEmail'] = desc_json['authorEmail']
                        comment_dict['date'] = desc_json['date']
                        comment_json = json.dumps(comment_dict)
                        #print(comment_json)
                        #print("--------")
                        annotated_dict['humanFuncDescription'].append(comment_dict)
                        #print("non empty desc: " + desc)
                    else:
                        2+2
                        #print("NO Desc: "+desc)
                #print("\n\n")
            
        except Exception as  e:
            print("Exception")
            print(e)
            continue
    return annotated_dict


if __name__ == "__main__":
    db_file = "/Users/palani/git/annotations-search/src/ebpf-samples-commented.db"
    project = "ebpf-samples"
    commit_id = "commit_id"
    docs = extract_human_comments_from_db(db_file, project, commit_id)
    #print(docs)
    comment_json = json.dumps(docs)
    out = validate_human_comments(comment_json)
    print(out)