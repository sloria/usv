#!/usr/bin/env python
# encoding: utf-8
"""
cv.py
Provides tests for evaluating classifiers. Includes k-fold cross validation, feature subset selection,
class accuracy, SVM parameter tuning, and learning curve tests.

Usage:
    Uncomment tests you want to use, then run:
    
    >>> cv.py
"""
import Orange, orange, orngDisc, orngTest, orngStat, orngFSS
from Orange.classification.svm import *
import orngTree
import sys
import time
from Orange.ensemble import *

def main():
    TRAIN_DATA = orange.ExampleTable("/Users/sloria1/projects/usv/trainsets/traindata_with_bark.tab")
    TEST_RESULTS = "/Users/sloria1/projects/usv/testresults.tab"
    testFile = open(TEST_RESULTS, "a+")

    # Learners
    bayes = orange.BayesLearner(name="Naive Bayes")
    tree = orngTree.TreeLearner(name="Classification Tree")
    treePruned2 = orngTree.TreeLearner(name="Classification Tree Pruned (2)", mForPruning=2)
    treePruned4 = orngTree.TreeLearner(name="Classification Tree Pruned (4)", mForPruning=4)
    svm_easy = SVMLearnerEasy(name="SVM (easy)")

    c = 128
    g = 2
    n = 0.1
    svmRBF = SVMLearner(name="SVM (RBF)", 
                        kernel_type=kernels.RBF, C=c, gamma=g, nu=n)
    svmPoly = SVMLearner(name="SVM (Poly)", 
                        kernel_type=kernels.Polynomial, degree=3, C=c, gamma=g, nu=n)
    svmLinear = SVMLearner(name="SVM (Linear)", 
                            kernel_type=kernels.Linear, C=c, gamma=g, nu=n)

    knn10 = Orange.classification.knn.kNNLearner(k=10, name="K-nearest neighbor (10)")
    knn = Orange.classification.knn.kNNLearner(name="K-nearest neighbor")
    knn50 = Orange.classification.knn.kNNLearner(k=50, name="K-nearest neighbor (50)")
    knn100 = Orange.classification.knn.kNNLearner(k=100, name="K-nearest neighbor (100)")
    knn5 = Orange.classification.knn.kNNLearner(k=5, name="K-nearest neighbor (5)")
    
    # Ensemble learners
    baseLearners = [bayes, knn, treePruned2]
    stacked = Orange.ensemble.stacking.StackedClassificationLearner(
                                        baseLearners, name="Stacked")
    baggedSVM10 = Orange.ensemble.bagging.BaggedLearner(
                                        svmRBF, name="Bagged SVM_RBF (10)", t=10)
    baggedSVM30 = Orange.ensemble.bagging.BaggedLearner(svmRBF, name="Bagged SVM_RBF (20)", t=30)
    boostedSVM10 = boosting.BoostedLearner(svmRBF, name="Boosted SVM_RBF(10)", t=10)
    baggedBayes5 = Orange.ensemble.bagging.BaggedLearner(
                                        bayes, name="Bagged Bayes (5)", t=5)    
    baggedBayes10 = Orange.ensemble.bagging.BaggedLearner(
                                        bayes, name="Bagged Bayes (10)", t=10)
    baggedBayes20 = Orange.ensemble.bagging.BaggedLearner(
                                        bayes, name="Bagged Bayes (20)", t=20)
    boostedBayes5 = Orange.ensemble.boosting.BoostedLearner(
                                        bayes, name="Boosted Bayes (5)", t=5)
    boostedBayes10 = Orange.ensemble.boosting.BoostedLearner(
                                        bayes, name="Boosted Bayes (10)", t=10)
    baggedTree5 = Orange.ensemble.bagging.BaggedLearner(
                                        tree, name="Bagged Tree (5)", t=5)
    baggedTree20 = Orange.ensemble.bagging.BaggedLearner(
                                        tree, name="Bagged Tree (20)", t=20)
    boostedTree5 = Orange.ensemble.boosting.BoostedLearner(
                                        tree, name="Boosted Tree (5)", t=5)
    boostedkNN50 = Orange.ensemble.boosting.BoostedLearner(
                                        knn, name="Boosted kNN (5)", t=50)
    boostedTree20 = Orange.ensemble.boosting.BoostedLearner(
                                        tree, name="Boosted Tree (20)", t=20)
    randomForest = Orange.ensemble.forest.RandomForestLearner(name="Random Forest") 
    
    ####################################
    ############  TUNE SVM  ############
    ####################################
        
    svmRBF.tune_parameters(TRAIN_DATA, folds=5, parameters=["C", "gamma"], verbose=True)
    svmRBF.tune_parameters(TRAIN_DATA, folds=5, parameters=["nu"], verbose=True)
    
    ####################################
    ############  TEST FSS  ############
    ####################################
    # test_fss(svmRBF, TRAIN_DATA, 0.01)
    
    ####################################
    ############  TEST LEARNERS ########
    ####################################
    # 
    learners = [ # bayes,
                 # tree,
                 #treePruned2,
                 # treePruned4,
                svmRBF,
                #svmPoly,
                 # svmLinear,
                 # knn
                 # knn5,
                 # knn10,
                 # knn50,
                 # knn100,
                 # stacked
                 # baggedSVM10,
                 # baggedSVM30
                 # boostedSVM10
                 # boostedkNN50,
                 # baggedBayes5,
                 # baggedBayes10,
                 # baggedBayes20,
                 # boostedBayes5,
                 # boostedBayes10
                 # baggedTree5,
                 # baggedTree20,
                 # boostedTree5,
                 # boostedTree20
                 # randomForest
                 ]
    
    localTime = time.asctime( time.localtime(time.time()))
    testFile.write(localTime + "\n")
    
    # test accuracy of the classifiers on each class
    # print "CLASS ACCURACY"
    # for learner in learners:
    #     print learner.name
    #     testClassAccuracies(TRAIN_DATA, learner, k=5)
    #     print "\n"
    
    # cross-validation
    # print "CROSS-VALIDATION"
    # testFile.write("Test: Cross-validation\n")
    # cv = Orange.evaluation.testing.cross_validation(learners, TRAIN_DATA, folds=5)
    
    # for i in range(len(learners)):
    #     accuracyCV = Orange.evaluation.scoring.CA(cv)[i]
    #     print "%s %.4f\n" % (learners[i].name, accuracyCV)
    #     testFile.write(learners[i].name + "\t" + str(accuracyCV) + "\n")

#    # proportion test
#    testFile.write("Test: Proportion test\n")
#    print "PROPORTION TEST"
#    pt = Orange.evaluation.testing.proportion_test(learners, TRAIN_DATA,
#                                                    learning_proportion=0.7,
#                                                    times = 5)
#    for i in range(len(learners)):
#        accuracyPT = Orange.evaluation.scoring.CA(pt)[i]
#        print "%s %.4f\n" % (learners[i].name, accuracyPT)
#        testFile.write(learners[i].name + "\t" + str(accuracyPT) + "\n")
#

    # learning curve
    # print "LEARNING CURVE"
    # props = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # lc = Orange.evaluation.testing.learning_curve_n(learners, TRAIN_DATA, folds=5,
    #                                                 proportions=props)
    # for i in range(len(lc)):
    #     for j in range(len(learners)):
    #         accuracyLC = Orange.evaluation.scoring.CA(lc[i])[j]
    #         print "%s %f: %.4f\n" % (learners[j].name, props[i], accuracyLC)
    # 
    # 
    testFile.write("\n")
    testFile.close()


def test_fss(learner, data, t=0.01):
    fss = orngFSS.FilterAttsAboveThresh(threshold=t)
    fLearner = orngFSS.FilteredLearner(learner, filter=fss,
        name='%s & fss' % (learner.name))
    learners = [learner, fLearner]
    results = orngTest.crossValidation(learners, data, folds=10, storeClassifiers=1)

    # how many attributes did each classifier use?
    natt = [0.] * len(learners)
    for fold in range(results.numberOfIterations):
        for lrn in range(len(learners)):
            natt[lrn] += len(results.classifiers[fold][lrn].domain.attributes)
    for lrn in range(len(learners)):
        natt[lrn] = natt[lrn] / 10.

    print "\nLearner         Accuracy  #Atts"
    for i in range(len(learners)):
        print "%-15s %5.3f     %5.2f" % (learners[i].name, orngStat.CA(results)[i], natt[i])

    # which attributes were used in filtered case?
    print '\nAttribute usage (how many folds attribute was used):'
    used = {}
    for fold in range(results.numberOfIterations):
        for att in results.classifiers[fold][1].domain.attributes:
            a = att.name
            if a in used.keys(): used[a] += 1
            else: used[a] = 1
    for a in used.keys():
        print '%2d x %s' % (used[a], a)


def testClassAccuracies(data, learner, k=5):
    classes = data.domain.classVar.values
    classAccuracies = [0.0] * len(classes)
    selection = orange.MakeRandomIndicesCV(data, folds=k)
    for testFold in range(k):
        trainData = data.select(selection, testFold, negate=1)
        testData = data.select(selection, testFold)
        hits = [0.] * len(classes)
        totals = [0.] * len(classes)
        classifier = learner(trainData)
        for ex in testData:
            totals[int(ex.getclass())] += 1
            if (classifier(ex) == ex.getclass()):
                hits[int(ex.getclass())] += 1
        for i in range(len(classes)):
            classAccuracies[i] += hits[i] / totals[i]

    for i in range(len(classes)):
        print "%s: %.4f" % (classes[i], classAccuracies[i] / k)


if __name__ == '__main__':
    main()

