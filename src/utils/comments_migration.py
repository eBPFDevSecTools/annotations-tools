import os
import glob
import shutil
import argparse
import json
from collections import defaultdict
from jsonschema import validate
import git
import comment_validator as validator

'''
Given a repo path and a commit_id checkout the same at repo_dload_path
'''
def clone_checkout_commit(repo_url, git_root, commit_id):
    repo = git.Repo.clone_from(repo_url, git_root, no_checkout=True)
    repo.git.checkout(commit_id)
    return


def get_file_path_relative(orig_path, git_root):
    # using basename function from os
    # module to print file name
    file_name = os.path.basename(orig_path)
    ret_list = list()
    for root, dirs, files in os.walk(git_root):
        if file_name in files:
            rel_path = os.path.relpath(root,git_root)
            ret_list.append(os.path.join(rel_path, file_name))
    return ret_list




'''
extract human annotations from db and returns an array of jsons containing human annotations in assets/templates templates/human_annotations-schema.json json schema

'''
def extract_human_comments_from_db(db_file:str, project:str, commit_id:str, git_root:str):
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
                        relative_file_path_list = get_file_path_relative(filePath, git_root)
                        #comment_dict['filePath']= filePath
                        print("Getting relative path for: "+filePath)
                        if len(relative_file_path_list) == 0:
                            print("Relative Filepath does not exist for:  "+filePath)
                        elif (len(relative_file_path_list) > 1):
                            print("DISAMBIGUATE FILEPATH FOR: "+filePath)
                        print("RELATIVE PATH FOR: "+filePath+ " IS: "+relative_file_path_list[0])
                        comment_dict['filePath']= relative_file_path_list[0]
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
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-s','--git_repo_url',action='store',required=True,
            help='github repo url ending with .git')
    my_parser.add_argument('-c','--commit_id',action='store',required=True,
            help='commit id in github repo to pull snapshot from')
    my_parser.add_argument('-r','--git_repo_root_dir',action='store',required=True,
            help='local folder to pull github repo commit id snapshot into')
    my_parser.add_argument('-o','--output_dir',action='store',required=True,
            help='directory to output annotated db files')
    my_parser.add_argument('-p','--project_name',action='store',required=True,
            help='project name that will be used to create annotated db file')
    my_parser.add_argument('-i','--old_comments_file_name',action='store',required=True,
            help='old annotated db file')
    args = my_parser.parse_args()

    
    #db_file = "/Users/palani/git/annotations-search/src/ebpf-samples-commented.db"
    
    output_dir = args.output_dir
    git_repo_url =  args.git_repo_url
    commit_id = args.commit_id
    git_repo_root = args.git_repo_root_dir
    project_name = args.project_name
    db_file = output_dir +"/"+project_name+".db"
    old_comments_file_name = args.old_comments_file_name
    
    clone_checkout_commit(git_repo_url, git_repo_root, commit_id)

    docs = extract_human_comments_from_db(old_comments_file_name, project_name, commit_id,git_repo_root)
    #print(docs)
    with open(db_file,'w') as fp:
        json.dump(docs,fp)
        fp.close()
    comment_json = json.dumps(docs)
    out = validator.validate_human_comments(comment_json)
    print(out)