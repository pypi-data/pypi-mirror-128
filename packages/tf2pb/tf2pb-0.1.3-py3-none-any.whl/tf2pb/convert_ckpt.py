# -*- coding: utf-8 -*-
'''
    convert_ckpt.py: 将tf bert transformer 等模型ckpt转换pb模型 tf-serving pb和 fastertransformer pb
'''
import os
import tensorflow as tf
import shutil
import tf2pb

#if not fastertransformer , don't advice change
ready_config = {
    "floatx": "float32",  # float16, float32 训练模型(ckpt_filename)的精度,通常需32,如需16 可以通过convert_ckpt_dtype.py 转换16精度之后再转换pb
    "fastertransformer": {
        "use": 0,  # 0 普通模型转换 , 1 启用fastertransormer
        "cuda_version": "11.3",  # 当前支持 10.2, 11.3
        "remove_padding": False,
        "int8_mode": 0,  # 需显卡支持,不建议修改
    }
}

if __name__ == '__main__':

    max_seq_len = 340
    num_labels = 16 * 4 + 1
    bert_dir = r'/data/nlp/pre_models/tf/bert/chinese_L-12_H-768_A-12'

    #normal pb
    freeze_pb_config = {
        "ckpt_filename": r"/home/tk/tk_nlp/script/ner/ner_output/bert/model.ckpt-2704",  # 训练ckpt权重
        "save_pb_file": r"/data/finalmodel/2021/ner_fast/11/bert_ner.pb",
    }
    #serving pb
    freeze_pb_serving_config = {
        'use':False,#默认注释掉保存serving模型
        "ckpt_filename": r"/home/tk/tk_nlp/script/ner/ner_output/bert/model.ckpt-2704",  # 训练ckpt权重
        "save_pb_path_serving": r'/data/finalmodel/2021/ner_fast/11/serving',  # tf_serving 保存模型路径
        'serve_option': {
            'method_name': 'tensorflow/serving/predict',
            'tags': ['serve'],
        }
    }

    if freeze_pb_config['save_pb_file'] and os.path.exists(freeze_pb_config['save_pb_file']):
        os.remove(freeze_pb_config['save_pb_file'])

    if freeze_pb_serving_config['use'] and freeze_pb_serving_config['save_pb_path_serving'] and os.path.exists(freeze_pb_serving_config['save_pb_path_serving']):
        shutil.rmtree(freeze_pb_serving_config['save_pb_path_serving'])


    config_file = os.path.join(bert_dir, 'bert_config.json')
    if not os.path.exists(config_file):
        raise Exception("bert_config does not exist")

    #初始化tf2seq模块
    BertModel_module = tf2pb.get_modeling(ready_config)
    if BertModel_module is None:
        raise Exception('tf2pb get_modeling failed')
    bert_config = BertModel_module.BertConfig.from_json_file(config_file)
    def create_model(bert_config, is_training, input_ids, input_mask, segment_ids, num_labels, use_one_hot_embeddings):
        """Creates a classification model."""
        model = BertModel_module.BertModel(
          config=bert_config,
          is_training=is_training,
          input_ids=input_ids,
          input_mask=input_mask,
          token_type_ids=segment_ids,
          use_one_hot_embeddings=use_one_hot_embeddings)

        output_layer = model.get_pooled_output()
        hidden_size = output_layer.shape[-1].value
        output_weights = tf.get_variable(
          "output_weights", [num_labels, hidden_size],
          dtype="float32",
          initializer=tf.truncated_normal_initializer(stddev=0.02))
        output_bias = tf.get_variable(
          "output_bias", [num_labels],
          dtype="float32",
          initializer=tf.zeros_initializer())
        logits = tf.matmul(output_layer, output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, output_bias)
        probabilities = tf.nn.softmax(logits, axis=-1)
        return probabilities


    def save(is_save_serving):
        def create_network_fn():
            input_ids = tf.placeholder(tf.int32, (None, max_seq_len), 'input_ids')
            input_mask = tf.placeholder(tf.int32, (None, max_seq_len), 'input_mask')
            segment_ids = None
            #这里简单使用分类，具体根据自己需求修改
            probabilities = create_model(bert_config, False, input_ids, input_mask, segment_ids, num_labels, False)
            save_config = {
                "input_tensor": {
                    'input_ids': input_ids,
                    'input_mask': input_mask
                },
                "output_tensor": {
                    "pred_ids": probabilities
                },
            }
            save_config.update(freeze_pb_serving_config if is_save_serving else freeze_pb_config)
            return save_config
        #根据自己的模型进行编写
        if not is_save_serving:
            ret = tf2pb.freeze_pb(create_network_fn)
            print(ret)
            if ret ==0:
                tf2pb.pb_show(freeze_pb_config['save_pb_file'])  # 查看
        else:
            ret = tf2pb.freeze_pb_serving(create_network_fn)
            print(ret)
            if ret ==0:
                tf2pb.pb_serving_show(freeze_pb_serving_config['save_pb_path_serving'],freeze_pb_serving_config['serve_option']['tags'])  # 查看
    #保存正常pb
    save(is_save_serving = False)
    #保存serving格式pb
    if freeze_pb_serving_config['use']:
        save(is_save_serving = True)
