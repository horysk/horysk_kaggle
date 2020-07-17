


def logistic():

    #coding=utf-8
    from sklearn import linear_model
    from matplotlib import pyplot
    import numpy as np

    #本程序建立逻辑回归模型
    #让逻辑回归模型自动学习如何判断两个数值的大小关系

    #训练数据集，共8个样本
    #每个样本包含两个特征[a,b]
    #前4个样本表示a<b，后4个样本表示a>b
    data=[[3,4],[3,6],[3,7],[4,7],
        [4,3],[6,3],[7,3],[7,4]]

    #目标值，即a<b还是a>b
    #0表示a<b，1表示a>b
    target=[0,0,0,0,
            1,1,1,1]

    #初始化逻辑回归模型
    logreg = linear_model.LogisticRegression(C=1e5)
    #训练逻辑回归模型
    logreg.fit(data, target)

    #测试判断样本[100,101]的目标值
    #即判断100<101还是100>101
    print (logreg.predict(np.array([100,101]).reshape(1,-1)))

    #同上
    print (logreg.predict(np.array([101,100]).reshape(1,-1)))


    #在一个2D图上绘制点阵
    #如果x<y，则将点绘制成红色
    #如果x>y，则将点绘制成蓝绿色
    for x in range(0,20):
        for y in range(0,20):
        #输入[x,y]，利用逻辑回归模型预测目标值
            t=logreg.predict(np.array([x,y]).reshape(1,-1))
            if(t==0):
                pyplot.plot(x,y,'ro')
            else:
                pyplot.plot(x,y,'co')

    pyplot.show()

def iris():
    from sklearn import datasets
    iris=datasets.load_iris()

    #data对应了样本的4个特征，150行4列
    print (iris.data.shape)

    #显示样本特征的前5行
    print (iris.data[:5])

    #target对应了样本的类别（目标属性），150行1列
    print( iris.target.shape
)
    #显示所有样本的目标属性
    print (iris.target)


def make_blobs():
    from sklearn.datasets import make_blobs
    from matplotlib import pyplot

    data,target=make_blobs(n_samples=100,n_features=2,centers=3)

    #在2D图中绘制样本，每个样本颜色不同
    pyplot.scatter(data[:,0],data[:,1],c=target);
    pyplot.show()

def make_blobs_():
    from sklearn.datasets import make_blobs
    from matplotlib import pyplot

    data,target=make_blobs(n_samples=100,n_features=2,centers=3,cluster_std=[1.0,2.0,3.0])

    #在2D图中绘制样本，每个样本颜色不同
    pyplot.scatter(data[:,0],data[:,1],c=target);
    pyplot.show()

def kmeans():
    #coding=utf-8
    from sklearn import datasets
    from matplotlib import pyplot as plt
    import numpy as np
    from sklearn.cluster import KMeans

    iris = datasets.load_iris()
    original_x = iris.data

    #读取内置的iris数据集
    #原始iris数据集有4个维度，为了方便展示到2D图
    #我们用第一列加上第三列、第二列加上第四列获得2个新特征
    #用这2个新特征取代原来的4个特征
    datas = original_x[:, :2] + original_x[:, 2:]

    #计算最大值最小值，用于绘图时计算坐标范围
    border = 0.5
    x_min, x_max = datas[:, 0].min() - border, datas[:, 0].max() + border
    y_min, y_max = datas[:, 1].min() - border, datas[:, 1].max() + border

    #进行KMeans聚类
    kmeans = KMeans(init='k-means++', n_clusters = 3)
    kmeans.fit(datas)

    #计算每一类到其中心距离的平均值，作为绘图时绘制圆圈的依据
    distances_for_labels = []

    for label in range(kmeans.n_clusters):
        distances_for_labels.append([])

    for i, data in enumerate(datas):
        label = kmeans.labels_[i]
        center = kmeans.cluster_centers_[label]
        distance = np.sqrt(np.sum(np.power(data - center, 2)))
        distances_for_labels[label].append(distance)

    ave_distances = [np.average(distances_for_label) for distances_for_label in distances_for_labels]

    #绘图
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    #设置坐标范围
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))

    #绘制每个Cluster
    for label, center in enumerate(kmeans.cluster_centers_):
        radius = ave_distances[label] * 1.5
        ax.add_artist(plt.Circle(center, radius = radius, color = "r", fill = False))

    #根据每个数据的真实label来选择数据点的颜色
    plt.scatter(datas[:, 0], datas[:, 1], c = iris.target)
    plt.show()

def k_means():
    from sklearn import cluster, datasets
    iris = datasets.load_iris()
    X_iris = iris.data
    y_iris = iris.target

    k_means = cluster.KMeans(n_clusters=3)
    k_means.fit(X_iris)
    print(k_means.labels_[::10])
    print(y_iris[::10])


def boundary():
    print(__doc__)

# Authors: Clay Woolam <clay@woolam.org>
# License: BSD

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn import svm
    from sklearn.semi_supervised import LabelSpreading

    rng = np.random.RandomState(0)

    iris = datasets.load_iris()

    X = iris.data[:, :2]
    y = iris.target

    # step size in the mesh
    h = .02

    y_30 = np.copy(y)
    y_30[rng.rand(len(y)) < 0.3] = -1
    y_50 = np.copy(y)
    y_50[rng.rand(len(y)) < 0.5] = -1
    # we create an instance of SVM and fit out data. We do not scale our
    # data since we want to plot the support vectors
    ls30 = (LabelSpreading().fit(X, y_30), y_30)
    ls50 = (LabelSpreading().fit(X, y_50), y_50)
    ls100 = (LabelSpreading().fit(X, y), y)
    rbf_svc = (svm.SVC(kernel='rbf', gamma=.5).fit(X, y), y)

    # create a mesh to plot in
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))

    # title for the plots
    titles = ['Label Spreading 30% data',
            'Label Spreading 50% data',
            'Label Spreading 100% data',
            'SVC with rbf kernel']

    color_map = {-1: (1, 1, 1), 0: (0, 0, .9), 1: (1, 0, 0), 2: (.8, .6, 0)}

    for i, (clf, y_train) in enumerate((ls30, ls50, ls100, rbf_svc)):
        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        plt.subplot(2, 2, i + 1)
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
        plt.axis('off')

        # Plot also the training points
        colors = [color_map[y] for y in y_train]
        plt.scatter(X[:, 0], X[:, 1], c=colors, edgecolors='black')

        plt.title(titles[i])

    plt.suptitle("Unlabeled points are colored white", y=0.1)
    plt.show()


def propagation():
    print(__doc__)

    # Authors: Clay Woolam <clay@woolam.org>
    #          Andreas Mueller <amueller@ais.uni-bonn.de>
    # License: BSD

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.semi_supervised import LabelSpreading
    from sklearn.datasets import make_circles

    # generate ring with inner box
    n_samples = 200
    X, y = make_circles(n_samples=n_samples, shuffle=False)
    outer, inner = 0, 1
    labels = np.full(n_samples, -1.)
    labels[0] = outer
    labels[-1] = inner

    # #############################################################################
    # Learn with LabelSpreading
    label_spread = LabelSpreading(kernel='knn', alpha=0.8)
    label_spread.fit(X, labels)

    # #############################################################################
    # Plot output labels
    output_labels = label_spread.transduction_
    plt.figure(figsize=(8.5, 4))
    plt.subplot(1, 2, 1)
    plt.scatter(X[labels == outer, 0], X[labels == outer, 1], color='navy',
                marker='s', lw=0, label="outer labeled", s=10)
    plt.scatter(X[labels == inner, 0], X[labels == inner, 1], color='c',
                marker='s', lw=0, label='inner labeled', s=10)
    plt.scatter(X[labels == -1, 0], X[labels == -1, 1], color='darkorange',
                marker='.', label='unlabeled')
    plt.legend(scatterpoints=1, shadow=False, loc='upper right')
    plt.title("Raw data (2 classes=outer and inner)")

    plt.subplot(1, 2, 2)
    output_label_array = np.asarray(output_labels)
    outer_numbers = np.where(output_label_array == outer)[0]
    inner_numbers = np.where(output_label_array == inner)[0]
    plt.scatter(X[outer_numbers, 0], X[outer_numbers, 1], color='navy',
                marker='s', lw=0, s=10, label="outer learned")
    plt.scatter(X[inner_numbers, 0], X[inner_numbers, 1], color='c',
                marker='s', lw=0, s=10, label="inner learned")
    plt.legend(scatterpoints=1, shadow=False, loc='upper right')
    plt.title("Labels learned with Label Spreading (KNN)")

    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.93, top=0.92)
    plt.show()

if __name__ == "__main__":
    # iris()
    # logistic()
    # make_blobs()
    # make_blobs_()
    # kmeans()
    # k_means()
    boundary()
    propagation()