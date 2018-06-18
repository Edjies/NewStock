import logging
import sys
import os
import zipfile
import StockConfig

def __getLogger():
    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger("python.lib")

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日志
    file_handler = logging.FileHandler("test.log")
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)

    # 输出不同级别的log
    # logger.debug('this is debug info')
    # logger.info('this is information')
    # logger.warn('this is warning message')
    # logger.error('this is error message')
    # logger.fatal('this is fatal message, it is same as logger.critical')
    # logger.critical('this is critical message')

    # 2016-10-08 21:59:19,493 INFO    : this is information
    # 2016-10-08 21:59:19,493 WARNING : this is warning message
    # 2016-10-08 21:59:19,493 ERROR   : this is error message
    # 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
    # 2016-10-08 21:59:19,493 CRITICAL: this is critical message

    # 移除一些日志处理器
    logger.removeHandler(file_handler)
    return logger


def get_annotation_data():
    import re
    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'r', encoding='utf-8') as f:
        content = ''.join(f.readlines())
        result = re.findall(r'#+[0-9]{6},', content)
    return [x[1:-1] for x in result]


def zip_dir(source_dir, zip_file):
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      print(pathfile[len(source_dir):])
      zip_file.write(pathfile, arcname=pathfile[len(source_dir):])
    # for dirname in dirnames:
    #   zip_dir(os.path.join(parent, dirname))


def get_phone_data(key):
    phone_data_path = '/storage/emulated/0/Android/com.tdx.AndroidNew/backup/backup.zip'
    pc_data_path = 'D:/new_stock/data'
    if not os.path.exists(pc_data_path):
        os.makedirs(pc_data_path)

    # 1. 将手机数据备份

    # 2. 将备份数据拷贝到电脑

    os.system('adb pull {} {}'.format(phone_data_path, pc_data_path))
    # 3. 解压备份数据
    zip_file = zipfile.ZipFile('D:/new_stock/data/backup.zip')
    zip_file.extractall('D:/new_stock/data')
    zip_file.close()
    os.remove('D:/new_stock/data/backup.zip')
    # 4. 替换文件数据
    file_list = os.listdir(pc_data_path + '/user/user_guest')  # 获取解压后的文件列表
    if '{}.blk'.format(key) in file_list:
        stock_codes = []
        with open('{}/user/user_guest/{}.blk'.format(pc_data_path, key), mode='r') as f:
            for line in f.readlines():
                if not '\n' == line and line != '':
                    stock_codes.append(line.strip('\n')[1:])

        with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'w', encoding='utf-8') as f:
            for line in lines:
                if not line.startswith("#") and not '\n' == line:
                    data = line.strip('\n').split(',')
                    stock_code = data[0]
                    if stock_code in stock_codes:
                        stock_codes.remove(stock_code)
                        f.write(line)
                else:
                    f.write(line)
        return stock_codes
    return []

def data_to_tdx_phone(**kwargs):
    phone_data_path = '/storage/emulated/0/Android/com.tdx.AndroidNew/backup/backup.zip'
    #phone_data_path = '/sdcard/Android/com.tdx.AndroidNew/backup/backup.zip'
    phone_data_dir_path = phone_data_path[:-11]  #'/sdcard/Android/com.tdx.AndroidNew/backup'
    print(phone_data_dir_path)
    pc_data_path = 'D:/new_stock/data'
    if not os.path.exists(pc_data_path):
        os.makedirs(pc_data_path)

    # 1. 将手机数据备份

    # 2. 将备份数据拷贝到电脑
    os.system('adb pull {} {}'.format(phone_data_path, pc_data_path))
    # 3. 解压备份数据
    zip_file = zipfile.ZipFile('D:/new_stock/data/backup.zip')
    zip_file.extractall('D:/new_stock/data')
    zip_file.close()
    os.remove('D:/new_stock/data/backup.zip')
    # 4. 替换文件数据
    file_list = os.listdir(pc_data_path + '/user/user_guest')#获取解压后的文件列表
    print(file_list)
    for key, value in kwargs.items():
        if '{}.blk'.format(key) in file_list:
            print(value)
            with open('{}/user/user_guest/{}.blk'.format(pc_data_path, key), mode='w') as f:
                for code in value:
                    f.write(('1' if code.startswith('6') else '0') + code + '\n')
    # 5. 重新压缩
    zip_file = zipfile.ZipFile('D:\\new_stock\\backup.zip', 'w')
    zip_dir('D:\\new_stock\\data', zip_file)
    zip_file.close()
    # 6. 重新上传
    os.system('adb push {} {}'.format('D:/new_stock/backup.zip', phone_data_dir_path))



if __name__=='__main__':
    #data to phone
    stock_code_list = []
    with open('{}/{}'.format(StockConfig.path_track, '1_sma_track.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code_list.append(data[0])
    print(stock_code_list)
    data_to_tdx_phone(zxg=stock_code_list)


    # phone to pc
    #print(get_phone_data('zxg'))


    # get annotation data
    #data_to_tdx_phone(todo=get_annotation_data())
    #result = get_annotation_data()

