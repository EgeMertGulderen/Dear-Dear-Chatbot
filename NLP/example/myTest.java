package org.example;

import py4j.GatewayServer;
import zemberek.morphology.TurkishMorphology;
import zemberek.morphology.analysis.SingleAnalysis;
import zemberek.morphology.analysis.WordAnalysis;
import zemberek.ner.NerDataSet;
import zemberek.ner.PerceptronNer;
import zemberek.ner.PerceptronNerTrainer;
import zemberek.tokenization.Token;
import zemberek.tokenization.TurkishTokenizer;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class myTest {

    List<String> Words = new ArrayList<>();
    List<String> Lem_Words = new ArrayList<>();
    List<List<Object>> pairs = new ArrayList<List<Object>>();

    List<String > classes = new ArrayList<>();
    public List<String> sentence_tokenize(String sentence)
    {
        TurkishTokenizer tokenizer = TurkishTokenizer.DEFAULT;
        List<Token> tokens = tokenizer.tokenize(sentence);

        List<String> lemmas = new ArrayList<>();
        System.out.println(tokens);
        for (Token token:tokens)
        {
            lemmas.add(sentence_analyze(token.getText()));
        }

        System.out.println(lemmas);
        return lemmas;

    }
    public String  sentence_analyze(String sentence)
    {
        TurkishMorphology m= TurkishMorphology.createWithDefaults();

        WordAnalysis result = m.analyze(sentence);
        String temp = null;
        for (SingleAnalysis analysis : result) {
            temp = analysis.getStem();
        }

        return temp;
    }

    public String  stemming(String word)
    {
        TurkishMorphology m = TurkishMorphology.createWithDefaults();

        WordAnalysis result = m.analyze(word);

        String temp = new String();
        for (SingleAnalysis analysis : result) {

            temp = analysis.getStem();
        }
        System.out.println(temp);
        return temp;
    }
    public List<String> tokenize(String test, String intents)
    {
        TurkishTokenizer tokenizer = TurkishTokenizer.DEFAULT;
        List<Token> tokens = tokenizer.tokenize(test);
        List<String> words = new ArrayList<>();
        List<Object> temp = new ArrayList<>();

        for (Token token:tokens)
        {
            words.add(token.getText());
            Words.add(token.getText());
        }

        temp.add(words);
        temp.add(intents);
        pairs.add(temp);

        return words;
    }
    public void Analyze()
    {
        TurkishMorphology m= TurkishMorphology.createWithDefaults();
        Words.remove("2022/2023");
        Words.remove("2");

        for (String word : Words)
        {
            WordAnalysis result = m.analyze(word);
            for (SingleAnalysis analysis : result) {
                String temp;
                Lem_Words.add(analysis.getLemmas().get(0));

            }
        }
        Collections.sort(Lem_Words);

        List<String> newList1 = new ArrayList<>();
        for (String element : Lem_Words) {

            // If this element is not present in newList
            // then add it
            if (!newList1.contains(element)) {

                newList1.add(element);
            }
        }

        newList1.remove("?");
        Lem_Words = newList1;


    }
    public List<String> getLem_Words()
    {
        return Lem_Words;
    }
    public List<List<Object>> get_pairs()
    {

        return pairs;
    }

    public void Entity() throws IOException {
        Path trainPath = Paths.get("ner-train");
        Path testPath = Paths.get("ner-train");
        //Path modelRoot = Paths.get("my-model");

        NerDataSet trainingSet;
        trainingSet = NerDataSet.load(trainPath, NerDataSet.AnnotationStyle.BRACKET);
        trainingSet.info(); // prints information


        NerDataSet testSet;
        testSet = NerDataSet.load(testPath, NerDataSet.AnnotationStyle.BRACKET);
        testSet.info();

        TurkishMorphology morphology = TurkishMorphology.createWithDefaults();

        // Training occurs here. Result is a PerceptronNer instance.
// There will be 7 iterations with 0.1 learning rate.
        PerceptronNer ner = new PerceptronNerTrainer(morphology).train(trainingSet, testSet, 7, 0.1f);


        //Files.createDirectories(modelRoot);
        //ner.saveModelAsText(modelRoot);

    }
    public static void main(String[] args) {
        myTest app = new myTest();
        // app is now the gateway.entry_point
        GatewayServer server = new GatewayServer(app);
        server.start();
    }
}
