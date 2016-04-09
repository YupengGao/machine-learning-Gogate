package neuralNetwork;


/**
 * A Java class that implements a simple text learner, based on WEKA.
 * To be used with MyFilteredClassifier.java.
 * WEKA is available at: http://www.cs.waikato.ac.nz/ml/weka/
 * Copyright (C) 2013 Jose Maria Gomez Hidalgo - http://www.esp.uem.es/jmgomez
 *
 * This program is free software: you can redistribute it and/or modify
 * it for any purpose.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */

import weka.core.Instances;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;
import weka.classifiers.Evaluation;
import java.util.Random;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.MultilayerPerceptron;
import weka.classifiers.meta.FilteredClassifier;
import weka.core.converters.ArffLoader.ArffReader;
import java.io.*;
import weka.core.*;
import weka.core.converters.*;
import weka.classifiers.trees.*;
import weka.filters.*;
import weka.filters.unsupervised.attribute.*;


/**
 * This class implements a simple text learner in Java using WEKA.
 * It loads a text dataset written in ARFF format, evaluates a classifier on it,
 * and saves the learnt model for further use.
 * @author Jose Maria Gomez Hidalgo - http://www.esp.uem.es/jmgomez
 * @see MyFilteredClassifier
 */
public class neuralNet {

	/**
	 * Object that stores training data.
	 */
	Instances trainData;
	/**
	 * Object that stores the filter
	 */
	StringToWordVector filter;
	/**
	 * Object that stores the classifier
	 */
	FilteredClassifier classifier;
		
	/**
	 * This method loads a dataset in ARFF format. If the file does not exist, or
	 * it has a wrong format, the attribute trainData is null.
	 * @param fileName The name of the file that stores the dataset.
	 */
	public void loadDataset(String fileName) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader(fileName));
			ArffReader arff = new ArffReader(reader);
			trainData = arff.getData();
			System.out.println("===== Loaded dataset: " + fileName + " =====");
			reader.close();
		}
		catch (IOException e) {
			System.out.println("Problem found when reading: " + fileName);
		}
	}
	
	/**
	 * This method evaluates the classifier. As recommended by WEKA documentation,
	 * the classifier is defined but not trained yet. Evaluation of previously
	 * trained classifiers can lead to unexpected results.
	 */
	public void evaluate() {
		try {
			trainData.setClassIndex(0);
			filter = new StringToWordVector();
			filter.setAttributeIndices("last");
			classifier = new FilteredClassifier();
			classifier.setFilter(filter);
			classifier.setClassifier(new NaiveBayes());
			Evaluation eval = new Evaluation(trainData);
			eval.crossValidateModel(classifier, trainData, 4, new Random(1));
			System.out.println(eval.toSummaryString());
			System.out.println(eval.toClassDetailsString());
			System.out.println("===== Evaluating on filtered (training) dataset done =====");
		}
		catch (Exception e) {
			System.out.println("Problem found when evaluating");
		}
	}
	
	/**
	 * This method trains the classifier on the loaded dataset.
	 */
	public void learn() {
		try {
			trainData.setClassIndex(0);
			filter = new StringToWordVector();
			filter.setAttributeIndices("last");
			classifier = new FilteredClassifier();
			classifier.setFilter(filter);
			classifier.setClassifier(new NaiveBayes());
			classifier.buildClassifier(trainData);
			// Uncomment to see the classifier
			// System.out.println(classifier);
			System.out.println("===== Training on filtered (training) dataset done =====");
		}
		catch (Exception e) {
			System.out.println("Problem found when training");
		}
	}
	
	/**
	 * This method saves the trained model into a file. This is done by
	 * simple serialization of the classifier object.
	 * @param fileName The name of the file that will store the trained model.
	 */
	public void saveModel(String fileName) {
		try {
            ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(fileName));
            out.writeObject(classifier);
            out.close();
 			System.out.println("===== Saved model: " + fileName + " =====");
        } 
		catch (IOException e) {
			System.out.println("Problem found when writing: " + fileName);
		}
	}
	
	/**
	 * Main method. It is an example of the usage of this class.
	 * @param args Command-line arguments: fileData and fileModel.
	 */
	public static void main (String[] args) throws Exception{
	
		 //neuralNet learner;
	
		 // convert the directory into a dataset
		
            TextDirectoryLoader loader = new TextDirectoryLoader();
		    loader.setDirectory(new File("/Users/pengpeng/Desktop/train"));
		    Instances trainRaw = loader.getDataSet();
		    
		    loader.setDirectory(new File("/Users/pengpeng/Desktop/test"));
		    Instances testRaw = loader.getDataSet();
		    Standardize filter = new Standardize();
		    filter.setInputFormat(trainRaw);  // initializing the filter once with training set
		    Instances newTrain = Filter.useFilter(trainRaw, filter);  // configures the Filter based on train instances and returns filtered instances
		    Instances newTest = Filter.useFilter(testRaw, filter); 
		 
		    // apply the StringToWordVector
		    // (see the source code of setOptions(String[]) method of the filter
		    // if you want to know which command-line option corresponds to which
		    // bean property)
		    StringToWordVector filter1 = new StringToWordVector();
		    filter1.setInputFormat(newTrain);
		    Instances TrainData = Filter.useFilter(newTrain, filter1);
		    Instances TestData = Filter.useFilter(newTest, filter1);
		  //build model
		   

		    //System.out.println("\n\nFiltered data:\n\n" + TrainData);
//		    ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("/Users/pengpeng/Desktop/Train.arff"));
//            out.writeObject(TrainData);
//            out.close();
//            out = new ObjectOutputStream(new FileOutputStream("/Users/pengpeng/Desktop/Test.arff"));
//            out.writeObject(TestData);
//            out.close();
//		    System.out.println("\n\nFiltered data:\n\n" + dataFiltered);
		  //Instance of NN
		    MultilayerPerceptron mlp = new MultilayerPerceptron();
		    MultilayerPerceptron mlp1 = new MultilayerPerceptron();
		    //Setting Parameters
		    mlp.setLearningRate(0.04);
		    mlp.setMomentum(0.1);
		    mlp.setTrainingTime(1000);
		    mlp.setHiddenLayers("3");

		    mlp.buildClassifier(TrainData);
		    Evaluation eval = new Evaluation(TrainData);
		    eval.evaluateModel(mlp, TestData);
		    System.out.println(eval.toSummaryString("\nResults\n======\nsetLearningRate(0.9)Momentum(0.1)HiddenLayers(3);\n", false));
//		    
//		    mlp1.setLearningRate(0.0034);
//		    mlp1.setMomentum(0.1);
//		    mlp1.setTrainingTime(100);
//		    mlp1.setHiddenLayers("3");
//
//		    mlp1.buildClassifier(TrainData);
//		    Evaluation eval1 = new Evaluation(TrainData);
//		    eval1.evaluateModel(mlp1, TestData);
//		    System.out.println(eval1.toSummaryString("\nResults\n======\nsetLearningRate(0.8)Momentum(0.1)HiddenLayers(3)\n;", false));
//		    
//		    mlp1.setLearningRate(0.0035);
//		    mlp1.setMomentum(0.1);
//		    mlp1.setTrainingTime(100);
//		    mlp1.setHiddenLayers("3");
//
//		    mlp1.buildClassifier(TrainData);
//		    Evaluation eval2 = new Evaluation(TrainData);
//		    eval2.evaluateModel(mlp1, TestData);
//		    System.out.println(eval2.toSummaryString("\nResults\n======\nsetLearningRate(0.8)Momentum(0.1)HiddenLayers(3)\n;", false));
	   
	}
}	