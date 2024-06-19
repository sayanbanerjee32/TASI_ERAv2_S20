import gradio as gr
import os

from huggingface_hub import hf_hub_download
import joblib

from utils import encode, decode


REPO_ID = "sayanbanerjee32/bengali_tokenizer"
data_file = "bengali_tokenizer.pkl"

data_dict = joblib.load(
    hf_hub_download(repo_id=REPO_ID, filename=data_file)
)
vocab = data_dict['vocab']
merges = data_dict['merges']
regex_pat = data_dict['regex_pat']



def encode_decode(text):    
    ids = encode(text, regex_pat, merges)
    return ' '.join([str(i) for i in ids]), decode(ids, vocab)


with gr.Blocks() as demo:
    gr.HTML("<h1 align = 'center'> Bengali BPE Tokenizer </h1>")
    gr.HTML("<h4 align = 'center'> Tokenizes bengali text using Byte Pair Encoding algorithm</h4>")
    
    content = gr.Textbox(label = "Enter the Bengali text for tokenization")
    inputs = [
            content,
            ]
    gr.Examples(["বাইরে এতই গরম যে আমি পুরোদিন আমার শীততাপ নিয়ন্ত্রিত বাড়িতে থাকতে চাই।",
                "খুব ভালোভাবেই নিজের দায়িত্ব পালন করেছেন তিনি।",
                "আয়কর উঠে যাচ্ছে অনেকটা।",
                "যদি কোনো ব্যক্তি এ ব্যাপারে দোষী সাব্যস্ত হয় তা হলে ব্যবস্থা নেওয়া হবে।",
                "বছরের বারোটা মাস হলো জানুয়ারি, ফেব্রুয়ারি, মার্চ, এপ্রিল, মে, জুন জুলাই, আগস্ট, সেপ্টেম্বর, অক্টোবর, নভেম্বর আর ডিসেম্বর।"], 
                inputs = inputs)

    generate_btn = gr.Button(value = 'Tokenize')
    with gr.Row():
        encoded = gr.Textbox(label = "Tokens")
        decoded = gr.Textbox(label = "Regenerated text")
    outputs  = [encoded, decoded]
    generate_btn.click(fn = encode_decode, inputs= inputs, outputs = outputs)

## for collab
# demo.launch(debug=True) 

if __name__ == '__main__':
    demo.launch() 
