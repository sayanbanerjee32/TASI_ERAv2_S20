# TASI_ERAv2_S20


## Objective

1. Pick any "Indian" language of own choice
2. Build own BPE for this language that satisfies these statistics:
   - it must have 5000+ tokens in its vocabulary
   - it must have a compression ratio of 3 or above

# Bengali BPE Tokenizer

Selected Bengali as the Indian language for BPE tokenizer training.

## Dataset

Multiple references of raw Bengali corpus are available at this [GitHub link](https://github.com/sagorbrur/bangla-corpus). Used following references from that for gathering raw bengali text for the purpose of training the tokenizer.
    - [Tab-delimited Bilingual Sentence Pairs](https://www.manythings.org/anki/) - These are selected sentence pairs from the [Tatoeba Project](http://tatoeba.org/home). This has approximately 6,500 english to bengali sentence pairs. Only Bengali sentences are extracted for training the tokenization
    - [IndicParaphrase](https://huggingface.co/datasets/ai4bharat/IndicParaphrase) - Only the input data from validation dataset of [Bengali paraphrases](https://huggingface.co/datasets/ai4bharat/IndicParaphrase/blob/main/data/bn_IndicParaphrase_v1.0.zip) are used for the tokenization. That dataset contains 10,000 Bengali sentences.
 
## Steps

### Initial experiment

1. Followed the instructions from the [video](https://youtu.be/zduSFxRajkE) from  Andrej Karpathy and created the [notebook](https://github.com/sayanbanerjee32/TASI_ERAv2_S20/blob/main/bengali_bpe_tokenizer_experiment.ipynb) for experiment.
2. Experimented with the regular expression that suits bengali language. The intention was to the regular expression for splitting Bengali words instead of characters.
    - Using gpt2 regex `'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+` was resulting in splitting of individual characters instead of words.
    - Used the regex ` ?\p{Bengali}+| ?[^\s\p{Bengali}]+|\s+(?!\S)|\s+` that could split the sentence _"সবাই যা করতে চায় তা করতে চায়নি।"_ into following words _'সবাই', ' যা', ' করতে', ' চায়', ' তা', ' করতে', ' চায়নি', '।'_
3. Updated BPE training process to use text chucks as output from the regular expression splits instead of the complete sentences. This helps avoid merging of tokens across different worlds. [Ref](https://github.com/karpathy/minbpe/blob/master/minbpe/regex.py)
4. Updated `encode` and `decoder` function to deal with text chucks instead of complete sentences. [Ref](https://github.com/karpathy/minbpe/blob/master/minbpe/regex.py)

### Tokenizer training
1. Refactored code in training [notebook](https://github.com/sayanbanerjee32/TASI_ERAv2_S20/blob/main/bengali_bpe_tokenizer_train.ipynb) and [utils.py](https://github.com/sayanbanerjee32/TASI_ERAv2_S20/blob/main/utils.py)
2. Trained the tokenizer to reach **vocab size of 5001 and compression of 11X**
3. Saved vocab file (contains the mapping from tokens to bengali text), merges files (contains the mapping from pair of tokens to be merged to token after merging) and the regular expression that is used for splitting the bengali sentences. All these artifacts are required to perform BPE tokenization on a new text.
4. Pushed the saved artifacts to HuggingFace Model Hub using huggingface API from the notebook

### Pushed Gradio App to HuggingFace Spaces
1. Created app.py that can read the tokenizer artifacts from HuggingFace Model Hub and launch the app,
2. Pushed the app.py, utils.py and requirements.txt to HuggingFace spaces using huggingface API from this [notebook](https://github.com/sayanbanerjee32/TASI_ERAv2_S20/blob/main/bengali_bpe_tokenizer_gradio.ipynb)

## The HuggingFace Spaces Gradio App

The app is available [here](https://huggingface.co/spaces/sayanbanerjee32/bengali_bpe_tokenizer)

The App takes one or more Bengali sentences as input provide following outputs
1. Numeric tokens that represent the sentence (using encode function)
2. Regenerated sentence using the tokens (using decode function)
3. A visualization for each token to Bengali text mapping as explanation for the tokenization.
