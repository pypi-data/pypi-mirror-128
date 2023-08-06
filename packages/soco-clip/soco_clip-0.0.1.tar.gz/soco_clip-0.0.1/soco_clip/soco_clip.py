import math
from PIL import Image
import torch
from argparse import ArgumentParser
from torchvision import transforms as T
from .models.wrapper import CustomCLIPWrapper
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import PIL
import soco_clip.clip as clip


class CLIP(object):
    def __init__(self, clip_model="ViT-B-16", model_path = None, tokenizer=None, txt_encoder=None):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer) if tokenizer else None  #model_path = "zh_roberta_vit16.ckpt", tokenizer="hfl/chinese-roberta-wwm-ext", txt_encoder="hfl/chinese-roberta-wwm-ext"
        txt_encoder = AutoModel.from_pretrained(txt_encoder) if txt_encoder else None
        self.model = CustomCLIPWrapper.load_from_checkpoint(checkpoint_path=model_path, text_encoder=txt_encoder, minibatch_size=64, avg_word_embs=True ) if model_path else None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_encoder,self.preprocess = clip.load(clip_model, device=self.device) 
        if self.model:
            self.model.eval()

    def text_encode(self, query):
        tk = self.tokenizer(query, return_tensors='pt', padding=True, truncation=True)
        y_hat = self.model.change_text_emb(self.model.encode_text(tk))
        return F.normalize(y_hat.to(self.device))
    
    def clip_text_encode(self, query):
        text_input = clip.tokenize(query).to(self.device)
        text_embedding = self.image_encoder.encode_text(text_input)
        return text_embedding

    def image_encode(self, url):
        image = Image.open(url)
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        img = self.image_encoder.encode_image(image_input)
        return F.normalize(img.to(torch.float32))
    
    def image_encodes(self, urls):
        temp = []
        for url in urls:
            image = Image.open(url)
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            img = self.image_encoder.encode_image(image_input)
            temp.append(img[0])
        return F.normalize(torch.stack(temp, dim=0).to(torch.float32))
