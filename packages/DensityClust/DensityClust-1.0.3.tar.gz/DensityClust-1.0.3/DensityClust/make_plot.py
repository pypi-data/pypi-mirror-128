from matplotlib import pyplot as plt
import pandas as pd


def make_plot(outcat_name, data, lable_num=True):
    outcat = pd.read_csv(outcat_name, sep='\t')
    ID = outcat['ID'].values
    Sum = outcat['Sum'].values
    if data.ndim == 2:
        fig, ax0 = plt.subplots(1, 1, figsize=(8, 6))
        ax0.imshow(data, cmap='gray')
        if outcat is not None:
            Cen1 = outcat['Cen1'] - 1
            Cen2 = outcat['Cen2'] - 1
            Peak1 = outcat['Peak1'] - 1
            Peak2 = outcat['Peak2'] - 1

            ax0.plot(Cen1, Cen2, '.', color='red')
            ax0.plot(Peak1, Peak2, '*', color='green')
            for i in range(outcat.shape[0]):

                ax0.text(Cen1[i], Cen2[i], '%d:%.2f' % (ID[i], Sum[i]), color='r', s=100)
                ax0.text(Cen1[i], Cen2[i], '%d' % (ID[i]), color='r')
                ax0.text(Peak1[i], Peak2[i], '%d' % (ID[i]), color='r')

        fig.tight_layout()
        plt.xticks([])
        plt.yticks([])
        plt.show()

    elif data.ndim == 3:
        fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(8, 6))
        ax0.imshow(data.sum(axis=0), cmap='gray')
        ax1.imshow(data.sum(axis=1), cmap='gray')
        ax2.imshow(data.sum(axis=2), cmap='gray')
        if outcat is not None:
            Cen1 = outcat['Cen1'] - 1
            Cen2 = outcat['Cen2'] - 1
            Cen3 = outcat['Cen3'] - 1
            outcat = outcat - 1

            ax0.scatter(Cen1, Cen2, marker='.', c='red', s=8)
            ax1.scatter(Cen1, Cen3, marker='*', c='red', s=8)
            ax2.scatter(Cen2, Cen3, marker='^', c='red', s=8)

            if lable_num:
                for i in range(outcat.shape[0]):
                    ax0.text(Cen1[i], Cen2[i], '%d' % ID[i], color='g')
                    ax1.text(Cen1[i], Cen3[i], '%d' % ID[i], color='g')
                    ax2.text(Cen2[i], Cen3[i], '%d' % ID[i], color='g')

        fig.tight_layout()
        plt.xticks([])
        plt.yticks([])
        plt.show()


def make_tri_plot(data):
    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(8, 6))
    ax0.imshow(data.sum(axis=0), cmap='gray',)
    ax1.imshow(data.sum(axis=1), cmap='gray')
    ax2.imshow(data.sum(axis=2), cmap='gray')

    fig.tight_layout()
    plt.xticks([])
    plt.yticks([])
    plt.show()


def make_two_plot(data, outcat):
    fig, ax0 = plt.subplots(1, 1, figsize=(8, 6))
    ax0.imshow(data, cmap='gray')
    ax0.plot(outcat[:, 3] - 1, outcat[:, 4] - 1, 'r*')

    fig.tight_layout()
    plt.xticks([])
    plt.yticks([])
    plt.show()


def plot_match():
    match_txt = r'test_data\2d_simulated_clump\gaussian_out_360\match\Match_table\Match_LDC.txt'
    match = pd.read_csv(match_txt, sep='\t')
    plt.subplot(3, 2, 1)
    plt.plot(match['s_Cen1'].values, match['f_Cen1'].values, '.')
    plt.subplot(3, 2, 2)
    plt.plot(match['s_Cen2'].values, match['f_Cen2'].values, '.')
    plt.subplot(3, 2, 3)
    plt.plot(match['s_Size1'].values, match['f_Size1'].values, '.')
    plt.subplot(3, 2, 4)
    plt.plot(match['s_Size2'].values, match['f_Size2'].values, '.')
    plt.subplot(3, 2, 5)
    plt.plot(match['s_Peak'].values, match['f_Peak'].values, '.')
    plt.subplot(3, 2, 6)
    plt.plot(match['s_Sum'].values, match['f_Sum'].values, '.')
    plt.show()
