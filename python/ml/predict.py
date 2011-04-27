#!/usr/bin/env python

# Copyright 2011 University of California at Berkeley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Aaron Steele and John Wieczorek"

"""This module provides basic characteristics of an Orange data set.

More information at the Orange website:
http://orange.biolab.si

"""
import logging
from optparse import OptionParser
import orange, orngTree

class ClassInstance(object):
    """Data object for data set class instances.

    ClassInstances are comparable by their count.
    """

    def __init__(self, name, count):
        """Constructs a new ClassInstance object.

        Args:
            name - A string class name for the instance
            count - An integer count of class instances in data set
        """
        self.name = name
        self.count = count
    
    def __cmp__(self, other):
        """Compares count."""
        if self.count > other.count:
            return 1
        elif self.count < other.count:
            return -1
        else:
            return 0

    def __str__(self):
        """Returns name=count string."""
        return '%s=%d' % (self.name, self.count)

def classify(datafile):

    data = orange.ExampleTable(datafile)

    # setting up the classifiers
    majority = orange.MajorityLearner(data)
    bayes = orange.BayesLearner(data)
    tree = orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)
    knn = orange.kNNLearner(data, k=21)

    majority.name="Majority"; bayes.name="Naive Bayes";
    tree.name="Tree"; knn.name="kNN"

    classifiers = [majority, bayes, tree, knn]

    # print the head
    print "Possible classes:", data.domain.classVar.values
    print "Probability for republican:"
    print "Original Class",
    for l in classifiers:
        print "%-13s" % (l.name),
    print

    # classify first 10 instances and print probabilities
    for example in data[:10]:
        print "(%-10s)  " % (example.getclass()),
        for c in classifiers:
            p = apply(c, [example, orange.GetProbabilities])
            print "%5.3f        " % (p[0]),
        print

def shape(datafile):
    """Prints a summary of the datafile."""

    data = orange.ExampleTable(datafile)
    
    print "Classes:", len(data.domain.classVar.values)
    print "Attributes:", len(data.domain.attributes),

    # Prints attribute info:
    ncont=0; ndisc=0
    for a in data.domain.attributes:
        if a.varType == orange.VarTypes.Discrete:
            ndisc = ndisc + 1
        else:
            ncont = ncont + 1
    print '(%d continuous, %d discrete)' % (ncont, ndisc)

    # Prints class distribution:
    c = [0] * len(data.domain.classVar.values)
    for e in data:
        c[int(e.getclass())] += 1
    print "ClassInstances: ", len(data), "total\n",
    instances = []
    for i in range(len(data.domain.classVar.values)):
        instances.append(ClassInstance(data.domain.classVar.values[i], c[i]))
    instances.sort()
    for x in instances:
        print x

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)    
    
    # Parses command line parameters:
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="datafile",
                      help="The Orange data file",
                      default=None)
    parser.add_option("-c", "--command", dest="command",
                      help="The command to run (shape, classify)",
                      default=None)

    (options, args) = parser.parse_args()
    datafile = options.datafile
    command = options.command
    logging.info('Command: %s\nDatafile: %s' % (command, datafile))
    
    if command == 'shape':
        shape(datafile)
    elif command == 'classify':
        classify(datafile)

