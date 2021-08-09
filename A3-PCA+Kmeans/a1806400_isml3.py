# -*- coding: utf-8 -*-
"""a1806400_ISML3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wrb_HTuarqriznvBA2Szch168QJPEo4m
"""

from google.colab import drive
drive.mount('/content/drive')

trainPath = "/content/drive/My Drive/data/mnist_train.csv"
testPath = "/content/drive/My Drive/data/mnist_test.csv"

import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

dfTrain = pd.read_csv(trainPath, header=None)
trainData = pd.DataFrame(dfTrain)
trainLabelData = dfTrain.iloc[:,0]
trainData = trainData.iloc[:,1:]
trainData.shape

dfTest = pd.read_csv(testPath, header=None)
testData = pd.DataFrame(dfTest)
testLabelData = testData.iloc[:,0]
testData = testData.drop([0], axis = 1)
testData.shape

"""**TASK 1 & 2**"""

# standardising features 

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(trainData)
trainData = scaler.transform(trainData)
testData = scaler.transform(testData)

# PCA implementation

def PCA_implemented(X,components):
  X = np.array(X)
  XmeanValue = np.mean(X , axis =0)
  X_meaned = X - XmeanValue
  # Covariance matrix
  covariance_matrix = np.matmul(X_meaned.T, X_meaned)/(X.shape[0]-1)
  # Eigen decomposition
  eigenValues, eigenVectors = np.linalg.eig(covariance_matrix)

  # sorting Eigen values and eigen vectors
  sortedEigenValues = eigenValues[:components]
  sortedEigenVectors = eigenVectors[:,:components]
  return eigenValues, eigenVectors, sortedEigenValues, sortedEigenVectors

# Explained variance

def explained_variance(eigenValues):
    explained_variance =[]
    for i in range(len(eigenValues)):
        explained_variance.append(eigenValues[i]/np.sum(eigenValues))
    return explained_variance

eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainData, 180)

# Cumulative variance

cum_variance = []
for i in range(len(eigenValues_train)):
  var = explained_variance(eigenValues_train)
  vsum = np.sum(var[:i])
  cum_variance.append(vsum)

#Graph to find the maximum variance

plt.figure(figsize=(12,7))
plt.plot(cum_variance)
plt.yticks(np.arange(0,1,0.1))
plt.xticks(np.arange(0,800,50))
plt.xlabel('no of components - PCA ', fontsize=12)
plt.ylabel('Explained Variance', fontsize=12)
plt.title('Explained Variance vs no of components - PCA', fontsize=12)

# Projection matrix

def project_matrix(X, eigen_vector, components):
    matrix=np.zeros((X.shape[0], components))
    for i in range(components):
        projection = np.dot(X, eigen_vector.T[i])
        matrix[:,i] = projection
    return matrix

trainDataPCA = project_matrix(trainData, eigenVectors_train, 180)
trainDataPCA = pd.DataFrame(trainDataPCA)

testDataPCA = project_matrix(testData, sortedEigenVectors_train, 180)
testDataPCA = pd.DataFrame(testDataPCA)



"""PCA with KNN (1 neighbour)"""

from sklearn.neighbors import KNeighborsClassifier
knn_scores = []
for i in range(1, 256, 10):
    neigh = KNeighborsClassifier(n_neighbors=1)
    eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainData, i)
    trainDataPCA = project_matrix(trainData, sortedEigenVectors_train, i)
    testDataPCA = project_matrix(testData, sortedEigenVectors_train, i)
    neigh.fit(trainDataPCA, trainLabelData)
    y_pred = neigh.predict(testDataPCA)
    score = np.mean(testLabelData == y_pred)
    knn_scores.append(score)

plt.figure(figsize=(10,6))
x = range(1, 256, 10)
plt.plot(x, knn_scores)
plt.xticks(range(1, 256, 10))
plt.xlabel('no of components - PCA')
plt.ylabel('accuracy score')
plt.title('KNN accuracy VS no of components - PCA')

"""**TASK 5**"""

dfTrain = pd.read_csv(trainPath, header=None)
trainData = pd.DataFrame(dfTrain)
trainLabelData = dfTrain.iloc[:,0]
trainData = trainData.iloc[:,1:]
trainData.shape

dfTest = pd.read_csv(testPath, header=None)
testData = pd.DataFrame(dfTest)
testLabelData = testData.iloc[:,0]
testData = testData.drop([0], axis = 1)
testData.shape

import warnings
warnings.simplefilter("ignore", np.ComplexWarning)
testLabelData = np.array(testLabelData)

from sklearn.neighbors import KNeighborsClassifier
knn_scores_regular = []
for i in range(1, 256, 10):
    knn = KNeighborsClassifier(n_neighbors=1)
    eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainData, i)
    X_train_pca = project_matrix(trainData, sortedEigenVectors_train, i)
    X_test_pca = project_matrix(testData, sortedEigenVectors_train, i)
    knn.fit(X_train_pca, trainLabelData)
    y_pred = knn.predict(X_test_pca)
    score = np.mean(testLabelData == y_pred)
    knn_scores_regular.append(score)

x = range(1, 256, 10)
plt.figure(figsize=(10,6))
plt.plot(x, knn_scores_regular)

x_ = range(1, 256, 10)
plt.xticks(x_);
plt.xlabel('n_components')
plt.ylabel('accuracy')
plt.title('Noisy Data - KNN accuracy VS PCA n_components')

"""Adding Noise to the data

Train data noise addition
"""

noiseTrain = np.random.normal(0, 0.75, (6000,256))
noiseTrain = pd.DataFrame(noiseTrain)
trainData = pd.DataFrame(trainData)
trainDataNoise = pd.concat([trainData,noiseTrain],ignore_index=True, axis =1) 
print(trainDataNoise.shape)

"""Test data noise addition"""

noiseTest = np.random.normal(0, 0.75, (1000,256))
noiseTest = pd.DataFrame(noiseTest)
testData = pd.DataFrame(testData)

testDataNoise = pd.concat([testData,noiseTest],ignore_index=True, axis =1) 
print(testDataNoise.shape)

"""PCA with KNN(n=1) - Noisy Data"""

from sklearn.neighbors import KNeighborsClassifier
knn_scores_noise = []
for i in range(1, 256, 10):
    neigh = KNeighborsClassifier(n_neighbors=1)
    trainDataNoise = np.array(trainDataNoise)
    eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainDataNoise, i)
    trainDataPCA = project_matrix(trainDataNoise, sortedEigenVectors_train, i)
    testDataPCA = project_matrix(testDataNoise, sortedEigenVectors_train, i)
    neigh.fit(trainDataPCA, trainLabelData)
    y_pred = neigh.predict(testDataPCA)
    score = np.mean(testLabelData == y_pred)
    knn_scores_noise.append(score)

PCA_components = range(1, 260, 10)
plt.figure(figsize=(10,6))
plt.plot(PCA_components, knn_scores_noise)

plt.xticks(PCA_components)
plt.xlabel('PCA_components')
plt.ylabel('accuracy')
plt.title('Noisy Data - KNN accuracy VS PCA_components')

# KNN performance comparison on noisy and normal data
plt.figure(figsize=(10,6))

PCA_components = range(1, 260, 10)
plt.plot(PCA_components, knn_scores, label='KNN - without noise')
plt.plot(PCA_components, knn_scores_noise, label = 'KNN - with noise')

plt.xticks(PCA_components)
plt.xlabel('PCA_components')
plt.ylabel('accuracy score')
plt.title('KNN with noise and without noise performance')
plt.legend()

"""SVM"""

from sklearn.svm import SVC

SVM_scores = []
for i in range(1, 260, 10):
    clf = SVC(gamma='auto', kernel='linear', C=0.05)
    eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainData, i)
    trainDataPca = project_matrix(trainData, sortedEigenVectors_train, i)    
    testDataPca = project_matrix(testData, sortedEigenVectors_train, i)

    clf.fit(trainDataPca, trainLabelData)
    y_pred = clf.predict(testDataPca)

    score = np.mean(testLabelData == y_pred)
    SVM_scores.append(score)

x = range(1, 260, 10)
plt.figure(figsize=(10,6))
plt.plot(x, SVM_scores)

PCA_components = range(1, 260, 10)
plt.xticks(PCA_components);
plt.xlabel('PCA components')
plt.ylabel('accuracy')
plt.title('SVM accuracy VS PCA components for normal data')

"""PCA + SVM with noisy data"""

#  SVM with noisy data

from sklearn.svm import SVC

SVM_scores_noise = []
for i in range(1, 260, 10):
    eigenValues_train, eigenVectors_train, sortedEigenValues_train, sortedEigenVectors_train = PCA_implemented(trainDataNoise, i)
    trainDataPCA = project_matrix(trainDataNoise, sortedEigenVectors_train, i)
    testDataPCA = project_matrix(testDataNoise, sortedEigenVectors_train, i)

    clf = SVC(gamma='auto', kernel='linear', C=0.05)
    clf.fit(trainDataPCA, trainLabelData)
    y_pred = clf.predict(testDataPCA)
    score = np.mean(testLabelData == y_pred)
    SVM_scores_noise.append(score)

x = range(1, 260, 10)
plt.figure(figsize=(10,6))
plt.plot(x, SVM_scores_noise)

PCA_components = range(1, 260, 10)
plt.xticks(PCA_components);
plt.xlabel('PCA components')
plt.ylabel('accuracy')
plt.title('SVM accuracy VS PCA components for noisy data')

# KNN performance comparison on noisy and normal data
plt.figure(figsize=(10,6))

PCA_components = range(1, 260, 10)
plt.plot(PCA_components, SVM_scores, label='SVM - without noise')
plt.plot(PCA_components, SVM_scores_noise, label = 'SVM - with noise')

plt.xticks(PCA_components)
plt.xlabel('PCA_components')
plt.ylabel('accuracy score')
plt.title('SVM with noise and without noise performance')
plt.legend()

"""TASK 3 & 4"""

trainPath = "/content/drive/My Drive/data/mnist_train.csv"
testPath = "/content/drive/My Drive/data/mnist_test.csv"

import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

dfTrain = pd.read_csv(trainPath, header=None)
trainData = pd.DataFrame(dfTrain)
trainLabelData = dfTrain.iloc[:,0]
trainData = trainData.iloc[:,1:]
trainData.shape

dfTest = pd.read_csv(testPath, header=None)
testData = pd.DataFrame(dfTest)
testLabelData = testData.iloc[:,0]
testData = testData.drop([0], axis = 1)
testData.shape

# standardising features 
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(trainData)
trainData = scaler.transform(trainData)
testData = scaler.transform(testData)
print(np.max(trainData))

# Initialising 10 centroids
centroids = []
k = 10
for i in range(k):
  centroid = trainData[i]
  centroids.append(centroid)
print("Initialised 10 centroids")

# recomputing the centroids

def recompute_centroids(clusters, clusterData):
    newCentroid = []
    cluster_df = pd.concat([pd.DataFrame(clusterData), pd.DataFrame(clusters,columns=['cluster'])], axis=1)
    for number in range(0,10):
        cluster_numbered  = cluster_df.loc[cluster_df['cluster']== number]
        cluster_numbered_mean = np.mean(cluster_numbered.iloc[:,:-1], axis=0)
        newCentroid.append(cluster_numbered_mean)
    return newCentroid

# Calculate variance within each cluster
def centroid_variance(clusters, cluster_array):
    sum_squares = []
    cluster_df = pd.concat([pd.DataFrame(cluster_array), pd.DataFrame(clusters, columns=['cluster'])], axis=1)
    for c in range(0,10):
        cluster_c  = cluster_df.loc[cluster_df['cluster']== c]
        cluster_c = cluster_c.iloc[:,:-1]
        cluster_c_mean = np.mean(cluster_c, axis=0)
        mean_repeat = np.tile(cluster_c_mean,(cluster_c.shape[0],1))
        sum_squares.append(np.sum(np.sum((cluster_c - mean_repeat)**2)))
    return sum_squares

import math
def assign_clusters(centroids, data):
    clusters = []
    for i in range(0, data.shape[0]):
        compDistance = []
        # calculating distance between each data point and all centroids
        for centroid in centroids:
            # Euclidean distance
            indvDistance = math.sqrt(sum((centroid - data[i])**2)) 
            compDistance.append(indvDistance)
        cluster = compDistance.index(min(compDistance))
        clusters.append(cluster)
    return clusters

"""TASK 3"""

clusters = assign_clusters(centroids, trainData)
cluster_variance_noDR = []

for i in range(1,100):
    # recomputing clusters
    centroids = recompute_centroids(clusters, trainData)
    clusters = assign_clusters(centroids, trainData)
    cluster_variance_mean = np.mean(centroid_variance(clusters, trainData))
    cluster_variance_noDR.append(cluster_variance_mean)
    # cluster_variance_3a.append(cluster_var_3a)
    print(i, round(cluster_variance_mean))

plt.figure(figsize=(10,6))
plt.plot(cluster_variance_noDR)
plt.title('K-means Cluster Loss value with no Dimensionality reduction Vs Iterations', fontsize=14)
plt.xlabel('Iterations', fontsize=12)
plt.ylabel('Loss value', fontsize=12)

"""TASK 4"""

def newCentroid(data, k):
    centroidList = []
    for i in range(k):
        centroid = data[i]
        centroidList.append(centroid) 
    return centroidList

centroid_6 = newCentroid(trainData, 6)
centroid_9 = newCentroid(trainData, 9)
centroid_12 = newCentroid(trainData, 12)
centroid_15 = newCentroid(trainData, 15)

centroidList = [centroid_6, centroid_9, centroid_12, centroid_15]

for centroidNo in centroidList:
    clusters = assign_clusters(centroidNo, trainData)
    converge_variance = []
    cluster_variance_list = []
    for i in range(1,65):
        centroids = recompute_centroids(clusters, trainData)
        clusters = assign_clusters(centroids, trainData)
        cluster_variance = np.mean(centroid_variance(clusters, trainData))
        cluster_variance_list.append(cluster_variance)
        cluster_variance_value = round(cluster_variance)
        print(i,cluster_variance_value)
    print ('converged_variance: ', cluster_variance)
    converge_variance.append(cluster_variance)

plt.figure(figsize=(10,6))
x = [6, 9, 12, 15]
cluster_variance = [350000 , 330000 , 320000, 300000]
plt.plot(x, cluster_variance)
plt.title('K-means Cluster Loss Vs no. of clusters', fontsize=14)
plt.xlabel('No. of classifications', fontsize=12)
plt.ylabel('Loss', fontsize=12)





