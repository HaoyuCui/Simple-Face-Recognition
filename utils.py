import face_recognition
from sklearn import svm
from sklearn.model_selection import cross_val_score, train_test_split
import pickle
import tqdm
import os
import time

train_dir = os.listdir('gt_db/')
re_generate = False


def generate_file(train_directory):
    _encodings = []
    _names = []
    for person in tqdm.tqdm(train_directory):
        if ".DS_Store" not in person:
            pix = os.listdir('gt_db/' + person)  # 人名类似 s01, s02 etc.

            # 遍历该层级下所有照片
            for person_img in pix:
                if ".DS_Store" not in person_img:
                    # 获取所有面部编码
                    face = face_recognition.load_image_file('gt_db/' + person + "/" + person_img)
                    face_bounding_boxes = face_recognition.face_locations(face, model="cnn")

                    # 可能会出现无法识别/超过一个人的情况
                    if len(face_bounding_boxes) == 1:
                        face_enc = face_recognition.face_encodings(face)[0]
                        # 加入编码
                        _encodings.append(face_enc)
                        _names.append(person)
                    else:
                        print('')
                        print('Warning: ' + person + "/" + person_img + " was skipped and can't be used for training")
    data_file = open('data_list.p', 'wb')
    pickle.dump([_encodings, _names], data_file)
    data_file.close()
    print('data_list.p has been generated in the root')
    return _encodings, _names


def load_params(re_generate):
    if not re_generate:
        file = open('data_list.p', 'rb')
        _lists = pickle.load(file)
        _encodings = _lists[0]
        _names = _lists[1]
    else:
        _encodings, _names = generate_file(train_dir)
    return _encodings, _names


def evaluate(encodings, names):
    # 使用SVC分类器
    X_train, X_test, y_train, y_test = train_test_split(encodings, names, test_size=0.2, random_state=42)

    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    score_test = clf.score(X_test, y_test)
    score_test = round(score_test, 2)
    # print("Test score: {}".format(score_test))

    scores_cv = cross_val_score(clf, encodings, names, cv=5)

    clf_all = svm.SVC(gamma='scale')
    clf_all.fit(encodings, names)
    print("Cross validation scores: {}".format(scores_cv))
    for i in scores_cv:
        round(i, 2)
    return score_test, scores_cv, clf_all


'''
def evaluate(encodings, names):
    clf_all = svm.SVC(kernel='linear')  # 线性核SVM
    scores_cv = cross_val_score(clf_all, encodings, names, cv=5)  # 5折交叉验证
    clf_all.fit(encodings, names)  # 拟合数据集
    print("Cross validation scores: {}".format(scores_cv))
    return scores_cv, clf_all
'''


def test_image(_clf, image_loc='test.jpg'):
    # 载入数据
    _test_image = face_recognition.load_image_file(image_loc)

    start = time.time()
    face_locations = face_recognition.face_locations(_test_image, model="cnn")
    print(str(time.time() - start))
    no = len(face_locations)
    print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    print("Found:")
    names = []
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(_test_image)[i]
        name = _clf.predict([test_image_enc])
        names.append(name[0])
        print(*name)
    return names
