import random
import time
from robertcommon.system.driver.opcda import OPCDADriver

#
def call_back(info:str):
    print(info)

def test_scan(dict_config, dict_point):
    opcda_driver = OPCDADriver(dict_config, dict_point)
    print(opcda_driver.search_servers())
    return opcda_driver.search_points('*', True)

def test_scrap(dict_config, dict_point):

    opcda_driver = OPCDADriver(dict_config, dict_point)

    while True:
        dict_result_scrap = opcda_driver.get_points()
        print(f"size: {len(dict_result_scrap)} {dict_result_scrap}")
        time.sleep(5)


        dict_result_scrap = opcda_driver.set_points({'Bucket Brigade.Int2': random.randint(1,10)})
        print(dict_result_scrap)

def test_case():
    #配置项
    dict_config = {
                        'server': 'Matrikon.OPC.Simulation.1',          #server
                        'host': '192.168.1.36:8804',                  #'host': '192.168.1.36:8804',
                        'enabled': True,
                        'group': f'opcda{random.randint(10,1000)}',          #
                        'read_limit': 50,
                        'update_rate': 500
                    }
    #点表
    dict_point = test_scan(dict_config, {})
    #dict_point['static_int'] = {'point_writable': True, 'point_name': 'static_int', 'point_tag': 'Bucket Brigade.Int2', 'point_type': '', 'point_description': ''}
    #dict_point['static_time'] = {'point_writable': True, 'point_name': 'static_time', 'point_tag': 'Bucket Brigade.Time', 'point_type': '', 'point_description': ''}
    #dict_point['random_float'] = {'point_writable': True, 'point_name': 'random_float', 'point_tag': 'Random.Real4', 'point_type': '', 'point_description': ''}
    #dict_point['random_str'] = {'point_writable': True, 'point_name': 'random_str', 'point_tag': 'Random.String', 'point_type': '', 'point_description': ''}

    test_scrap(dict_config, dict_point)

    print()

test_case()