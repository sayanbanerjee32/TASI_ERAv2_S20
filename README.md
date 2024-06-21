# TASI_ERAv2_S20


## Objective

1. Pick any "Indian" language of own choice
2. Build own BPE for this language that satisfies these statistics:
  - it must have 5000+ tokens in its vocabulary
  - it must have a compression ratio of 3 or above

# Bengali BPE Tokenizer



## Dataset

Multiple reference to raw Bengali corpus is available at this [GitHub link](https://github.com/sagorbrur/bangla-corpus). Used following references from that for gathering raw bengali text for the purpose of training the tokenizer.
  - [Tab-delimited Bilingual Sentence Pairs](https://www.manythings.org/anki/) - These are selected sentence pairs from the [Tatoeba Project](http://tatoeba.org/home). This has approximately 6,500 english to bengali sentence pairs. Only Bengali sentectes are extracted for training the tokenization
  - [IndicParaphrase](https://huggingface.co/datasets/ai4bharat/IndicParaphrase) - Only the input data from validation dataset of [Bengali paraphrases](https://huggingface.co/datasets/ai4bharat/IndicParaphrase/blob/main/data/bn_IndicParaphrase_v1.0.zip) are used for the tokenization. That dataset contains 10,000 bengali sentences.
 
## Steps

### Initial experiment

1. Followed the instructions [video](https://youtu.be/zduSFxRajkE) from  Andrej Karpathy and created the [notebook]() for experiment.
2. Updated the model code for adding Gradio in the notebook as part of experiment
3. Added the Gradio app in the notebook

### Pushed Model to HuggingFace Model Hub
1. Refactored code in train.py and model.py
2. Added code to same vocab and model arguments and weights that would need to be used for inferencing later
3. Pushed the model.py and saved artifacts to HuggingFace Model Hub using huggingface API from this [notebook](https://github.com/sayanbanerjee32/TASI_ERAv2_S19/blob/main/gpt_dev_hfhub.ipynb)

### Pushed Gradio App to HuggingFace Spaces
1. Created app.py that can read the model artefacts and vocab artefacts from HuggingFace Model Hub and launch the app
2. Pushed the model.py, app.py and requirements.txt to HuggingFace spaces using huggingface API from this [notebook](https://github.com/sayanbanerjee32/TASI_ERAv2_S19/blob/main/gpt-dev-spaces.ipynb)

## The Huggingface Spaces Gradio App

The app is available [here](https://huggingface.co/spaces/sayanbanerjee32/nano_text_generator)

The App takes following as input 
1. Seed Text (Prompt) - This provided as input text to the GPT model, based on which it generates further contents. If no data is provided, the only a space (" ") is provided as input
2. Max tokens to generate - This controls the numbers of character tokens it will generate. The default value is 100.
3. Temperature - This accepts value between 0 to 1. Higher value introduces more randomness in the next token generation. Default value is set to 0.7.
4. Select Top N in each step - This is optional field. If no value is provided (or <= 0), all available tokens are considered for next token prediction based on SoftMax probability. However, if a number is set then only that many top characters will be considered for next token prediction.
