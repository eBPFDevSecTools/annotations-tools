import argparse
import json
import glob
import comment_extractor as extractor
import jsonschema
from jsonschema import validate


def validate_human_comments(human_comments:str) -> bool:
    human_comments_schema_file = "../../assets/templates/human_annotations-schema.json"

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
                    



def extract_and_validate_comments_from_json(file_name,start_pattern,end_pattern):
    comments_list = []
    print("PROCESSING: "+file_name)
    src_file = open(file_name,'r')
    data = src_file.read()
    #print(data)
    #TODO: Try a regular expression insted of multiple split operations
    tokens = data.split(start_pattern)
    #print("TOKENS")
    #print(tokens)
    for token in tokens[1:]:
        #print("TOKEN")
        #print(token)
        comment = token.split(end_pattern)[0]
        #print("COMMENT")
        #print(comment)
        try:
            op_dict = json.loads(comment,strict=False)
            #print(op_dict)
            comments_list.append(op_dict)
        except:
            #print("Error")
            print("Invalid COMMENT")
            print(comment)
    return comments_list


if __name__ == "__main__":
    '''
    
    human_comments="""
    {
    "gitRepoUrl":"https://github.com/vbpf/ebpf-samples",
    "commitId":"e052151f8cf3b3d65bfaade6255318a566457fbb",
    "humanFuncDescription":[
        {
            "filePath":"tail_call.c",
            "description":"This is a callee function location which returns 42",
            "author":"Utkalika Satapathy",
            "authorEmail":"utkalika.satapathy01@gmail.com",
            "date":"14.02.2023",
            "funcName":"callee",
            "startLine":33,
            "endLine":37
        }
    ]

}
"""
    validate_human_comments(human_comments)
    
    exit(0)

'''
    AUTHOR = 'author'
    AUTHOR_NAME = 'authorName'
    AUTHOR_EMAIL = 'authorEmail'
    FILE = 'file'
    EMAIL = 'email'

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-s','--src_dir',action='store',required=True,
            help='directory with source code')
    args = my_parser.parse_args()

    src_dir = args.src_dir

    
    files = []
    files.append(src_dir)

    if extractor.check_if_file_does_not_exist(files)  == True:
        print("Input file does not Exist..Quitting")
        exit(0)
    
    
    for filepath in glob.iglob(src_dir+"/*" , recursive=True):
        fname = filepath.split('/')[-1]
        print("path: "+filepath+" name: "+fname) 
        if filepath.endswith(".c") or filepath.endswith(".h"):
            comments_list= extract_and_validate_comments_from_json(filepath," OPENED COMMENT BEGIN","OPENED COMMENT END")
            #print(comments_list)
