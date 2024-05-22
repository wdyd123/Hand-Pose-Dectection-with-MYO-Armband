import sqlite3
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def extract_data():
    conn = sqlite3.connect('myo.db')
    c = conn.cursor()

    # 提取 EMG 数据
    c.execute('SELECT POD0, POD1, POD2, POD3, POD4, POD5, POD6, POD7 FROM EMG')
    emg_data = c.fetchall()

    # 提取 IMU 数据和标签
    c.execute('SELECT QUAT0, QUAT1, QUAT2, QUAT3, ACC0, ACC1, ACC2, GYRO0, GYRO1, GYRO2, Label FROM IMU')
    imu_data = c.fetchall()

    conn.close()

    # 去掉 IMU 数据开头多余的部分
    imu_data_trimmed = imu_data[len(imu_data) - len(emg_data):]

    # 提取标签
    labels = [data[-1] for data in imu_data_trimmed]

    return emg_data, imu_data_trimmed, labels

def create_dataset(emg_data, imu_data, labels):
    scaler_emg = MinMaxScaler()
    scaler_imu = MinMaxScaler()

    processed_data = []
    for emg_sample, imu_sample, label in zip(emg_data, imu_data, labels):
        emg_data_normalized = scaler_emg.fit_transform(np.array(emg_sample).reshape(-1, 1)).flatten()
        imu_data_normalized = scaler_imu.fit_transform(np.array(imu_sample[:-1]).reshape(-1, 1)).flatten()
        feature = np.concatenate((emg_data_normalized, imu_data_normalized))
        processed_data.append((feature, label))

    # 转换成 TensorFlow 数据集
    dataset = tf.data.Dataset.from_generator(lambda: processed_data, output_types=(tf.float32, tf.int32))
    return dataset

def save_dataset_as_tfrecord(dataset, filename):
    # 创建TFRecord写入器
    with tf.io.TFRecordWriter(filename) as writer:
        # 遍历数据集，将每个样本序列化并写入TFRecord文件
        for feature, label in dataset:
            feature_raw = tf.io.serialize_tensor(feature).numpy()
            example = tf.train.Example(features=tf.train.Features(feature={
                'feature': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature_raw])),
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label.numpy()]))
            }))
            writer.write(example.SerializeToString())

def main():
    emg_data, imu_data, labels = extract_data()
    dataset = create_dataset(emg_data, imu_data, labels)

    # 在这里可以进一步处理数据集，如拆分成训练集和测试集、进行批处理等
    save_dataset_as_tfrecord(dataset, 'dataset.tfrecord')
    # 示例：将数据集打印出来
    for feature, label in dataset:
        print("Feature:", feature.numpy(), "Label:", label.numpy())

if __name__ == '__main__':
    main()
