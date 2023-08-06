import numpy as np
import time


def setdiff_nd(a1, a2):
    """
    python 使用numpy求二维数组的差集
    :param a1:
    :param a2:
    :return:
    """
    # a1 = index_value
    # a2 = np.array([point_ii_xy])
    a1_rows = a1.view([('', a1.dtype)] * a1.shape[1])
    a2_rows = a2.view([('', a2.dtype)] * a2.shape[1])

    a3 = np.setdiff1d(a1_rows, a2_rows).view(a1.dtype).reshape(-1, a1.shape[1])
    return a3


def get_xyz(data):
    """
    :param data: 3D data
    :return: 3D data coordinates
    第1,2,3维数字依次递增

     :param data: 2D data
    :return: 2D data coordinates
    第1,2维数字依次递增

    """
    nim = data.ndim
    if nim == 3:
        size_x, size_y, size_z = data.shape
        x_arange = np.arange(1, size_x+1)
        y_arange = np.arange(1, size_y+1)
        z_arange = np.arange(1, size_z+1)
        [xx, yy, zz] = np.meshgrid(x_arange, y_arange, z_arange, indexing='ij')
        xyz = np.column_stack([zz.flatten(), yy.flatten(), xx.flatten()])

    else:
        size_x, size_y = data.shape
        x_arange = np.arange(1, size_x + 1)
        y_arange = np.arange(1, size_y + 1)
        [xx, yy] = np.meshgrid(x_arange, y_arange, indexing='ij')
        xyz = np.column_stack([yy.flatten(), xx.flatten()])
    return xyz


def kc_coord_3d(point_ii_xy, xm, ym, zm, r):
    """
    :param point_ii_xy: 当前点坐标(x,y,z)
    :param xm: size_x
    :param ym: size_y
    :param zm: size_z
    :param r: 2 * r + 1
    :return:
    返回delta_ii_xy点r邻域的点坐标
    """
    it = point_ii_xy[0]
    jt = point_ii_xy[1]
    kt = point_ii_xy[2]

    xyz_min = np.array([[1, it - r], [1, jt - r], [1, kt - r]])
    xyz_min = xyz_min.max(axis=1)

    xyz_max = np.array([[xm, it + r], [ym, jt + r], [zm, kt + r]])
    xyz_max = xyz_max.min(axis=1)

    x_arange = np.arange(xyz_min[0], xyz_max[0] + 1)
    y_arange = np.arange(xyz_min[1], xyz_max[1] + 1)
    v_arange = np.arange(xyz_min[2], xyz_max[2] + 1)

    [p_k, p_i, p_j] = np.meshgrid(x_arange, y_arange, v_arange, indexing='ij')
    Index_value = np.column_stack([p_k.flatten(), p_i.flatten(), p_j.flatten()])
    Index_value = setdiff_nd(Index_value, np.array([point_ii_xy]))

    ordrho_jj = np.matmul(Index_value - 1, np.array([[1], [xm], [ym * xm]]))
    ordrho_jj.reshape([1, ordrho_jj.shape[0]])

    return ordrho_jj[:, 0], Index_value


def kc_coord_2d(point_ii_xy, xm, ym, r):
    """
    :param point_ii_xy: 当前点坐标(x,y)
    :param xm: size_x
    :param ym: size_y
    :param r: 2 * r + 1
    :return:
    返回point_ii_xy点r邻域的点坐标
    """
    it = point_ii_xy[0]
    jt = point_ii_xy[1]

    xyz_min = np.array([[1, it - r], [1, jt - r]])
    xyz_min = xyz_min.max(axis=1)

    xyz_max = np.array([[xm, it + r], [ym, jt + r]])
    xyz_max = xyz_max.min(axis=1)

    x_arrange = np.arange(xyz_min[0], xyz_max[0] + 1)
    y_arrange = np.arange(xyz_min[1], xyz_max[1] + 1)

    [p_k, p_i] = np.meshgrid(x_arrange, y_arrange, indexing='ij')
    Index_value = np.column_stack([p_k.flatten(), p_i.flatten()])
    Index_value = setdiff_nd(Index_value, np.array([point_ii_xy]))

    return Index_value


if __name__ == '__main__':
    xm, ym, zm = 100, 80, 120
    r = 3
    delta_ii_xy = np.array([43, 22, 109])
    t0 = time.time()
    index, index_value = kc_coord_3d(delta_ii_xy, xm, ym, zm, r)
    t1 = time.time()
    print((t1-t0) * 10000000)
    delta_ii_xy = np.array([43, 22])
    aa1 = kc_coord_2d(delta_ii_xy, xm, ym, r)
