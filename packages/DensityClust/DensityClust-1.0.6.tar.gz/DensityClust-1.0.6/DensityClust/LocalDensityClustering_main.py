import os
import numpy as np
import astropy.io.fits as fits
import time
import pandas as pd
from astropy import wcs
from DensityClust.densityCluster_3d import densityCluster_3d, densityCluster_2d
from tabulate import tabulate
import matplotlib.pyplot as plt
# https://stackoverflow.com/questions/16490261/python-pandas-write-dataframe-to-fixed-width-file-to-fwf


def to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)


def save_outcat(outcat_name, outcat):
    """
    # 保存LDC检测的直接结果，即单位为像素
    :param outcat_name: 核表的路径
    :param outcat: 核表数据
    :return:
    """

    outcat_colums = outcat.shape[1]
    pd.DataFrame.to_fwf = to_fwf
    if outcat_colums == 10:
        # 2d result
        table_title = ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2', 'Size1', 'Size2', 'Peak', 'Sum', 'Volume']
        dataframe = pd.DataFrame(outcat, columns=table_title)
        dataframe = dataframe.round({'ID': 0, 'Peak1': 0, 'Peak2': 0, 'Cen1': 3, 'Cen2': 3,
                                     'Size1': 3, 'Size2': 3, 'Peak': 3, 'Sum': 3, 'Volume': 3})
        dataframe.to_csv(outcat_name, sep='\t', index=False)
        # dataframe.to_fwf(detected_outcat_name)
    elif outcat_colums == 13:
        # 3d result
        table_title = ['ID', 'Peak1', 'Peak2', 'Peak3', 'Cen1', 'Cen2', 'Cen3', 'Size1', 'Size2', 'Size3', 'Peak', 'Sum',
                       'Volume']
        dataframe = pd.DataFrame(outcat, columns=table_title)
        dataframe = dataframe.round({'ID': 0, 'Peak1': 0, 'Peak2': 0, 'Peak3': 0, 'Cen1': 3, 'Cen2': 3, 'Cen3': 3,
                                     'Size1': 3, 'Size2': 3, 'Size3': 3, 'Peak': 3, 'Sum': 3, 'Volume': 3})
        dataframe.to_csv(outcat_name, sep='\t', index=False)
        # dataframe.to_fwf(detected_outcat_name)

    elif outcat_colums == 11:
        # fitting 2d data result
        fit_outcat_name = outcat_name
        fit_outcat = outcat
        table_title = ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2', 'Size1', 'Size2', 'theta', 'Peak',
                       'Sum', 'Volume']
        dataframe = pd.DataFrame(fit_outcat, columns=table_title)
        dataframe = dataframe.round(
            {'ID': 0, 'Peak1': 3, 'Peak2': 3, 'Cen1': 3, 'Cen2': 3, 'Size1': 3, 'Size2': 3, 'theta': 3, 'Peak': 3,
             'Sum': 3, 'Volume': 3})
        dataframe.to_csv(fit_outcat_name, sep='\t', index=False)
        # dataframe.to_fwf(fit_outcat_name)
    else:
        print('outcat columns is %d' % outcat_colums)


def get_wcs(data_name):
    """
    得到wcs信息
    :param data_name: fits文件
    :return:
    data_wcs
    """
    data_header = fits.getheader(data_name)
    keys = data_header.keys()
    key = [k for k in keys if k.endswith('4')]
    [data_header.remove(k) for k in key]

    try:
        data_header.remove('VELREF')
    except:
        pass
    data_wcs = wcs.WCS(data_header)

    return data_wcs


def change_pix2word(data_wcs, outcat):
    """
    将算法检测的结果(像素单位)转换到天空坐标系上去
    :param data_wcs: 头文件得到的wcs
    :param outcat: 算法检测核表
    :return:
    outcat_wcs
    ['ID', 'Peak1', 'Peak2', 'Peak3', 'Cen1', 'Cen2', 'Cen3', 'Size1', 'Size2', 'Size3', 'Peak', 'Sum', 'Volume'] -->3d
     ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2',  'Size1', 'Size2', 'Peak', 'Sum', 'Volume']-->2d
    """
    outcat_column = outcat.shape[1]

    if outcat_column == 10:
        # 2d result
        peak1, peak2 = data_wcs.all_pix2world(outcat['Peak1'], outcat['Peak2'], 1)
        clump_Peak = np.column_stack([peak1, peak2])
        cen1, cen2 = data_wcs.all_pix2world(outcat['Cen1'], outcat['Cen2'], 1)
        clump_Cen = np.column_stack([cen1, cen2])
        size1, size2 = np.array([outcat['Size1'] * 30, outcat['Size2'] * 30])
        clustSize = np.column_stack([size1, size2])
        clustPeak, clustSum, clustVolume = np.array([outcat['Peak'], outcat['Sum'], outcat['Volume']])
        id_clumps = []  # MWSIP017.558+00.150+020.17  分别表示：银经：17.558°， 银纬：0.15°，速度：20.17km/s
        for item_l, item_b in zip(cen1, cen2):
            str_l = 'MWSIP' + ('%.03f' % item_l).rjust(7, '0')
            if item_b < 0:
                str_b = '-' + ('%.03f' % abs(item_b)).rjust(6, '0')
            else:
                str_b = '+' + ('%.03f' % abs(item_b)).rjust(6, '0')
            id_clumps.append(str_l + str_b)
        id_clumps = np.array(id_clumps)

    elif outcat_column == 13:
        # 3d result
        peak1, peak2, peak3 = data_wcs.all_pix2world(outcat['Peak1'], outcat['Peak2'], outcat['Peak3'], 1)
        clump_Peak = np.column_stack([peak1, peak2, peak3 / 1000])
        cen1, cen2, cen3 = data_wcs.all_pix2world(outcat['Cen1'], outcat['Cen2'], outcat['Cen3'], 1)
        clump_Cen = np.column_stack([cen1, cen2, cen3 / 1000])
        size1, size2, size3 = np.array([outcat['Size1'] * 30, outcat['Size2'] * 30, outcat['Size3'] * 0.166])
        clustSize = np.column_stack([size1, size2, size3])
        clustPeak, clustSum, clustVolume = np.array([outcat['Peak'], outcat['Sum'], outcat['Volume']])

        id_clumps = []  # G017.558+00.150+020.17  分别表示：银经：17.558°， 银纬：0.15°，速度：20.17km/s
        for item_l, item_b, item_v in zip(cen1, cen2, cen3 / 1000):
            str_l = 'MWISP' + ('%.03f' % item_l).rjust(7, '0')
            if item_b < 0:
                str_b = '-' + ('%.03f' % abs(item_b)).rjust(6, '0')
            else:
                str_b = '+' + ('%.03f' % abs(item_b)).rjust(6, '0')
            if item_v < 0:
                str_v = '-' + ('%.03f' % abs(item_v)).rjust(6, '0')
            else:
                str_v = '+' + ('%.03f' % abs(item_v)).rjust(6, '0')
            id_clumps.append(str_l + str_b + str_v)
        id_clumps = np.array(id_clumps)
    else:
        print('outcat columns is %d' % outcat_column)
        return None

    outcat_wcs = np.column_stack((id_clumps, clump_Peak, clump_Cen, clustSize, clustPeak, clustSum, clustVolume))
    return outcat_wcs


def get_outcat_local(outcat):
    """
    返回局部区域的检测结果：
    原始图为120*120  局部区域为30-->90, 30-->90 左开右闭
    :param outcat:
    :return:
    """
    # outcat = pd.read_csv(txt_name, sep='\t')
    cen1_min = 30
    cen1_max = 90
    cen2_min = 30
    cen2_max = 90
    aa = outcat.loc[outcat['Cen1'] > cen1_min]
    aa = aa.loc[outcat['Cen1'] <= cen1_max]
    aa = aa.loc[outcat['Cen2'] > cen2_min]
    aa = aa.loc[outcat['Cen2'] <= cen2_max]
    return aa


def localDenCluster(data_name, para=None, mask_name=None, outcat_name=None, outcat_wcs_name=None):
    """
    LDC algorithm
    :param data_name: 待检测数据的路径(str)，fits文件
    :param para: 算法参数，dict
        para.rhomin: Minimum density
        para.deltamin: Minimum delta
        para.v_min: Minimum volume
        para.rms: The noise level of the data, used for data truncation calculation
        para.sigma: 密度估计的窗口
    :param mask_name: 掩模数据的保存路径(str)
    :param outcat_name: 基于像素单位的核表保存路径(str)
    :param outcat_wcs_name: 基于wcs的核表保存路径(str)
    :return:
    """
    data_port_dir = data_name.replace('.fits', '')  # 默认保存路径
    if para is None:
        para = {"gradmin": 0.01, "rhomin": 0.8, "deltamin": 4, "v_min": 27, "rms": 0.46, "dc": 0.6, "is_plot": 0}

    data = fits.getdata(data_name)
    data[np.isnan(data)] = 0
    data_ndim = data.ndim
    if data_ndim == 2:
        print("2d")
        outcat, mask, out = densityCluster_2d(data, para)

    elif data_ndim == 3:
        print("3d data")
        t0 = time.time()
        outcat, mask, out = densityCluster_3d(data, para)
        t1 = time.time()
        print('LDC time: %0.2f' % (t1-t0))
    else:
        outcat, mask, out = None, None, None
        print(data.shape)

    if outcat_name is None:
        if not os.path.exists(data_port_dir):
            os.mkdir(data_port_dir)
        outcat_name = os.path.join(data_port_dir, 'LDC_outcat.txt')
    if mask_name is None:
        if not os.path.exists(data_port_dir):
            os.mkdir(data_port_dir)
        mask_name = os.path.join(data_port_dir, 'LDC_mask.fits')
    if outcat_wcs_name is None:
        if not os.path.exists(data_port_dir):
            os.mkdir(data_port_dir)
        outcat_wcs_name = os.path.join(data_port_dir, 'LDC_outcat_wcs.txt')

    if os.path.isfile(mask_name):
        os.remove(mask_name)
        fits.writeto(mask_name, mask)
    else:
        fits.writeto(mask_name, mask)

    save_outcat(outcat_name=outcat_name, outcat=outcat)

    outcat = pd.read_csv(outcat_name, sep='\t')
    data_wcs = get_wcs(data_name)
    outcat_wcs = change_pix2word(data_wcs, outcat)

    save_outcat(outcat_name=outcat_wcs_name, outcat=outcat_wcs)


if __name__ == '__main__':
    pass

