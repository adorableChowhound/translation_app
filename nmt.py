import sys
import os
import MeCab
from konlpy.tag import Hannanum

'''
Usage: 
python nmt.py sentence_to_translate src_lang tgt_lang
'''

data_dir = 'nmt/data_processing/'


# 分词
def cut(fpath, lang):
    fp = open(fpath, encoding='utf-8')
    new_fp = open(data_dir + 'norm.seg.txt', 'w', encoding='utf-8')
    # jieba中文分词
    if lang == "zh":
        os.system('python -m jieba -d " " ${data_dir}/norm.txt > ${data_dir}/norm.seg.txt')
    # 日语分词
    if lang == "jp":
        mecab = MeCab.Tagger("-Owakati")
        for line in fp.readlines():
            newline = mecab.parse(str(line))
            new_fp.write(newline)
    # 韩语分词
    if lang == "ko":
        hannanum = Hannanum()
        for line in fp.readlines():
            seg_list = hannanum.morphs(line)
            newline = " ".join(seg_list)
            new_fp.write(newline + "\n")

    fp.close()
    new_fp.close()


# 数据预处理
def data_preprocessing(src, scripts):
    # 定义了后面需要用到的变量、各种脚本的路径
    os.environ['NORM_PUNC'] = scripts + "/tokenizer/normalize-punctuation.perl"
    os.environ['TOKENIZER'] = scripts + "/tokenizer/tokenizer.perl"
    os.environ['TC'] = scripts + "/recaser/truecase.perl"
    os.environ['BPEROOT'] = "nmt/tools/subword-nmt/subword_nmt"

    # 标点符号的标准化 normalize-punctuation
    os.system("perl ${NORM_PUNC} -l ${src} < ${raw_file} > ${data_dir}/norm.txt")
    # 分词 tokenize
    cut(data_dir + "/norm.txt", src)
    os.system("perl ${TOKENIZER} -l ${src} < ${data_dir}/norm.seg.txt > ${data_dir}/norm.seg.tok.txt")
    # 大小写转换处理 truecase
    os.system("perl ${TC} -model ${model_dir}/truecase-model.txt <${data_dir}/norm.seg.tok.txt > ${data_dir}/norm.tok.true.txt")
    # 子词处理 bpe
    os.system("python ${BPEROOT}/apply_bpe.py -c ${model_dir}/bpecode.txt --vocabulary ${model_dir}/voc.txt < ${data_dir}/norm.tok.true.txt > ${data_dir}/norm.tok.true.bpe.txt")


# 主程序入口
def nmt(src_lang, tgt_lang, file_name='nmt/raw.txt'):
    src = src_lang
    tgt = tgt_lang
    lang = ["zh", "jp", "ko"]
    if src not in lang:
        print("Please choose language from zh, jp and ko")
        sys.exit()

    # 定义了后面需要用到的变量、各种脚本的路径
    os.environ['src'] = str(src)
    os.environ['tgt'] = str(tgt)
    os.environ['raw_file'] = str(file_name)
    os.environ['data_dir'] = "nmt/data_processing"
    os.environ['checkpoint_best'] = 'checkpoints/' + str(src) + '2' + str(tgt) + '.pt'
    os.environ['model_dir'] = 'nmt/' + str(src) + '2' + str(tgt)
    scripts = "nmt/tools/mosesdecoder/scripts"
    os.environ['DETC'] = scripts + "/recaser/detruecase.perl"
    os.environ['DETOKENIZER'] = scripts + "/tokenizer/detokenizer.perl"

    data_preprocessing(src, scripts)

    # 交互式解码
    os.system('cat ${data_dir}/norm.tok.true.bpe.txt | fairseq-interactive ${model_dir}/data-bin \
    --path ${checkpoint_best} \
    --remove-bpe > ${data_dir}/result/bestbeam8.txt')
    # 抽取译文
    os.system('grep ^H ${data_dir}/result/bestbeam8.txt | cut -f3- > ${data_dir}/result/predict.tok.true.txt')
    # detruecase
    os.system('perl ${DETC} < ${data_dir}/result/predict.tok.true.txt > ${data_dir}/result/predict.tok.txt')
    # detokenize
    os.system('perl ${DETOKENIZER} -l ${tgt} < ${data_dir}/result/predict.tok.txt > ${data_dir}/result/predict.txt')
    # 翻译结果存入nmt/result.txt
    os.system('cp ${data_dir}/result/predict.txt nmt')
    os.system('mv nmt/predict.txt nmt/result.txt')
    os.system('cat nmt/result.txt')


if __name__ == '__main__':
    nmt(src_lang=sys.argv[1], tgt_lang=sys.argv[2], file_name=sys.argv[3])

