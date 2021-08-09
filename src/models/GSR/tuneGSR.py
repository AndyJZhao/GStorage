import os.path as osp
import sys

sys.path.append((osp.abspath(osp.dirname(__file__)).split('src')[0] + 'src'))
from utils import *

import argparse
import numpy as np

zero_to_one_rough_list = [0, 0.25, 0.5, 0.75, 1.0]
zero_to_half_rough_list = [0, 0.25, 0.5]
small_list = [0, 0.25, 0.5]
fsim_weight_list = [0, 0.25, 0.5, 0.75, 1.0]
p_epoch_list = [100, 0, 5, 10, 20, 50, 100]
zero_to_one_fine_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# rm_cand_ratio = [0, 0.025, 0.05]
# add_cand_ratio = [0, 0.05, 0.1]
# filter_mode_list = [f'Mod_{i}_{j}' for i in rm_cand_ratio for j in add_cand_ratio]
c_conf_dict = {  # 25 x Trials
    'semb': 'dw',
    'fsim_weight': zero_to_one_rough_list,  # 5
    'intra_weight': zero_to_one_rough_list,  # 5
    'fsim_norm': True,
    'stochastic_trainer': False,
    'activation': ['Elu'],
    'p_batch_size': [256],
    'p_schedule_step': [500]
}
fan_out_list = ['1_2', '3_5', '5_10', '10_20', '15_30', '20_40', '30_50']
RoughDict = {
    **c_conf_dict
    ,
    'data_spec_configs': {
        'fan_out': {
            'cora': '20_40',  # 5
            'citeseer': '10_20',  # 5
            'airport': '5_10',  # 2
            'blogcatalog': '15_30',
            'flickr': '15_30',
            'arxiv': '5_10',
        },
        'add_ratio': {
            'cora': zero_to_one_fine_list,  # 5
            'citeseer': zero_to_one_fine_list,  # 5
            'airport': zero_to_one_fine_list,  # 4
            'blogcatalog': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'flickr': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'arxiv': [0.0, 0.1, 0.2, 0.3],
        },
        'rm_ratio': {
            'cora': [0.0],  # 2
            'citeseer': [0.0],
            'airport': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'blogcatalog': [0.0, 0.1, 0.2, 0.3],
            'flickr': [0.0, 0.1, 0.2, 0.3],
            'arxiv': [0.0, 0.05, 0.1],
        },
        'p_epochs': {
            'cora': [10, 20, 30, 40, 50, 100],
            'citeseer': [10, 50, 100, 150, 200],
            'airport': [10, 20, 30, 40, 50, 100],
            'blogcatalog': [1, 2, 3],
            'flickr': [1, 2, 3],
            'arxiv': [1, 2]
        },
    },
}

FineDict = {
    'semb': 'dw',
    'fsim_weight': zero_to_one_fine_list,  # 5
    'intra_weight': zero_to_one_rough_list,  # 5
    'fsim_norm': True,
    'stochastic_trainer': False,
    'activation': ['Elu'],
    'p_schedule_step': [0, 100, 250, 500, 1000],
    'data_spec_configs': {
        'fan_out': {
            'cora': '20_40',
            'citeseer': '1_2',
            'airport': '5_10',
            'blogcatalog': '15_30',
            'flickr': '15_30',
            'arxiv': '5_10',
        },
        'add_ratio': {
            'cora': zero_to_one_fine_list,  # 5
            'citeseer': zero_to_one_fine_list + [1.1, 1.2, 1.3, 1.4, 1.5],  # 5
            'airport': zero_to_one_fine_list + [1.1, 1.2, 1.3, 1.4, 1.5],
            'blogcatalog': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'flickr': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'arxiv': [0.0, 0.1, 0.2, 0.3],
        },
        'p_epochs': {
            'cora': [10, 20, 30, 40, 50, 100],  # 2
            'citeseer': [10, 50, 100, 150, 200, 250, 300],  # 4
            'airport': [10, 20, 30, 40, 50, 100],
            'blogcatalog': [1, 3, 5],
            'flickr': [1, 3, 5],
            'arxiv': [1, 2, 3]
        },
        'rm_ratio': {
            'cora': [0.0],
            'citeseer': [0.0],
            'airport': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'blogcatalog': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'flickr': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'arxiv': [0.0, 0.05, 0.1, 0.2],
        },
        'p_batch_size': {
            'cora': [128, 256, 512],
            'citeseer': [128, 256, 512],
            'airport': [128, 256, 512],
            'blogcatalog': [128, 256, 512],
            'flickr': [128, 256, 512],
            'arxiv': [512, 1024, 2048],
        },
    },
}

EXP_DICT = {
    'RoughTuneGCN': {'gnn_model': 'GCN', **RoughDict},
    'RoughTuneGAT': {'gnn_model': 'GAT', **RoughDict},
    'RoughTuneGraphSage': {'gnn_model': 'GraphSage', **RoughDict},
    'Test': {
        'fsim_weight': zero_to_one_rough_list,  # 5        ,
        'data_spec_configs': {
            'add_ratio': {
                'cora': 0.7,
            }
        },
    }
}


@time_logger
def tune_mgsl():
    from models.GSR import train_GSR, GSRConfig
    model, config, train_func = 'GSR', GSRConfig, train_GSR
    exp_name = 'Test'

    tuner = tuner_from_argparse_args(model, config, train_func, EXP_DICT, exp_name=exp_name)
    tuner.grid_search()
    tuner.summarize()


if __name__ == '__main__':
    tune_mgsl()

# tu -dcora -t1 -eFineTune1 -g0; tu -dcora -t3 -eFineTune1 -g0; tu -dcora -t5 -eFineTune1 -g0; tu -dcora -t10 -eFineTune1 -g0;

# python /home/zja/PyProject/MGSL/src/models/MGSL/sum_results.py
