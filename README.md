# 机器学习笔记

本工程为我的机器学习笔记，用来放置一些机器学习相关代码和实现，相关文字性内容请前往：https://lulaoshi.info/machine-learning/。

### 方法一：本地仓库关联github仓库，适用于首次上传


1.在想要提交的文件夹下或者新建文件夹目录下初始化
git init

2.添加需要上传的文件或代码到本地仓库
git status//红色文件是待添加到本地仓库的文件，绿色表示已添加到本地仓库的文件
git add xxx.txt//添加某个文件到本地仓库
或
git add .//将当前文件夹下所有文件都添加到本地仓库

3.提交到本地仓库
git commit -m "first commit log"//提交并填写提交log

4.将本地仓库关联到github仓库上
git remote add origin git@github com:leiphp/awesome-python3-webapp.git

5.将本地仓库代码和文件提交到github仓库
git push -u origin master//提交到master分支上



### 方法二：先将github仓库clone到本地，再添加并提交

1.新建文件夹，在当前文件夹下运行cmd，clone远程仓库到本地
git clone git@github com:leiphp/awesome-python3-webapp.git

2.将所需要的文件拷贝到文件夹指定目录下，然后依次执行以下命令
git add xxx.txt//添加某个文件到本地仓库
或
git add .//将当前文件夹下所有文件都添加到本地仓库
git commit -m "first commit log"//提交并填写提交log
git push
