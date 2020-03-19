# --coding:utf-8--

from bilibili_analysis_image import Bilibili_ai


class BilibiliAnalysis:
    def __init__(self, src_dir_path, src_video_path):
        self.src_dir_path = src_dir_path
        self.src_video_path = src_video_path
        self.bilibili_ai = Bilibili_ai()

    @staticmethod
    def get_input_list(data_dict):
        input_list = []
        if isinstance(data_dict, dict):
            for key in data_dict:
                num_str, _ = data_dict[key].split('_')
                input_list.append(int(num_str))
        else:
            for item in data_dict:
                num_str, _ = item[1].split('_')
                input_list.append(int(num_str))

        return input_list

    @staticmethod
    def draw_hist(heights, x_label_name, y_label_name, title_str, image_path, hist_num=10):
        from matplotlib import pyplot
        # 创建直方图
        # 第一个参数为待绘制的定量数据，不同于定性数据，这里并没有事先进行频数统计
        # 第二个参数为划分的区间个数

        pyplot.hist(heights, hist_num)
        pyplot.xlabel(x_label_name)
        pyplot.ylabel(y_label_name)
        pyplot.title(title_str)
        pyplot.show()

        pyplot.savefig(image_path)

    @staticmethod
    def draw_bar(data_array, x_label_name, y_label_name, title_str, image_path, xticks):
        from collections import defaultdict
        from matplotlib import pyplot
        #xticks = ['0', '10', '50', '100', '1000', '2000', ]
        # xticks = []
        # for i in range(0, 10001, 10):
        #     xticks.append(i)
        xticks = [str(i) for i in xticks]
        bar_num = defaultdict(int)
        print(data_array)
        for data in data_array:
            for i in range(1, len(xticks)):
                if int(xticks[i]) > data >= int(xticks[i - 1]):
                    bar_num[xticks[i]] += 1
        xticks = xticks[1:]
        print(bar_num)
        test_array = [bar_num[xtick] for xtick in xticks]
        print(test_array)
        pyplot.bar(xticks, [bar_num[xtick] for xtick in xticks], align='center')

        pyplot.xlabel(x_label_name)
        pyplot.ylabel(y_label_name)
        pyplot.title(title_str)
        pyplot.show()
        pyplot.savefig(image_path)

    def cal_gini(self, data_dict):
        import numpy as np

        if isinstance(data_dict, dict):
            input_list = self.get_input_list(data_dict)
        else:
            input_list = data_dict

        input_cumsum = np.cumsum(sorted(np.append(input_list, 0)))
        input_sum = input_cumsum[-1]
        x_array = np.array(range(0, len(input_cumsum))) / np.float(len(input_cumsum) - 1)
        y_array = input_cumsum / input_sum
        b_area = np.trapz(y_array, x=x_array)
        a_area = 0.5 - b_area
        gini_index = a_area / (a_area + b_area)
        return gini_index

    def get_median(self, data_dict):
        import numpy as np
        if isinstance(data_dict, list):
            input_list = data_dict
        else:
            input_list = self.get_input_list(data_dict)

        return np.median(np.array(input_list))

    @staticmethod
    def t_test(input_1, input_2):
        import numpy as np
        from scipy import stats

        mean_1 = np.mean(input_1)
        mean_2 = np.mean(input_2)
        std_1 = np.std(input_1)
        std_2 = np.std(input_2)
        len_1 = len(input_1)
        len_2 = len(input_2)

        mod_std_1 = np.sqrt(np.float32(len_1) / np.float32(len_1 - 1) * std_1)
        mod_std_2 = np.sqrt(np.float32(len_2) / np.float32(len_2 - 1) * std_2)

        statistics, p_value = stats.ttest_ind_from_stats(mean1=mean_1, mean2=mean_2, std1=mod_std_1,
                                                         std2=mod_std_2, nobs1=len_1, nobs2=len_2)
        return statistics, p_value

    def sep_data(self, data_dict, sep):
        group_1 = []
        group_2 = []

        for key in data_dict:
            num_str, weight_str = data_dict[key].split('_')
            if int(num_str) > sep:
                group_1.append(float(weight_str))
            else:
                group_2.append(float(weight_str))
        return group_1, group_2

    def video_analysis(self, video_id):
        import os
        import pickle
        from collections import defaultdict

        res_root_dict = defaultdict(int)
        res_keyword_dict = defaultdict(int)
        res_weight_dict = defaultdict(int)
        with open(os.path.join(self.src_video_path, video_id + '.pkl'), 'rb') as video_data_file:
            video_data = pickle.load(video_data_file)
            # frame_num = len(video_data)
            for key in video_data:
                try:
                    frame_data = video_data[key]
                    frame_result = frame_data["result"]
                    for result in frame_result:
                        res_root_dict[result["root"]] += 1
                        res_keyword_dict[result["keyword"]] += 1
                        res_root_dict[result["keyword"]] += result["score"]
                except Exception as e:
                    print(e)
                    print(frame_data)
                    continue
        return res_root_dict, res_keyword_dict, res_weight_dict

    def meta_analysis(self, video_id):
        import os
        import pickle

        with open(os.path.join(self.src_dir_path, video_id, video_id + ".pkl"), 'rb') as meta_data_file:
            meta_data = pickle.load(meta_data_file)
            comment_dict, danmu_list, info_dict, user_info, video_info = meta_data
        return comment_dict, danmu_list, info_dict, user_info, video_info

    def comment_analysis(self, comment_dict):
        from jieba.analyse import extract_tags, textrank
        from collections import defaultdict
        if not comment_dict:
            return {}
        comment_keyword_dict = defaultdict(int)
        for comment in comment_dict:
            comment_content = comment["reply_content"]
            reply_like = comment["reply_like"]

            comment_keyword = extract_tags(comment_content, topK=3, withWeight=True, allowPOS=())

            for keyword in comment_keyword:
                comment_keyword_dict[keyword[0]] += 1

            if 'replies' in comment:
                for reply in comment["replies"]:
                    comment_content = reply["reply_content"]

                    comment_keyword = extract_tags(comment_content, topK=3, withWeight=True, allowPOS=())

                    for keyword in comment_keyword:
                        comment_keyword_dict[keyword[0]] += 1
        return comment_keyword_dict

    def danmu_analysis(self, danmu_list):
        from jieba.analyse import extract_tags, textrank
        from collections import defaultdict

        if not danmu_list:
            return {}
        danmu_keyword_dict = defaultdict(int)
        for danmu in danmu_list:
            danmu_content = danmu.split("\t&&&\t")[1]

            danmu_keyword = extract_tags(danmu_content, topK=3, withWeight=True, allowPOS=())

            for keyword in danmu_keyword:
                danmu_keyword_dict[keyword[0]] += 1
        return danmu_keyword_dict

    def extract_video_info(self, info_dict, user_info, video_info):
        from jieba.analyse import extract_tags, textrank
        if not user_info:
            user_info = {
                "name": "NotKnow",
                "level": -1,
                "sex": -1,
                "video_num": -1,
                "face": "",
                "following": -1,
                "follower": -1,
                "total_view": -1,
                "total_like": -1
            }
            print("UserInfo None.")
        if user_info and "official" in user_info:
            user_official = user_info["official"]["role"]
        else:
            user_official = -1
        title_dict = {}
        title_content = video_info["title"]
        title_keyword = extract_tags(title_content, topK=3, withWeight=True, allowPOS=())
        for keyword in title_keyword:
            title_dict[keyword] = 1
        dynamic_dict = {}
        for dynamic_tag in video_info["dynamic"].split():
            dynamic_dict[dynamic_tag.replace("#", "")] = 1
        return {
            "view_num": info_dict["data"]["view"],
            "danmu_num": info_dict["data"]["danmaku"],
            "reply_num": info_dict["data"]["reply"],
            "favorite_num": info_dict["data"]["favorite"],
            "coin_num": info_dict["data"]["coin"],
            "share_num": info_dict["data"]["share"],
            "like_num": info_dict["data"]["like"],
            "dislike_num": info_dict["data"]["dislike"],
            "followee_num": user_info["following"],
            "follower_num": user_info["follower"],
            "total_view_num": user_info["total_view"],
            "total_like_num": user_info["total_like"],
            "user_name": user_info["name"],
            "user_level": user_info["level"],
            "user_sex": user_info["sex"],
            "user_official: ": user_official,
            "user_video_num": user_info["video_num"],
            "user_face": user_info["face"],
            "video_duration": video_info["duration"],
            "video_tag": video_info["tname"],
            "pubtime": video_info["pubdate"],
            "video_title": title_dict,
            "video_dynamic": dynamic_dict,
        }

    def analysis_header(self, video_id, url):
        import os
        import pickle
        from urllib.request import urlretrieve
        from collections import defaultdict
        if not url:
            return {}, {}, {}
        face_data_path = os.path.join(self.src_dir_path, video_id, video_id + "_face.pkl")
        face_root_dict = defaultdict(int)
        face_keyword_dict = defaultdict(int)
        face_weight_dict = defaultdict(int)
        if os.path.exists(face_data_path):
            with open(face_data_path, 'rb') as face_data_file:
                face_data = pickle.load(face_data_file)
                if "result" not in face_data:
                    face_data["result"] = {}
                face_data = face_data['result']
                for result in face_data:
                    face_root_dict[result["root"]] += 1
                    face_keyword_dict[result["keyword"]] += 1
                    face_weight_dict[result["keyword"]] += result["score"]
        else:
            face_img_path = os.path.join(self.src_dir_path, video_id, video_id + "_face.jpg")
            try:
                urlretrieve(url, face_img_path)
                face_data = self.bilibili_ai.baidu_image_path(face_img_path)
            except Exception as e:
                print(e)
                face_data = {}
            if "result" not in face_data:
                face_data["result"] = {}
            with open(face_data_path, 'wb') as face_data_file:
                pickle.dump(face_data, face_data_file)
            face_data = face_data['result']

            for result in face_data:
                face_root_dict[result["root"]] += 1
                face_keyword_dict[result["keyword"]] += 1
                face_weight_dict[result["keyword"]] += result["score"]
        return face_root_dict, face_keyword_dict, face_weight_dict

    def get_keyword_freq(self):
        import os
        from collections import defaultdict

        top_video_key_word = defaultdict(int)
        top_video_key_word_freq = defaultdict(int)
        top_video_key_word_weight = defaultdict(float)

        top_video_root_word = defaultdict(int)
        top_video_root_word_freq = defaultdict(int)

        top_face_key_word = defaultdict(int)
        top_face_key_word_freq = defaultdict(int)
        top_face_key_word_weight = defaultdict(float)

        top_face_root_word = defaultdict(int)
        top_face_root_word_freq = defaultdict(int)

        top_comment_key_word = defaultdict(int)
        top_comment_key_word_freq = defaultdict(int)

        top_danmu_key_word = defaultdict(int)
        top_danmu_key_word_freq = defaultdict(int)

        top_title_key_word = defaultdict(int)
        top_title_key_word_freq = defaultdict(int)

        top_dynamic_key_word = defaultdict(int)
        top_dynamic_key_word_freq = defaultdict(int)
        video_path = self.src_video_path
        video_file_list = os.listdir(video_path)
        for index, video_file_name in enumerate(video_file_list):
            if index % 10 == 0:
                print(index)
            video_id = video_file_name.replace('.pkl', '')
            if not os.path.exists(os.path.join(self.src_dir_path, video_id, video_id + ".pkl")):
                continue
            video_root_dict, video_keyword_dict, video_weight_dict = self.video_analysis(video_id)
            comment_dict, danmu_list, info_dict, user_info, video_info = self.meta_analysis(video_id)
            comment_keyword_dict = self.comment_analysis(comment_dict)
            danmu_keyword_dict = self.danmu_analysis(danmu_list)
            video_info_dict = self.extract_video_info(info_dict, user_info, video_info)
            url = video_info_dict["user_face"]
            face_root_dict, face_keyword_dict, face_weight_dict = self.analysis_header(video_id, url)
            for key in video_root_dict:
                top_video_root_word[key] += 1
                top_video_root_word_freq[key] += video_info_dict["view_num"]

            for key in video_keyword_dict:
                top_video_key_word[key] += 1
                top_video_key_word_freq[key] += video_info_dict["view_num"]
                top_video_key_word_weight[key] += video_weight_dict[key] / video_keyword_dict[key]

            for key in face_root_dict:
                top_face_root_word[key] += 1
                top_face_root_word_freq[key] += video_info_dict["view_num"]

            for key in face_keyword_dict:
                top_face_key_word[key] += 1
                top_face_key_word_freq[key] += video_info_dict["view_num"]
                top_face_key_word_weight[key] += face_weight_dict[key] / face_keyword_dict[key]

            for key in comment_keyword_dict:
                top_comment_key_word[key] += 1
                top_comment_key_word_freq[key] += video_info_dict["view_num"]

            for key in danmu_keyword_dict:
                top_danmu_key_word[key] += 1
                top_danmu_key_word_freq[key] += video_info_dict["view_num"]

            for key in video_info_dict["video_title"]:
                top_title_key_word[key] += 1
                top_title_key_word_freq[key] += video_info_dict["view_num"]

            for key in video_info_dict["video_dynamic"]:
                top_dynamic_key_word[key] += 1
                top_dynamic_key_word_freq[key] += video_info_dict["view_num"]
        res_dict = {
            "top_video_key_word": top_video_key_word,
            "top_video_key_word_freq": top_video_key_word_freq,
            "top_video_key_word_weight": top_video_key_word_weight,
            "top_video_root_word": top_video_root_word,
            "top_video_root_word_freq": top_video_root_word_freq,
            "top_face_key_word": top_face_key_word,
            "top_face_key_word_freq": top_face_key_word_freq,
            "top_face_key_word_weight": top_face_key_word_weight,
            "top_face_root_word": top_face_root_word,
            "top_face_root_word_freq": top_face_root_word_freq,
            "top_comment_key_word": top_comment_key_word,
            "top_comment_key_word_freq": top_comment_key_word_freq,
            "top_danmu_key_word": top_danmu_key_word,
            "top_danmu_key_word_freq": top_danmu_key_word_freq,
            "top_title_key_word": top_title_key_word,
            "top_title_key_word_freq": top_title_key_word_freq,
            "top_dynamic_key_word": top_dynamic_key_word,
            "top_dynamic_key_word_freq": top_dynamic_key_word_freq,
        }

        return res_dict

    def video_feature(self, input_dict):
        import os

        video_path = self.src_video_path
        video_file_list = os.listdir(video_path)
        video_view_list = []
        keyword_video_dict = {}
        for index, video_file_name in enumerate(video_file_list):
            if index % 10 == 0:
                print("Video feature.")
                print(index)
            video_id = video_file_name.replace('.pkl', '')
            if not os.path.exists(os.path.join(self.src_dir_path, video_id, video_id + ".pkl")):
                continue
            video_root_dict, video_keyword_dict, video_weight_dict = self.video_analysis(video_id)
            comment_dict, danmu_list, info_dict, user_info, video_info = self.meta_analysis(video_id)
            video_info_dict = self.extract_video_info(info_dict, user_info, video_info)
            view_num = video_info_dict["view_num"]
            video_view_list.append(view_num)
            for keyword in input_dict:
                if keyword in video_keyword_dict:
                    show_num = video_keyword_dict[keyword]
                    score_num = video_weight_dict[keyword]
                    avg_score = score_num / show_num
                    if keyword in keyword_video_dict:
                        keyword_video_dict[keyword][video_id] = str(view_num) + "_" + str(avg_score)
                    else:
                        keyword_video_dict[keyword] = {video_id: str(view_num) + "_" + str(avg_score)}
                else:
                    if keyword in keyword_video_dict:
                        keyword_video_dict[keyword][video_id] = str(view_num) + "_" + str(0.0)
                    else:
                        keyword_video_dict[keyword] = {video_id: str(view_num) + "_" + str(0.0)}
        return video_view_list, keyword_video_dict

    def video_statistic(self):
        import os

        video_path = self.src_video_path
        video_file_list = os.listdir(video_path)

        result_dict = {
            "view": [],
            "duration": [],
            "comment": [],
            "danmu": [],
            "like": [],
            "favorite": [],
        }

        xtick_dict = {
            "view": [0, 10, 100, 200, 500, 1000, 2000, 10000, 100000, 1000000],
            "duration": [0, 30, 60, 300, 600],
            "comment": [0, 10, 30, 50, 100, 500],
            "danmu": [0, 10, 100, 200, 500, 1000],
            "like": [0, 10, 100, 200, 500, 1000, 2000, 10000],
            "favorite": [0, 10, 100, 200, 500, 1000, 2000, 10000],
        }

        for index, video_file_name in enumerate(video_file_list):
            if index % 10 == 0:
                print(index)
            video_id = video_file_name.replace('.pkl', '')
            if not os.path.exists(os.path.join(self.src_dir_path, video_id, video_id + ".pkl")):
                continue
            _, _, info_dict, user_info, video_info = self.meta_analysis(video_id)
            video_info_dict = self.extract_video_info(info_dict, user_info, video_info)
            result_dict["view"].append(video_info_dict["view_num"])
            result_dict["duration"].append(video_info_dict["video_duration"])
            result_dict["comment"].append(video_info_dict["reply_num"])
            result_dict["danmu"].append(video_info_dict["danmu_num"])
            result_dict["like"].append(video_info_dict["like_num"])
            result_dict["favorite"].append(video_info_dict["favorite_num"])
        res_str = ','.join([str(i) for i in result_dict["view"]])
        for key in result_dict:
            image_path = "./" + key + "_bar.jpg"
            x_label_name = key + " number"
            y_label_name = "video number"
            title_str = key + " statistics"
            hist_num = 10
            print(key)
            print(result_dict[key])
            print(xtick_dict[key])
            # self.draw_hist(result_dict[key], x_label_name, y_label_name, title_str, image_path, hist_num)
            self.draw_bar(result_dict[key], x_label_name, y_label_name, title_str, image_path, xtick_dict[key])


if __name__ == "__main__":
    import sys
    import pickle
    import os

    args = sys.argv
    src_dir_path = args[1]
    src_video_path = args[2]
    dest_file_path = args[3]
    full_dest_file_path = dest_file_path.split(".pkl")[0]+"_full.pkl"

    bilibili_analysis = BilibiliAnalysis(src_dir_path, src_video_path)
    bilibili_analysis.video_statistic()
    if not os.path.exists(dest_file_path):
        res_dict = bilibili_analysis.get_keyword_freq()
        with open(dest_file_path, 'wb') as dest_file:
            pickle.dump(res_dict, dest_file)
    else:
        with open(dest_file_path, 'rb') as dest_file:
            res_dict = pickle.load(dest_file)

    if not os.path.exists(full_dest_file_path):
        video_view_list, keyword_video_dict = bilibili_analysis.video_feature(res_dict["top_video_key_word"])

        median = bilibili_analysis.get_median(video_view_list)
        static_keyword_dict ={}
        for keyword in keyword_video_dict:
            video_dict = keyword_video_dict[keyword]
            gini_index = bilibili_analysis.cal_gini(video_dict)
            group_1, group_2 = bilibili_analysis.sep_data(video_dict, median)
            statistics, p_value = bilibili_analysis.t_test(group_1, group_2)
            temp_key_dict = {
                "gini_index": gini_index,
                "p_value": p_value
            }
            static_keyword_dict[keyword] = temp_key_dict
        with open(full_dest_file_path, 'wb') as dest_file:
            pickle.dump([res_dict, video_view_list, keyword_video_dict, static_keyword_dict], dest_file)
    else:
        with open(full_dest_file_path, 'rb') as dest_file:
            res_dict, video_view_list, keyword_video_dict, static_keyword_dict = pickle.load(dest_file)




