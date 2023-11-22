# Simple Face Recognition

This is a Simple-Face-Recognition app using Python and the module `face_recognition`

To start with, you only need to:

1. clone this repository: `git clone https://github.com/HaoyuCui/Simple-Face-Recognition.git`

2. input the command` cd Simple-Face-Recognition`

3. switch to your virtual environment, and use the command `pip install -r requirements.txt` and the install session will be started automatically

4. the project can be trained by the **[Georgia Tech face database](http://www.anefian.com/research/gt_db.zip)** , download and replace it with 'gt_db' folder, after that, your folder's structure should looks like this:

    ```
    gt_db
    ├─ s01
    │    ├─ 01.jpg
    │    ├─ ...
    │    └─ 15.jpg
    ├─ ...
    └─ s50
    ```

    You can replace this with your own dataset, make sure to use names like  `gt_db/name/pics`, more than one image per person is accepted (recommend 1 ~ 5 for each person). 
5. to run the app,  use `python UI.py`,[do not recommend as it is already exists] you can choose 'Generate feature file' to generate a pickle encoded file to help train process (this file is already in the repo) manually, it may take more than 5 minutes

6. Tip: This repo is powered by the lib: [face-recognition](https://github.com/ageitgey/face_recognition), the structure looks like this:

    ![img_1](.github/img_1.png)

7. choose 'Fit model & Evaluate' to train a SVM, you can now select image file to evaluate this model, the accuracy can achieve up to 98.66%

8. The over-all process looks like this:

   ![img_2](.github/img_2.png)

