# -*- coding: utf-8 -*-
# version 4
# developed by zk chen
import random
import time
import requests
import re
import json


# 以下的csrftoken和sessionid需要改成自己登录后的cookie中对应的字段！！！！而且脚本需在登录雨课堂状态下使用
# 登录上雨课堂，然后按F12-->选Application-->找到雨课堂的cookies，寻找csrftoken、sessionid、university_id字段，并复制到下面两行即可
csrftoken = ""  # 需改成自己的
sessionid = ""  # 需改成自己的
university_id = "3309"  # 需改成自己的
url_root = "https://uestcedu.yuketang.cn/"  # 按需修改域名 example:https://*****.yuketang.cn/


# 以下字段不用改，下面的代码也不用改动
user_id = ""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=' + csrftoken + '; sessionid=' + sessionid + '; university_id=' + university_id + '; platform_id=3',
    'x-csrftoken': csrftoken,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'university-id': university_id,
    'xtbz': 'cloud'
}

leaf_type = {
    "video": 0,
    "homework": 6,
    "exam": 5,
    "recommend": 3,
    "discussion": 4
}




def get_shuati_ids(course_name, classroom_id, course_sign):
    get_homework_ids = url_root + "mooc-api/v1/lms/learn/course/chapter?cid=" + str(
        classroom_id) + "&term=latest&uv_id=" + university_id + "&sign=" + course_sign
    homework_ids_response = requests.get(url=get_homework_ids, headers=headers)
    homework_json = json.loads(homework_ids_response.text)
    homework_dic = {}
    try:
        for i in homework_json["data"]["course_chapter"]:
            for j in i["section_leaf_list"]:
                if "leaf_list" in j:
                    for z in j["leaf_list"]:
                        if z['leaf_type'] == leaf_type["homework"]:
                            homework_dic[z["id"]] = z["name"]
                else:
                    if j['leaf_type'] == leaf_type["homework"]:
                        # homework_ids.append(j["id"])
                        homework_dic[j["id"]] = j["name"]
        print(course_name + "共有" + str(len(homework_dic)) + "个作业喔！")
        print(homework_dic)
        return homework_dic
    except:
        print("fail while getting homework_ids!!! please re-run this program!")
        raise Exception("fail while getting homework_ids!!! please re-run this program!")

def shuati(classroom_id,sku_id,course_sign,kcid,kcid1,course_name):
    get_ProblemID = url_root + "mooc-api/v1/lms/learn/leaf_info/" + str(classroom_id) + "/" + str(kcid)+"/?sign="+str(course_sign)+"&term=latest&uv_id="+university_id
    tiku_response = requests.get(url=get_ProblemID, headers=headers)
    tiku_json = json.loads(tiku_response.text)
    leaf_type_id = tiku_json["data"]["content_info"]["leaf_type_id"]
    get_exercise_list = url_root + "mooc-api/v1/lms/exercise/get_exercise_list/"+str(leaf_type_id)+ "/" +str(sku_id)+"/?term=latest&uv_id="+university_id
    get_exercise_list_get = requests.get(url=get_exercise_list,headers=headers)
    exercise_list_json = json.loads(get_exercise_list_get.text)

    homework_dic = {}
    for i in exercise_list_json["data"]["problems"]:
        ProblemID = i["content"]["ProblemID"]
        print("==========================================================================")
        print("当前课程：" + course_name + "==>" + "作业题：" + kcid1  + "==>第" + str(i["index"]) +"题;")

        Type_ex = str(i["content"]["Type"]).strip()

        if str(i["user"]["is_show_answer"]).strip() == 'False':
            if Type_ex == "SingleChoice":
                print("题目类型：单选题")
                zuoti(classroom_id,ProblemID)
            if Type_ex == "MultipleChoice":
                print("题目类型：多选题")
                duoxuan(classroom_id, ProblemID)
            else:
                print("当前课程：" + course_name + "==>" + "作业顺序：" + kcid1 + "==>第" + str(i["index"]) + "题;题目类型：" + str(
                    i["content"]["Type"]))
                #print(exercise_list_json)
                time.sleep(5)
                continue
        if str(i["user"]["is_show_answer"]).strip() == 'True':
            print("该题已经提交正确答案！")
            continue
def duoxuan(classroom_id,problem_id):
    for i in range(14):
        if i == 0:
            answer=["C"]
        if i == 1:
            answer=["A"]
        if i == 2:
            answer=["D"]
        if i == 3:
            answer=["B"]
        if i == 4:
            answer = ["A","B"]
        if i == 5:
            answer = ["A","C"]
        if i == 6:
            answer = ["A","D"]
        if i == 7:
            answer = ["B","C"]
        if i == 8:
            answer = ["B", "D"]
        if i == 9:
            answer = ["C", "D"]
        if i == 10:
            answer = ["A", "B", "C"]
        if i == 11:
            answer = ["A", "B", "D"]
        if i == 12:
            answer = ["B", "C", "D"]
        if i == 13:
            answer = ["A", "B", "C", "D"]
        print("当前选择:"+str(answer))
        post = {
            "classroom_id" : classroom_id,
            "problem_id" : problem_id,
            "answer" : answer
        }
        print(post)
        dati_url = url_root + "mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id="+university_id
        try:
            get_result_res = requests.post(url=dati_url, data=json.dumps(post), headers=headers)
            print(get_result_res.text)
            result_res = json.loads(get_result_res.text)
            is_show_answer = str(result_res["data"]["is_show_answer"]).strip()
            print(is_show_answer)
            if(is_show_answer == 'True'):
                print("回答正确")
                time.sleep(3)
                break
            else:
                time.sleep(2)

        except:
            time.sleep(5)
            continue
def zuoti(classroom_id,problem_id):
    for i in range(4):
        if i==0:
            answer=["C"]
        if i==1:
            answer=["A"]
        if i==2:
            answer=["D"]
        if i==3:
            answer=["B"]
        print("当前选择:"+str(answer))

        post = {
            "classroom_id" : classroom_id,
            "problem_id" : problem_id,
            "answer" : answer
        }
        print(post)
        dati_url = url_root + "mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id="+university_id
        try:
            get_result_res = requests.post(url=dati_url, data=json.dumps(post), headers=headers)
            print(get_result_res.text)
            result_res = json.loads(get_result_res.text)
            is_show_answer = str(result_res["data"]["is_show_answer"]).strip()
            if(is_show_answer == 'True'):
                print("回答正确")
                time.sleep(3)
                break
            else:
                time.sleep(2)

        except:
            time.sleep(5)
            continue

if __name__ == "__main__":
    your_courses = []

    # 首先要获取用户的个人ID，即user_id,该值在查询用户的视频进度时需要使用
    user_id_url = url_root + "edu_admin/check_user_session/"
    id_response = requests.get(url=user_id_url, headers=headers)
    try:
        user_id = re.search(r'"user_id":(.+?)}', id_response.text).group(1).strip()
    except:
        print("也许是网路问题，获取不了user_id,请试着重新运行")
        raise Exception("也许是网路问题，获取不了user_id,请试着重新运行!!! please re-run this program!")

    # 然后要获取教室id
    get_classroom_id = url_root + "mooc-api/v1/lms/user/user-courses/?status=1&page=1&no_page=1&term=latest&uv_id=" + university_id + ""
    submit_url = url_root + "mooc-api/v1/lms/exercise/problem_apply/?term=latest&uv_id=" + university_id + ""
    classroom_id_response = requests.get(url=get_classroom_id, headers=headers)
    try:
        for ins in json.loads(classroom_id_response.text)["data"]["product_list"]:
            your_courses.append({
                "course_name": ins["course_name"],
                "classroom_id": ins["classroom_id"],
                "course_sign": ins["course_sign"],
                "sku_id": ins["sku_id"],
                "course_id": ins["course_id"]
            })
    except Exception as e:
        print("fail while getting classroom_id!!! please re-run this program!")
        raise Exception("fail while getting classroom_id!!! please re-run this program!")

    # 显示用户提示
    for index, value in enumerate(your_courses):
        print("编号：" + str(index + 1) + " 课名：" + str(value["course_name"]))
    number = input("你想刷哪门课呢？请输入编号。输入0表示全部课程都刷一遍\n")
    if int(number) == 0:
        # 0 表示全部刷一遍
        for ins in your_courses:
            homework_dic = get_shuati_ids(ins["course_name"], ins["classroom_id"], ins["course_sign"])
            for kcid in homework_dic.items():
                shuati(ins["classroom_id"],ins["sku_id"],ins["course_sign"],kcid[0],kcid[1],ins["course_name"])
    else:
        number = int(number) - 1
        homework_dic = get_shuati_ids(your_courses[number]["course_name"], your_courses[number]["classroom_id"],
                                      your_courses[number]["course_sign"])

        for kcid in homework_dic.items():
            shuati(your_courses[number]["classroom_id"], your_courses[number]["sku_id"], your_courses[number]["course_sign"], kcid[0], kcid[1], your_courses[number]["course_name"])
        # 指定序号的课程刷一遍

    print("所有题已经搞定啦～sir!")
