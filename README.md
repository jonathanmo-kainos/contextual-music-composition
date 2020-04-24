# contextual-music-composition
A context driven neural network which generates music

This is a web application which takes user input, and sits on a sentiment analysis API and machine learning model to generate music based on the user input.

The user input is in the form of text and is analysed using Microsoft Azures Cognitive Services Text Analysis sentiment analysis API. From this, it determines whether to generate a major or minor song and affect other components of the music such as note length, note density, speed etc.

The model is an autoencoder which has been trained on a dataset of 10,000 16 bar video game and anime soundtrack MIDI files.
PCA has been performed to get the most significant components of the encoded samples and determine how the user can affect the generated music.
