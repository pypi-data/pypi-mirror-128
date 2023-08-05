from skimage import filters
import numpy as np
import time
import matplotlib.pyplot as plt

from DensityClust.kc_coord_3d_new import kc_coord_3d, kc_coord_2d
from DensityClust.dist_xyz import dist_xyz
from DensityClust.get_xx import get_xyz


def densityCluster_3d(data, para):
    """
    根据决策图得到聚类中心和聚类中心个数
    :param data: 3D data
    :param para:
        para.rhomin: Minimum density
        para.deltamin: Minimum delta
        para.v_min: Minimum volume
        para.rms: The noise level of the data, used for data truncation calculation
        para.sigma: Standard deviation of Gaussian filtering
    :return:
        NCLUST: number of clusters
        centInd:  centroid index vector
    """
    # 参数初始化
    gradmin = para["gradmin"]
    rhomin = para["rhomin"]
    deltamin = para["deltamin"]
    v_min = para["v_min"]
    rms = para["rms"]
    sigma = para['sigma']
    is_plot = para['is_plot']
    k = 1  # 第1次计算点的邻域大小
    k2 = np.ceil(deltamin).astype(np.int)   # 第2次计算点的邻域大小
    xx = get_xyz(data)  #    xx: 3D data coordinates  坐标原点是 1

    data_filter = filters.gaussian(data, sigma)
    size_x, size_y, size_z = data.shape
    # rho = data_filter.transpose(0, 2, 1).ravel()
    rho = data_filter.flatten()
    rho_Ind = np.argsort(-rho)
    rho_sorted = rho[rho_Ind]
    maxd = size_x + size_y + size_z
    ND = len(rho)

    delta, IndNearNeigh, Gradient = np.zeros(ND, np.float), np.zeros(ND, np.int), np.zeros(ND, np.float)
    delta[rho_Ind[0]] = np.sqrt(size_x ** 2 + size_y ** 2 + size_z ** 2)

    # delta 记录距离，
    # IndNearNeigh
    # 记录：两个密度点的联系 % index of nearest neighbor with higher density
    IndNearNeigh[rho_Ind[0]] = rho_Ind[0]
    t0_ = time.time()
    # 计算 delta, Gradient
    for ii in range(1, ND):
        # 密度降序排序后，即密度第ii大的索引（在rho中）
        # t0 = time.time()
        ordrho_ii = rho_Ind[ii]
        rho_ii = rho_sorted[ii] #第ii大的密度值
        ss = 'litte'
        if rho_ii >= rms:
            delta[ordrho_ii] = maxd
            point_ii_xy = xx[ordrho_ii, :]
            get_value = True  # 判断是否需要在大循环中继续执行，默认需要，一旦在小循环中赋值成功，就不在大循环中运行
            idex, bt = kc_coord_3d(point_ii_xy, size_z, size_y, size_x, k)
            for item_ord, item in zip(idex, bt):
                ordrho_jj = item_ord
                rho_jj = rho[ordrho_jj]  # 根据索引在rho里面取值
                dist_i_j = np.sqrt(((point_ii_xy - item) ** 2).sum())  # 计算两点间的距离
                if dist_i_j <= delta[ordrho_ii]:
                    gradient = (rho_jj - rho_ii) / dist_i_j
                    if gradient >= Gradient[ordrho_ii]:
                        delta[ordrho_ii] = dist_i_j
                        Gradient[ordrho_ii] = gradient
                        IndNearNeigh[ordrho_ii] = ordrho_jj
                        get_value = False

            if get_value:# 表明，在(2 * k + 1) * (2 * k + 1) * (2 * k + 1)的领域中没有找到比该点高，距离最近的点，则在更大的邻域中搜索
                idex, bt = kc_coord_3d(point_ii_xy, size_z, size_y, size_x, k2)
                for item_ord, item in zip(idex, bt):
                    ordrho_jj = item_ord
                    rho_jj = rho[ordrho_jj]  # 根据索引在rho里面取值
                    dist_i_j = np.sqrt(((point_ii_xy - item) ** 2).sum())  # 计算两点间的距离
                    if dist_i_j <= delta[ordrho_ii]:
                        gradient = (rho_jj - rho_ii) / dist_i_j
                        if gradient >= Gradient[ordrho_ii]:
                            delta[ordrho_ii] = dist_i_j
                            Gradient[ordrho_ii] = gradient
                            IndNearNeigh[ordrho_ii] = ordrho_jj
                            get_value = False
            if get_value:
                delta[ordrho_ii] = k2 + 0.0001
                Gradient[ordrho_ii] = -1
                IndNearNeigh[ordrho_ii] = ND
        else:
            IndNearNeigh[ordrho_ii] = ND
        # t1 = time.time()
        # print('%s Elapsed time is %.8f m seconds.\n' % (ss, t1 - t0)*1000)
    delta_sorted = np.sort(-delta) * (-1)
    delta[rho_Ind[0]] = delta_sorted[1]
    t1_ = time.time()
    print('delata, rho and Gradient are calculated, using %.2f seconds' % (t1_-t0_))

    # 根据密度和距离来确定类中心
    NCLUST = 0
    clustInd = -1 * np.ones(ND + 1)
    clust_index = np.intersect1d(np.where(rho > rhomin), np.where(delta > deltamin))

    clust_num = clust_index.shape[0]

    # icl是用来记录第i个类中心在xx中的索引值
    icl = np.zeros(clust_num, dtype=int)
    for ii in range(0, clust_num):
        i = clust_index[ii]
        icl[NCLUST] = i
        NCLUST += 1
        clustInd[i] = NCLUST
    # assignation
    # 将其他非类中心分配到离它最近的类中心中去
    # clustInd = -1
    # 表示该点不是类的中心点，属于其他点，等待被分配到某个类中去
    # 类的中心点的梯度Gradient被指定为 - 1
    # if is_plot == 1:
    #     pass
    for i in range(ND):
        ordrho_i = rho_Ind[i]
        if clustInd[ordrho_i] == -1:    # not centroid
            clustInd[ordrho_i] = clustInd[IndNearNeigh[ordrho_i]]
        else:
            Gradient[ordrho_i] = -1  #将类中心点的梯度设置为-1

    clustVolume = np.zeros(NCLUST)
    for i in range(0, NCLUST):
        clustVolume[i] = clustInd.tolist().count(i + 1)

    # % centInd [类中心点在xx坐标下的索引值，
    # 类中心在centInd的索引值: 代表类别编号]
    centInd = []
    for i, item in enumerate(clustVolume):
        if item >= v_min:
            centInd.append([icl[i], i])
    centInd = np.array(centInd, np.int)

    mask_grad = np.where(Gradient > gradmin)[0]

    # 通过梯度确定边界后，还需要进一步利用最小体积来排除假核
    clustInd_re = -1 * np.ones(ND + 1)   # % 保存最后确定下来的云核的坐标索引
    centInd_re = []  # 保存经过最小体积排出后的类中心信息
    for i, item in enumerate(centInd):
        rho_clust_i = np.zeros(ND)
        # centInd[i, 1] --> item[1] 表示第i个类中心的编号
        index_clust_i = np.where(clustInd == (item[1] + 1))[0]
        index_cc = np.intersect1d(mask_grad, index_clust_i)
        rho_clust_i[index_clust_i] = rho[index_clust_i]
        rho_cc_mean = rho[index_cc].mean() * 0.2
        index_cc_rho = np.where(rho_clust_i > rho_cc_mean)[0]
        index_clust_rho = np.union1d(index_cc, index_cc_rho)
        if len(index_clust_rho) > v_min:
            clustInd_re[index_clust_rho] = i + 1
            centInd_re.append([item[0], i])

    # NCLUST_ = centInd_re.shape[0]
    centInd_re = np.array(centInd_re, np.int)
    return centInd_re, clustInd_re


def get_rho_delta(Gradient, delta, IndNearNeigh, rho_Ind, rho_sorted, rho, rms, maxd, size_x, size_y, size_z, xx, ND):
    # delta 记录距离，
    # IndNearNeigh
    # 记录：两个密度点的联系 % index of nearest neighbor with higher density


    # 计算 delta, Gradient
    for ii in range(1, ND):
        # 密度降序排序后，即密度第ii大的索引（在rho中）
        ordrho_ii = rho_Ind[ii]
        rho_ii = rho_sorted[ii]  # 第ii大的密度值
        if rho_ii >= rms:
            delta[ordrho_ii] = maxd
            point_ii_xy = xx[ordrho_ii, :]
            get_value = True  # 判断是否需要在大循环中继续执行，默认需要，一旦在小循环中赋值成功，就不在大循环中运行
            idex, bt = kc_coord_3d(point_ii_xy, size_z, size_y, size_x, k)
            for item_ord, item in zip(idex, bt):
                ordrho_jj = item_ord

                # ordrho_jj_ = (item[2] - 1) * size_y * size_z + (item[1] - 1) * size_z + item[0]
                # rho_jj_ = data_filter[item[2] - 1, item[1] - 1, item[0] - 1]  #根据坐标在data cube中取值
                rho_jj = rho[ordrho_jj]  # 根据索引在rho里面取值
                # print(rho_jj, rho_jj_)
                # print(ordrho_jj-1, ordrho_jj_)
                dist_i_j = np.sqrt(((point_ii_xy - item) ** 2).sum())  # 计算两点间的距离

                if dist_i_j <= delta[ordrho_ii]:
                    gradient = (rho_jj - rho_ii) / dist_i_j

                    if gradient >= Gradient[ordrho_ii]:
                        delta[ordrho_ii] = dist_i_j
                        Gradient[ordrho_ii] = gradient
                        # IndNearNeigh[ordrho_ii] = (item[2] - 1) * size_y * size_z + (item[1] - 1) * size_z + item[0]
                        IndNearNeigh[ordrho_ii] = ordrho_jj
                        get_value = False
            # for j_ in range(0, bt.shape[0]):
            #     rho_jj = data_filter[bt[j_, 2]-1, bt[j_, 1]-1, bt[j_, 0]-1]
            #     dist_i_j = dist_xyz(delta_ii_xy, bt[j_, :])
            #     gradient = (rho_jj - rho_ii) / dist_i_j
            #     # 通过距离和梯度值的控制可以实现
            #     # 找到“比当前点强度大的点”中最近的点
            #     if dist_i_j <= delta[ordrho_ii] and gradient >= Gradient[ordrho_ii]:
            #         delta[ordrho_ii] = dist_i_j
            #         Gradient[ordrho_ii] = gradient
            #         IndNearNeigh[ordrho_ii] = (bt[j_, 2] - 1) * size_x * size_y + (bt[j_, 1] - 1) * size_x + bt[j_, 0]

            if get_value:
                #  表明，在(2 * k + 1) * (2 * k + 1) * (2 * k + 1)
                # 的领域中没有找到比该点高，距离最近的点，则进行全局搜索
                for jj in range(0, ii, 1):
                    # rho_jj = rho_sorted[jj]
                    ordrho_jj = rho_Ind[jj]
                    point_jj_xy = xx[ordrho_jj, :]

                    dist_i_j = np.sqrt(((point_ii_xy - point_jj_xy) ** 2).sum())
                    gradient = (rho_sorted[jj] - rho_ii) / dist_i_j
                    if dist_i_j <= delta[ordrho_ii]:
                        delta[ordrho_ii] = dist_i_j
                        Gradient[ordrho_ii] = gradient
                        IndNearNeigh[ordrho_ii] = ordrho_jj
        else:
            IndNearNeigh[ordrho_ii] = ND


def densityCluster_3d_multithreading(data, para):
    """
    根据决策图得到聚类中心和聚类中心个数
    :param data: 3D data
    :param para:
        para.rhomin: Minimum density
        para.deltamin: Minimum delta
        para.v_min: Minimum volume
        para.rms: The noise level of the data, used for data truncation calculation
        para.sigma: Standard deviation of Gaussian filtering

    :return:
        NCLUST: number of clusters
        centInd:  centroid index vector
    """
    # 参数初始化
    gradmin = para["gradmin"]
    rhomin = para["rhomin"]
    deltamin = para["deltamin"]
    v_min = para["v_min"]
    rms = para["rms"]
    sigma = para['sigma']
    is_plot = para['is_plot']
    k = 2 # 计算点的邻域大小
    xx = get_xyz(data)  # xx: 3D data coordinates  坐标原点是 1

    data_filter = filters.gaussian(data, sigma)
    size_x, size_y, size_z = data.shape
    # rho = data_filter.transpose(0, 2, 1).ravel()
    rho = data_filter.flatten()
    rho_Ind = np.argsort(-rho)
    rho_sorted = rho[rho_Ind]
    maxd = size_x + size_y + size_z
    ND = len(rho)

    delta, IndNearNeigh, Gradient = np.zeros(ND, np.float), np.zeros(ND, np.int), np.zeros(ND, np.float)
    delta[rho_Ind[0]] = np.sqrt(size_x ** 2 + size_y ** 2 + size_z ** 2)
    IndNearNeigh[rho_Ind[0]] = rho_Ind[0]
    t0 = time.time()
    get_rho_delta(Gradient, delta, IndNearNeigh, rho_Ind, rho_sorted, rho, rms, maxd, size_x, size_y, size_z, xx, ND)
    delta_sorted = np.sort(-delta) * -1
    delta[rho_Ind[0]] = delta_sorted[1]
    t1 = time.time()
    print('delata, rho and Gradient are calculated, using %.2f seconds' % (t1-t0))

    # 根据密度和距离来确定类中心
    NCLUST = 0
    clustInd = -1 * np.ones(ND + 1)
    clust_index = np.intersect1d(np.where(rho > rhomin), np.where(delta > deltamin))

    clust_num = clust_index.shape[0]

    # icl是用来记录第i个类中心在xx中的索引值
    icl = np.zeros(clust_num, dtype=int)
    for ii in range(0, clust_num):
        i = clust_index[ii]
        icl[NCLUST] = i
        NCLUST += 1
        clustInd[i] = NCLUST

    # assignation
    # 将其他非类中心分配到离它最近的类中心中去
    # clustInd = -1
    # 表示该点不是类的中心点，属于其他点，等待被分配到某个类中去
    # 类的中心点的梯度Gradient被指定为 - 1
    if is_plot == 1:
        delta = delta / max(delta[:])
        # figure
    for i in range(0, ND):
        ordrho_i = rho_Ind[i]
        if clustInd[ordrho_i] == -1:# not centroid
            clustInd[ordrho_i] = clustInd[IndNearNeigh[ordrho_i]]
        else:
            Gradient[ordrho_i] = -1  #将类中心点的梯度设置为-1

    clustVolume = np.zeros(NCLUST)
    for i in range(0, NCLUST):
        clustVolume[i] = clustInd.tolist().count(i + 1)

    # % centInd [类中心点在xx坐标下的索引值，
    # 类中心在centInd的索引值: 代表类别编号]
    centInd = []
    for i, item in enumerate(clustVolume):
        if item >= v_min:
            centInd.append([icl[i], i])
    centInd = np.array(centInd, np.int)

    mask_grad = np.where(Gradient > gradmin)[0]

    # 通过梯度确定边界后，还需要进一步利用最小体积来排除假核
    clustInd_re = -1 * np.ones(ND + 1)   # % 保存最后确定下来的云核的坐标索引
    centInd_re = []  # 保存经过最小体积排出后的类中心信息
    for i, item in enumerate(centInd):
        rho_clust_i = np.zeros(ND)
        # centInd[i, 1] --> item[1] 表示第i个类中心的编号
        index_clust_i = np.where(clustInd == (item[1] + 1))[0]
        index_cc = np.intersect1d(mask_grad, index_clust_i)
        rho_clust_i[index_clust_i] = rho[index_clust_i]
        rho_cc_mean = rho[index_cc].mean() * 0.2
        index_cc_rho = np.where(rho_clust_i > rho_cc_mean)[0]
        index_clust_rho = np.union1d(index_cc, index_cc_rho)
        if len(index_clust_rho) > v_min:
            clustInd_re[index_clust_rho] = i + 1
            centInd_re.append(item)

    # NCLUST_ = centInd_re.shape[0]
    centInd_re = np.array(centInd_re, np.int)
    return centInd_re, clustInd_re


def densityCluster_2d(data, para):
    """
    根据决策图得到聚类中心和聚类中心个数
    :param data: 2D data
    :param para:
        para.rhomin: Minimum density
        para.deltamin: Minimum delta
        para.v_min: Minimum volume
        para.rms: The noise level of the data, used for data truncation calculation
        para.sigma: Standard deviation of Gaussian filtering

    :return:
        NCLUST: number of clusters
        centInd:  centroid index vector
    """
    # 参数初始化
    gradmin = para["gradmin"]
    rhomin = para["rhomin"]
    deltamin = para["deltamin"]
    v_min = para["v_min"]
    rms = para["rms"]
    sigma = para['sigma']
    is_plot = para['is_plot']
    k = 1   # 计算点的邻域大小
    xx = get_xyz(data)  # xx: 2D data coordinates  坐标原点是 1

    data_filter = filters.gaussian(data, sigma)
    size_x, size_y = data.shape
    rho = data_filter.flatten()
    rho_Ind = np.argsort(-rho)
    rho_sorted = rho[rho_Ind]
    maxd = size_x + size_y
    ND = len(rho)

    # delta 记录距离， # IndNearNeigh 记录：两个密度点的联系 % index of nearest neighbor with higher density
    delta, IndNearNeigh, Gradient = np.zeros(ND, np.float), np.zeros(ND, np.int), np.zeros(ND, np.float)

    delta[rho_Ind[0]] = np.sqrt(size_x ** 2 + size_y ** 2)
    IndNearNeigh[rho_Ind[0]] = rho_Ind[0]

    t0 = time.time()
    # 计算 delta, Gradient
    for ii in range(1, ND):
        # 密度降序排序后，即密度第ii大的索引（在rho中）
        ordrho_ii = rho_Ind[ii]
        rho_ii = rho_sorted[ii]   # 第ii大的密度值
        if rho_ii >= rms:
            delta[ordrho_ii] = maxd
            delta_ii_xy = xx[ordrho_ii, :]

            bt = kc_coord_2d(delta_ii_xy, size_y, size_x, k)
            for item in bt:
                rho_jj = data_filter[item[1] - 1, item[0] - 1]
                dist_i_j = np.sqrt(((delta_ii_xy - item) ** 2).sum())  # 计算两点间的距离
                gradient = (rho_jj - rho_ii) / dist_i_j

                if dist_i_j <= delta[ordrho_ii] and gradient >= Gradient[ordrho_ii]:
                    delta[ordrho_ii] = dist_i_j
                    Gradient[ordrho_ii] = gradient
                    IndNearNeigh[ordrho_ii] = (item[1] - 1) * size_y + item[0] - 1

            if delta[ordrho_ii] == maxd:
                # 表明，在(2 * k + 1) * (2 * k + 1) * (2 * k + 1)
                # 的领域中没有找到比该点高，距离最近的点，则进行全局搜索
                for jj in range(0, ii, 1):
                    rho_jj = rho_sorted[jj]
                    ordrho_jj = rho_Ind[jj]
                    delta_jj_xy = xx[ordrho_jj, :]
                    dist_i_j = np.sqrt(((delta_ii_xy - delta_jj_xy) ** 2).sum())
                    gradient = (rho_jj - rho_ii) / dist_i_j
                    if dist_i_j <= delta[ordrho_ii]:
                        delta[ordrho_ii] = dist_i_j
                        Gradient[ordrho_ii] = gradient
                        IndNearNeigh[ordrho_ii] = ordrho_jj
        else:
            IndNearNeigh[ordrho_ii] = ND

    delta_sorted = np.sort(-delta) * (-1)
    delta[rho_Ind[0]] = delta_sorted[1]
    t1 = time.time()
    print('delata, rho and Gradient are calculated, using %.2f seconds' % (t1-t0))

    # 根据密度和距离来确定类中心
    NCLUST = 0
    clustInd = -1 * np.ones(ND + 1)
    clust_index = np.intersect1d(np.where(rho > rhomin), np.where(delta > deltamin))

    clust_num = clust_index.shape[0]
    print(clust_num)

    # icl是用来记录第i个类中心在xx中的索引值
    icl = np.zeros(clust_num, dtype=int)
    for ii in range(0, clust_num):
        i = clust_index[ii]
        icl[NCLUST] = i
        NCLUST += 1
        clustInd[i] = NCLUST

    # assignation
    # 将其他非类中心分配到离它最近的类中心中去
    # clustInd = -1
    # 表示该点不是类的中心点，属于其他点，等待被分配到某个类中去
    # 类的中心点的梯度Gradient被指定为 - 1
    if is_plot == 1:

        plt.scatter(rho, delta, marker='.')
        plt.show()

    for i in range(ND):
        ordrho_i = rho_Ind[i]
        if clustInd[ordrho_i] == -1:    # not centroid
            clustInd[ordrho_i] = clustInd[IndNearNeigh[ordrho_i]]
        else:
            Gradient[ordrho_i] = -1  # 将类中心点的梯度设置为-1

    clustVolume = np.zeros(NCLUST)
    for i in range(NCLUST):
        clustVolume[i] = clustInd.tolist().count(i + 1)

    # % centInd [类中心点在xx坐标下的索引值，
    # 类中心在centInd的索引值: 代表类别编号]
    centInd = []
    for i, item in enumerate(clustVolume):
        if item >= v_min:
            centInd.append([icl[i], i])
    centInd = np.array(centInd, np.int)
    print(centInd.shape[0])
    mask_grad = np.where(Gradient > gradmin)[0]

    # 通过梯度确定边界后，还需要进一步利用最小体积来排除假核
    clustInd_re = -1 * np.ones(ND + 1)   # % 保存最后确定下来的云核的坐标索引
    centInd_re = []  # 保存经过最小体积排出后的类中心信息
    for i, item in enumerate(centInd):
        rho_clust_i = np.zeros(ND)
        # centInd[i, 1] --> item[1] 表示第i个类中心的编号
        index_clust_i = np.where(clustInd == (item[1] + 1))[0]
        index_cc = np.intersect1d(mask_grad, index_clust_i)
        rho_clust_i[index_clust_i] = rho[index_clust_i]
        if len(index_cc) > 0:
            rho_cc_mean = rho[index_cc].mean() * 0.2
        else:
            rho_cc_mean = rms
        index_cc_rho = np.where(rho_clust_i > rho_cc_mean)[0]
        index_clust_rho = np.union1d(index_cc, index_cc_rho)

        if len(index_clust_rho) > v_min:
            # print(i + 1)
            clustInd_re[index_clust_rho] = i + 1
            centInd_re.append([item[0], i])
            # centInd_re.append(item)

    # NCLUST_ = centInd_re.shape[0]
    centInd_re = np.array(centInd_re, np.int)
    return centInd_re, clustInd_re


def densityCluster_2d_new(data, para):
    """
    根据决策图得到聚类中心和聚类中心个数
    :param data: 2D data
    :param para:
        para.rhomin: Minimum density
        para.deltamin: Minimum delta
        para.v_min: Minimum volume
        para.rms: The noise level of the data, used for data truncation calculation
        para.sigma: Standard deviation of Gaussian filtering

    :return:
        NCLUST: number of clusters
        centInd:  centroid index vector
    """
    # 参数初始化
    gradmin = para["gradmin"]
    rhomin = para["rhomin"]
    deltamin = para["deltamin"]
    v_min = para["v_min"]
    rms = para["rms"]
    sigma = para['sigma']
    is_plot = para['is_plot']
    k = 2 # 计算点的邻域大小
    xx = get_xyz(data)  # xx: 2D data coordinates  坐标原点是 1

    data_filter = filters.gaussian(data, sigma)
    size_x, size_y = data.shape
    rho = data_filter.flatten()
    rho_Ind = np.argsort(-rho)
    rho_sorted = rho[rho_Ind]
    maxd = size_x + size_y
    ND = len(rho)

    delta, IndNearNeigh, Gradient = np.zeros(ND, np.float), np.zeros(ND, np.int), np.zeros(ND, np.float)
    delta[rho_Ind[0]] = np.sqrt(size_x ** 2 + size_y ** 2)

    # delta 记录距离，
    # IndNearNeigh
    # 记录：两个密度点的联系 % index of nearest neighbor with higher density
    IndNearNeigh[rho_Ind[0]] = rho_Ind[0]
    t0 = time.time()
    # 计算 delta, Gradient
    for ii in range(1, ND):
        # 密度降序排序后，即密度第ii大的索引（在rho中）
        ordrho_ii = rho_Ind[ii]
        rho_ii = rho_sorted[ii] #第ii大的密度值
        if rho_ii >= rms:
            delta[ordrho_ii] = maxd
            delta_ii_xy = xx[ordrho_ii, :]

            bt = kc_coord_2d(delta_ii_xy, size_y, size_x, k)
            for item in bt:
                rho_jj = data_filter[item[1] - 1, item[0] - 1]
                dist_i_j = dist_xyz(delta_ii_xy, item)
                gradient = (rho_jj - rho_ii) / dist_i_j

                if dist_i_j <= delta[ordrho_ii] and gradient >= Gradient[ordrho_ii]:
                    delta[ordrho_ii] = dist_i_j
                    Gradient[ordrho_ii] = gradient
                    IndNearNeigh[ordrho_ii] = (item[1] - 1) * size_y + item[0] - 1

            if delta[ordrho_ii] == maxd:
                # 表明，在(2 * k + 1) * (2 * k + 1) * (2 * k + 1)
                # 的领域中没有找到比该点高，距离最近的点，则进行全局搜索
                for jj in range(0, ii, 1):
                    rho_jj = rho_sorted[jj]
                    ordrho_jj = rho_Ind[jj]
                    delta_jj_xy = xx[ordrho_jj, :]
                    temp = delta_ii_xy - delta_jj_xy
                    dist_i_j = np.sqrt((temp ** 2).sum())
                    gradient = (rho_jj - rho_ii) / dist_i_j
                    if dist_i_j <= delta[ordrho_ii]:
                        delta[ordrho_ii] = dist_i_j
                        Gradient[ordrho_ii] = gradient
                        IndNearNeigh[ordrho_ii] = ordrho_jj
        else:
            IndNearNeigh[ordrho_ii] = ND

    delta_sorted = np.sort(-delta) * (-1)
    # delta[rho_Ind[0]] = delta_sorted[1]
    t1 = time.time()
    print('delata, rho and Gradient are calculated, using %.2f seconds' % (t1-t0))

    # 根据密度和距离来确定类中心
    NCLUST = 0
    clustInd = -1 * np.ones(ND + 1)
    clust_index = np.intersect1d(np.where(rho > rhomin), np.where(delta > deltamin))

    clust_num = clust_index.shape[0]
    print(clust_num)

    # icl是用来记录第i个类中心在xx中的索引值
    icl = np.zeros(clust_num, dtype=int)
    for ii in range(0, clust_num):
        i = clust_index[ii]
        icl[NCLUST] = i
        NCLUST += 1
        clustInd[i] = NCLUST

    # assignation
    # 将其他非类中心分配到离它最近的类中心中去
    # clustInd = -1
    # 表示该点不是类的中心点，属于其他点，等待被分配到某个类中去
    # 类的中心点的梯度Gradient被指定为 - 1
    if is_plot == 1:
        delta = delta / max(delta[:])
        # figure
    for i in range(0, ND):
        ordrho_i = rho_Ind[i]
        if clustInd[ordrho_i] == -1:# not centroid
            clustInd[ordrho_i] = clustInd[IndNearNeigh[ordrho_i]]
        else:
            Gradient[ordrho_i] = -1  #将类中心点的梯度设置为-1

    clustVolume = np.zeros(NCLUST)
    for i in range(0, NCLUST):
        clustVolume[i] = clustInd.tolist().count(i + 1)

    # % centInd [类中心点在xx坐标下的索引值，
    # 类中心在centInd的索引值: 代表类别编号]
    centInd = []
    for i, item in enumerate(clustVolume):
        if item >= v_min:
            centInd.append([icl[i], i])
    centInd = np.array(centInd, np.int)

    mask_grad = np.where(Gradient > gradmin)[0]

    # 通过梯度确定边界后，还需要进一步利用最小体积来排除假核
    clustInd_re = -1 * np.ones(ND + 1)   # % 保存最后确定下来的云核的坐标索引
    centInd_re = []  # 保存经过最小体积排出后的类中心信息
    for i, item in enumerate(centInd):
        rho_clust_i = np.zeros(ND)
        # centInd[i, 1] --> item[1] 表示第i个类中心的编号
        index_clust_i = np.where(clustInd == (item[1] + 1))[0]
        index_cc = np.intersect1d(mask_grad, index_clust_i)
        rho_clust_i[index_clust_i] = rho[index_clust_i]
        rho_cc_mean = rho[index_cc].mean() * 0.2
        index_cc_rho = np.where(rho_clust_i > rho_cc_mean)[0]
        index_clust_rho = np.union1d(index_cc, index_cc_rho)
        if len(index_clust_rho) > v_min:
            clustInd_re[index_clust_rho] = i + 1

            centInd_re.append(item)

    # NCLUST_ = centInd_re.shape[0]
    centInd_re = np.array(centInd_re, np.int)
    return centInd_re, clustInd_re


if __name__ == '__main__':
    pass