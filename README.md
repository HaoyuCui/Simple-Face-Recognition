# Simple Face Recognition

This is a Simple-Face-Recognition app using Python and the module `face_recognition`

To start with, you only need to:

1. clone this file: `git clone https://github.com/HaoyuCui/Simple-Face-Recognition.git`
2. input the command` cd Simple-Face-Recognition`
3. switch to your virtual environment, and use the command `pip install -r requirements.txt` and the install session will be started automatically
4. the project can be trained by the **[Georgia Tech face database](http://www.anefian.com/research/gt_db.zip)** , download and replace it with 'gt_db' folder
5. to run the app,  use `python UI.py`,choose 'Generate feature file' to generate a pickle encoded file to help train process (this file is already in the repo) manually
6. Tip: This repo is powered by the lib: [face-recognition](https://github.com/ageitgey/face_recognition), the structure looks like this:

    ![img_1](imgs/img_1.png)
7. choose 'Fit model & Evaluate' to train a SVM, you can now select image file to evaluate this model, the accuracy can achieve up to 98.66%
8. The over-all process looks like this:

   ![img_2](imgs/img_2.png)