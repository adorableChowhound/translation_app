# 中日韩自动翻译研究及APP开发

- [环境的配置](##环境的配置)
- [翻译](##翻译)
- [待解决的问题](##待解决的问题)
- [参考资料](##参考资料)

## 环境的配置

Python3.6

## 翻译

翻译部分使用的是fairseq。

best-bleu：中日为28.07，日中为22.89；中韩为25.09，韩中为17.53。

翻译平行语料在https://jbox.sjtu.edu.cn/l/0HRRVp

代码已在CentOS 7.6，macOS做测试。

#### 环境准备

也可以直接使用服务器上的环境（账号密码看8月29号的聊天记录），跳过这个步骤。

```
conda activate tmp
cd test/app
```

也可以在新环境中，所有操作都是在项目的目录（/app）里，安装指令如下：

1. [fairseq](https://github.com/pytorch/fairseq) （一个基于PyTorch的序列建模工具）：

```
cd nmt/tools/fairseq && pip install --editable ./
```

2. [jieba](https://github.com/fxsjy/jieba) （中文分词组件）：

```
pip install jieba
```

3. MeCab（日语分词工具）：

有可能会报错

```
# Linux
pip install mecab-python3
pip install unidic-lite
pip install --no-binary :all: mecab-python3
# macOS
brew install mecab
brew install mecab-ipadic
pip install mecab-python3
```

4. KoNLPy（韩语分词工具）：

```
pip install konlpy
```

5. 下载训练好的模型：

链接:https://pan.baidu.com/s/1RzXN3ey0xXvknYinnzMUVg 提取码:r5r9

把checkpoints文件夹下载到项目的目录（/app）里。

文件特别大，自己想办法下载，或者找我发给你。



#### 如何使用模型翻译

记得返回项目的目录（/app）里运行：

```
python	nmt.py	源语言	目标语言	要翻译的文件
```

例：

输入想要翻译的句子：

```
cat > nmt/raw.txt
```

输入句子后退出。

运行nmt.py进行翻译：

```
python nmt.py jp zh nmt/raw.txt
```

可选语言为三种：zh，jp，ko

翻译的结果存在nmt/result.txt

输出文件查看结果：

```
cat nmt/result.txt
```

所有安装下载运行操作都是在项目的目录（/app）里，跟我的目录结构不一样，软链接没指向正确的路径都有可能会报错。

(这些代码有的时候会莫名报错，如unrecognized arguments，重来一遍可能就好了，也可以来找我)


## 关于app的一些文件
上传的时候有一些问题，导致master branch这个文件夹里出现了很多跟TranslationApp这个文件夹里一样的文件
然后在跑的时候这个文件夹的命名是Translation
为了顺利上传，里面有很多zip文件夹，解压之后应该就是在正确的位置
里面的readme不用管
（主要是很多我不知道怎么删掉orz）

## 待解决的问题

大家有问题可以一起想办法啊

- 翻译模型特别大(大于1G)，暂时没想到比较好的处理方法（pcy）



## 参考资料

1. [使用fairseq从头开始训练一个中英神经机器翻译模型](https://blog.csdn.net/qq_42734797/article/details/112916511)
2. [使用mosesdecoder对机器翻译语料进行处理](https://blog.csdn.net/orangefly0214/article/details/103278612)
