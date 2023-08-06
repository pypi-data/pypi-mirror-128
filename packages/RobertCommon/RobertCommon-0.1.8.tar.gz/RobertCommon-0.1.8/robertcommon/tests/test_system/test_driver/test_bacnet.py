
from robertcommon.system.driver.bacnet import BacnetDriver

#回调函数
def call_back(info:str):
    print(info)

#测试扫点
def test_scan(dict_config, dict_point):
    nCount = 1
    while nCount > 0:
        dict_point.update(BacnetDriver(dict_config, dict_point).search_points(call_back))
        print(f'scan {len(dict_point)}')
        nCount = nCount - 1

#测试读点
def test_get(dict_config, dict_point):

    bacnet_driver = BacnetDriver(dict_config, dict_point)

    dict_result_get = {}
    for point_name in dict_point.keys():
        dict_result_get.update(bacnet_driver.get_points({point_name:''}))
    print(len(dict_result_get))

def test_scrap(dict_config, dict_point):

    bacnet_driver = BacnetDriver(dict_config, dict_point)

    #轮询全部
    nCount = 20
    while nCount > 0:
        dict_result_scrap = bacnet_driver.get_points()
        print(f'scrap {len(dict_result_scrap)}')
        nCount = nCount - 1

def test_case():
    #配置项
    dict_config = {
                        'address': '192.168.1.42/24:47808',          # bacnet server ip(绑定网卡)
                        'identifier': '555',                  # bacnet server identifier
                        'name': 'BacnetDriver',          # bacnet server name
                        'max_apdu': '1024',                   # bacnet server max apdu
                        'segmentation': 'segmentedBoth',     # bacnet server segmentation
                        'vendor_identifier': '15',            # bacnet server vendor
                        'multi_read':'20',                             # bacnet 批量读取个数
                        'cmd_interval': '0.3',                         # bacnet命令间隔
                        'time_out': '5'                                 # 超时时间
                    }
    #点表
    dict_point = {}

    test_scan(dict_config, dict_point)

    test_scrap(dict_config, dict_point)

    print()

test_case()
