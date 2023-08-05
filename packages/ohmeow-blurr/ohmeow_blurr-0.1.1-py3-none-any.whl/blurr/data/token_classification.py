# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_data-token-classification.ipynb (unless otherwise specified).

__all__ = ['HF_TokenTensorCategory', 'HF_TokenCategorize', 'HF_TokenCategoryBlock', 'HF_TokenClassInput',
           'HF_TokenClassBeforeBatchTransform']

# Cell
import os, ast
from functools import reduce

from fastcore.all import *
from fastai.data.block import TransformBlock, Category, CategoryMap
from fastai.imports import *
from fastai.losses import CrossEntropyLossFlat
from fastai.torch_core import *
from fastai.torch_imports import *
from transformers import (
    AutoModelForTokenClassification, logging,
    PretrainedConfig, PreTrainedTokenizerBase, PreTrainedModel
)

from ..utils import BLURR
from .core import HF_BaseInput, HF_BeforeBatchTransform, first_blurr_tfm

logging.set_verbosity_error()

# Cell
class HF_TokenTensorCategory(TensorBase): pass

# Cell
class HF_TokenCategorize(Transform):
    """Reversible transform of a list of category string to `vocab` id"""
    def __init__(
        self,
        # The unique list of entities (e.g., B-LOC) (default: CategoryMap(vocab))
        vocab=None,
        # The token used to identifiy ignored tokens (default: xIGNx)
        ignore_token=None,
        # The token ID that should be ignored when calculating the loss (default: CrossEntropyLossFlat().ignore_index)
        ignore_token_id=None
    ):
        self.vocab = None if vocab is None else CategoryMap(vocab)
        self.ignore_token = '[xIGNx]' if ignore_token is None else ignore_token
        self.ignore_token_id = CrossEntropyLossFlat().ignore_index if ignore_token_id is None else ignore_token_id

        self.loss_func, self.order = CrossEntropyLossFlat(ignore_index=self.ignore_token_id), 1

    def setups(self, dsets):
        if self.vocab is None and dsets is not None: self.vocab = CategoryMap(dsets)
        self.c = len(self.vocab)

    def encodes(self, labels):
        ids = [[self.vocab.o2i[lbl]] + [self.ignore_token_id]*(n_subtoks-1) for lbl, n_subtoks in labels]
        return HF_TokenTensorCategory(reduce(operator.concat, ids))

    def decodes(self, encoded_labels):
        return Category([(self.vocab[lbl_id]) for lbl_id in encoded_labels if lbl_id != self.ignore_token_id ])

# Cell
def HF_TokenCategoryBlock(
    # The unique list of entities (e.g., B-LOC) (default: CategoryMap(vocab))
    vocab=None,
    # The token used to identifiy ignored tokens (default: xIGNx)
    ignore_token=None,
    # The token ID that should be ignored when calculating the loss (default: CrossEntropyLossFlat().ignore_index)
    ignore_token_id=None
):
    """`TransformBlock` for single-label categorical targets"""
    return TransformBlock(type_tfms=HF_TokenCategorize(vocab=vocab,
                                                       ignore_token=ignore_token,
                                                       ignore_token_id=ignore_token_id))

# Cell
class HF_TokenClassInput(HF_BaseInput): pass

# Cell
class HF_TokenClassBeforeBatchTransform(HF_BeforeBatchTransform):
    def __init__(
        self,
        # The abbreviation/name of your Hugging Face transformer architecture (e.b., bert, bart, etc..)
        hf_arch:str,
        # A specific configuration instance you want to use
        hf_config:PretrainedConfig,
        # A Hugging Face tokenizer
        hf_tokenizer:PreTrainedTokenizerBase,
        # A Hugging Face model
        hf_model:PreTrainedModel,
        # The token ID that should be ignored when calculating the loss
        ignore_token_id = CrossEntropyLossFlat().ignore_index,
        # To control the length of the padding/truncation. It can be an integer or None,
        # in which case it will default to the maximum length the model can accept. If the model has no
        # specific maximum input length, truncation/padding to max_length is deactivated.
        # See [Everything you always wanted to know about padding and truncation](https://huggingface.co/transformers/preprocessing.html#everything-you-always-wanted-to-know-about-padding-and-truncation)
        max_length:int=None,
        # To control the `padding` applied to your `hf_tokenizer` during tokenization. If None, will default to
        # `False` or `'do_not_pad'.
        # See [Everything you always wanted to know about padding and truncation](https://huggingface.co/transformers/preprocessing.html#everything-you-always-wanted-to-know-about-padding-and-truncation)
        padding:Union[bool, str]=True,
        # To control `truncation` applied to your `hf_tokenizer` during tokenization. If None, will default to
        # `False` or `do_not_truncate`.
        # See [Everything you always wanted to know about padding and truncation](https://huggingface.co/transformers/preprocessing.html#everything-you-always-wanted-to-know-about-padding-and-truncation)
        truncation:Union[bool, str]=True,
        # The `is_split_into_words` argument applied to your `hf_tokenizer` during tokenization. Set this to `True`
        # if your inputs are pre-tokenized (not numericalized)
        is_split_into_words:bool=False,
        # Any other keyword arguments you want included when using your `hf_tokenizer` to tokenize your inputs
        tok_kwargs={}
        # Keyword arguments to apply to `HF_TokenClassBeforeBatchTransform`
        , **kwargs
    ):
        super().__init__(hf_arch, hf_config, hf_tokenizer, hf_model,
                         max_length=max_length, padding=padding, truncation=truncation,
                         is_split_into_words=is_split_into_words, tok_kwargs=tok_kwargs, **kwargs)

        self.ignore_token_id = ignore_token_id

    def encodes(self, samples):
        samples = super().encodes(samples)
        if (len(samples[0]) == 1): return samples

        target_cls = type(samples[0][1])
        updated_samples = []

        # we assume that first target = the categories we want to predict for each token
        for s in samples:
            targ_len = len(s[1])
            idx_first_input_id = s[0]['special_tokens_mask'].tolist().index(0)
            targ_ids = target_cls([ self.ignore_token_id if (el == 1 or idx > targ_len)
                                   else s[1][idx-idx_first_input_id].item()
                                   for idx, el in enumerate(s[0]['special_tokens_mask']) ])

            updated_samples.append((s[0], targ_ids))

        return updated_samples

# Cell
@typedispatch
def show_batch(
    # This typedispatched `show_batch` will be called for `HF_TokenClassInput` typed inputs
    x:HF_TokenClassInput,
    y,
    # Your raw inputs/targets
    samples,
    # Your `DataLoaders`. This is required so as to get at the Hugging Face objects for
    # decoding them into something understandable
    dataloaders,
    # Your `show_batch` context
    ctxs=None,
    # The maximum number of items to show
    max_n=6,
    # Any truncation your want applied to your decoded inputs
    trunc_at=None,
    # Any other keyword arguments you want applied to `show_batch`
    **kwargs
):
    # grab our tokenizer
    tfm = first_blurr_tfm(dataloaders, before_batch_tfm_class=HF_TokenClassBeforeBatchTransform)
    hf_tokenizer = tfm.hf_tokenizer

    res = L()
    for inp, trg, sample in zip(x, y, samples):
        # recontstruct the string and split on space to get back your pre-tokenized list of tokens
        toks = hf_tokenizer.convert_ids_to_tokens(inp, skip_special_tokens=True)
        pretokenized_toks =  hf_tokenizer.convert_tokens_to_string(toks).split()

        res.append([f'{[ (tok, lbl) for idx, (tok, lbl) in enumerate(zip(pretokenized_toks, ast.literal_eval(sample[1]))) if (trunc_at is None or idx < trunc_at) ]}'])

    display_df(pd.DataFrame(res, columns=['token / target label'])[:max_n])
    return ctxs