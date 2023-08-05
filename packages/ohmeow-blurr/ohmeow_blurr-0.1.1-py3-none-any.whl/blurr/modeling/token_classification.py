# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_modeling-token-classification.ipynb (unless otherwise specified).

__all__ = ['calculate_token_class_metrics', 'HF_TokenClassMetricsCallback', 'BlearnerForTokenClassification']

# Cell
import os, ast, inspect
from typing import Any, Callable, Dict, List, Optional, Union, Type

from fastcore.all import *
from fastai.callback.all import *
from fastai.data.block import DataBlock, ColReader, ItemGetter, ColSplitter, RandomSplitter
from fastai.data.core import DataLoader, DataLoaders, TfmdDL
from fastai.imports import *
from fastai.learner import *
from fastai.losses import CrossEntropyLossFlat
from fastai.optimizer import Adam, OptimWrapper, params
from fastai.metrics import perplexity
from fastai.torch_core import *
from fastai.torch_imports import *
from fastprogress.fastprogress import progress_bar,master_bar
from seqeval import metrics as seq_metrics
from transformers import (
    AutoModelForTokenClassification, logging,
    PretrainedConfig, PreTrainedTokenizerBase, PreTrainedModel
)

from ..utils import BLURR
from ..data.core import HF_TextBlock, BlurrDataLoader, get_blurr_tfm, first_blurr_tfm
from .core import HF_PreCalculatedLoss, Blearner
from ..data.token_classification import (
    HF_TokenClassInput, HF_TokenTensorCategory, HF_TokenCategorize,
    HF_TokenCategoryBlock, HF_TokenClassBeforeBatchTransform
)

logging.set_verbosity_error()

# Cell
def calculate_token_class_metrics(pred_toks, targ_toks, metric_key):
    if (metric_key == 'accuracy'): return seq_metrics.accuracy_score(targ_toks, pred_toks)
    if (metric_key == 'precision'): return seq_metrics.precision_score(targ_toks, pred_toks)
    if (metric_key == 'recall'): return seq_metrics.recall_score(targ_toks, pred_toks)
    if (metric_key == 'f1'): return seq_metrics.f1_score(targ_toks, pred_toks)

    if (metric_key == 'classification_report'): return seq_metrics.classification_report(targ_toks, pred_toks)


# Cell
class HF_TokenClassMetricsCallback(Callback):
    """A fastai friendly callback that includes accuracy, precision, recall, and f1 metrics using the
    `seqeval` library.  Additionally, this metric knows how to *not* include your 'ignore_token' in it's
    calculations.

    See [here](https://github.com/chakki-works/seqeval) for more information on `seqeval`.
    """
    def __init__(self, tok_metrics=["accuracy", "precision", "recall", "f1"], **kwargs):
        self.run_before = Recorder

        store_attr(self=self, names='tok_metrics, kwargs')
        self.custom_metrics_dict = { k:None for k in tok_metrics }

        self.do_setup = True

    def setup(self):
        # one time setup code here.
        if (not self.do_setup): return

        # grab the hf_tokenizer from the HF_TokenClassBeforeBatchTransform
        tfm = first_blurr_tfm(self.learn.dls, before_batch_tfm_class=HF_TokenClassBeforeBatchTransform)
        hf_tok_categorize_tfm = get_blurr_tfm(self.learn.dls.tfms[1], tfm_class=HF_TokenCategorize)

        self.hf_tokenizer = tfm.hf_tokenizer
        self.ignore_label_token_id = hf_tok_categorize_tfm.ignore_token_id
        self.tok_special_symbols = list(self.hf_tokenizer.special_tokens_map.values())
        self.tok_kwargs = tfm.kwargs

        # add custom text generation specific metrics
        custom_metric_keys = self.custom_metrics_dict.keys()
        custom_metrics = L([ ValueMetric(partial(self.metric_value, metric_key=k), k) for k in custom_metric_keys ])
        self.learn.metrics = self.learn.metrics + custom_metrics
        self.learn.token_classification_report = None

        self.do_setup = False

    def before_fit(self): self.setup()


    # --- batch begin/after phases ---
    def after_batch(self):
        if (self.training or self.learn.y is None): return

        # do this only for validation set
        preds = self.pred.argmax(dim=-1)
        targs = self.yb[0] # yb is TensorText tuple, item 0 is the data

        preds_list, targets_list = [], []
        for i in range(targs.shape[0]):
            item_targs, item_preds = [], []

            for j in range(targs.shape[1]):
                if (targs[i, j] != self.ignore_label_token_id):
                    item_preds.append(self.dls.vocab[preds[i][j].item()])
                    item_targs.append(self.dls.vocab[targs[i][j].item()])

            preds_list.append(item_preds)
            targets_list.append(item_targs)

        self.results += [ (res[0], res[1]) for res in zip(preds_list, targets_list) ]


    # --- validation begin/after phases ---
    def before_validate(self): self.results = []

    def after_validate(self):
        if (len(self.results) < 1): return

        preds, targs = map(list, zip(*self.results))
        for k in self.custom_metrics_dict.keys():
            self.custom_metrics_dict[k] = calculate_token_class_metrics(targs, preds, metric_key=k)

        try:
            self.learn.token_classification_report = calculate_token_class_metrics(targs,
                                                                                   preds,
                                                                                   'classification_report')
        except ZeroDivisionError as err:
            print(f'Couldn\'t calcualte classification report: {err}')


    # --- for ValueMetric metrics ---
    def metric_value(self, metric_key): return self.custom_metrics_dict[metric_key]

# Cell
@typedispatch
def show_results(
    # This typedispatched `show_results` will be called for `HF_TokenClassInput` typed inputs
    x:HF_TokenClassInput,
    # This typedispatched `show_results` will be called for `HF_TokenTensorCategory` typed targets
    y:HF_TokenTensorCategory,
    # Your raw inputs/targets
    samples,
    # The model's predictions
    outs,
    # Your `Learner`. This is required so as to get at the Hugging Face objects for decoding them into
    # something understandable
    learner,
    # Your `show_results` context
    ctxs=None,
    # The maximum number of items to show
    max_n=6,
     # Any truncation your want applied to your decoded inputs
    trunc_at=None,
    # Any other keyword arguments you want applied to `show_results`
    **kwargs
):
    tfm = first_blurr_tfm(learner.dls, before_batch_tfm_class=HF_TokenClassBeforeBatchTransform)
    hf_tokenizer = tfm.hf_tokenizer
    ignore_token_id = tfm.ignore_token_id

    res = L()
    for inp, trg, sample, pred in zip(x, y, samples, outs):
        # recontstruct the string and split on space to get back your pre-tokenized list of tokens
        toks = hf_tokenizer.convert_ids_to_tokens(inp, skip_special_tokens=True)
        pretokenized_toks =  hf_tokenizer.convert_tokens_to_string(toks).split()

        # get predictions for subtokens that aren't ignored (e.g. special toks and token parts)
        pred_labels = [ pred_lbl for lbl_id, pred_lbl in zip(trg, ast.literal_eval(pred[0])) if lbl_id != -ignore_token_id ]

        trg_labels = ast.literal_eval(sample[1])
        res.append([f'{[ (tok, trg, pred) for idx, (tok, pred, trg) in enumerate(zip(pretokenized_toks, pred_labels, trg_labels)) if (trunc_at is None or idx < trunc_at) ]}'])

    display_df(pd.DataFrame(res, columns=['token / target label / predicted label'])[:max_n])
    return ctxs

# Cell
def _blurr_predict_tokens(
    # The function to do the base predictions (default: self.blurr_predict)
    predict_func:Callable,
    # The str (or list of strings) you want to get token classification predictions for
    items:Union[str, List[str]],
    # The Blurr Transform with information about the Hugging Face objects used in your training
    tfm:Transform
):
    """Remove all the unnecessary predicted tokens after calling `Learner.blurr_predict` or `blurrONNX.predict.
    Aligns the predicted labels, label ids, and probabilities with what you passed in excluding subword tokens
    """
    # grab the Hugging Face tokenizer from the learner's dls.tfms
    hf_tokenizer = tfm.hf_tokenizer
    tok_kwargs = tfm.tok_kwargs

    if (isinstance(items[0], str)): items = [items]

    outs = []
    for inp, res in zip(items, predict_func(items)):
        # blurr_predict returns a list for each, we only doing one at a time so git first element of each
        pred_lbls, pred_lbl_ids, probs = res[0][0], res[1][0], res[2][0]

        # calculate the number of subtokens per raw/input token so that we can determine what predictions to
        # return
        subtoks_per_raw_tok = [ (entity, len(hf_tokenizer.tokenize(str(entity)))) for entity in inp ]

        # very similar to what HF_BatchTransform does with the exception that we are also grabbing
        # the `special_tokens_mask` to help with getting rid or irelevant predicts for any special tokens
        # (e.g., [CLS], [SEP], etc...)
        res = hf_tokenizer(inp, None,
                           max_length=tfm.max_length,
                           padding=tfm.padding,
                           truncation=tfm.truncation,
                           is_split_into_words=tfm.is_split_into_words,
                           **tok_kwargs)

        special_toks_msk = L(res['special_tokens_mask'])
        actual_tok_idxs = special_toks_msk.argwhere(lambda el: el != 1)

        # using the indexes to the actual tokens, get that info from the results returned above
        pred_lbls_list = ast.literal_eval(pred_lbls)
        actual_pred_lbls = L(pred_lbls_list)[actual_tok_idxs]
        actual_pred_lbl_ids = pred_lbl_ids[actual_tok_idxs]
        actual_probs = probs[actual_tok_idxs]

        # now, because a raw token can be mapped to multiple subtokens, we need to build a list of indexes composed
        # of the *first* subtoken used to represent each raw token (that is where the prediction is)
        offset = 0
        raw_trg_idxs = []
        for idx, (raw_tok, sub_tok_count) in enumerate(subtoks_per_raw_tok):
            raw_trg_idxs.append(idx+offset)
            offset += sub_tok_count-1 if (sub_tok_count > 1) else 0

        outs.append((inp,
                     actual_pred_lbls[raw_trg_idxs],
                     actual_pred_lbl_ids[raw_trg_idxs],
                     actual_probs[raw_trg_idxs]))

    return outs

# Cell
@patch
def blurr_predict_tokens(
    self:Learner,
    # The str (or list of strings) you want to get token classification predictions for
    items:Union[str, List[str]],
    # Keyword arguments for `blurr_predict_tokens`
    **kwargs
):
    tfm = first_blurr_tfm(self.dls, before_batch_tfm_class=HF_TokenClassBeforeBatchTransform)
    return _blurr_predict_tokens(self.blurr_predict, items, tfm)

# Cell
@delegates(Blearner.__init__)
class BlearnerForTokenClassification(Blearner):

    def __init__(
        self,
        dls:DataLoaders,
        hf_model:PreTrainedModel,
        **kwargs
    ):
        super().__init__(dls, hf_model, **kwargs)

    @classmethod
    def get_model_cls(self):
        return AutoModelForTokenClassification

    @classmethod
    def _get_y(cls, r, tokens, token_labels, tokenizer):
        return [ (label, len(tokenizer.tokenize(str(entity)))) for entity, label in zip(r[tokens], r[token_labels]) ]

    @classmethod
    def get_metrics_cb(self):
        return HF_TokenClassMetricsCallback()

    @classmethod
    def _create_learner(
        cls,
        # Your raw dataset
        data,
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The attribute in your dataset that contains a list of your tokens
        tokens_attr:List[str]='tokens',
        # The attribute in your dataset that contains the entity labels for each token in your raw text
        token_labels_attr:List[str]='token_labels',
        # The unique entity labels (or vocab) available in your dataset
        labels:List[str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs={}
    ):
        # get our hf objects
        n_labels = len(labels)
        hf_arch, hf_config, hf_tokenizer, hf_model = BLURR.get_hf_objects(pretrained_model_name_or_path,
                                                                          model_cls=cls.get_model_cls(),
                                                                          config_kwargs={'num_labels': n_labels})

        # if we need to preprocess the raw data before creating our DataLoaders
        if (preprocess_func):
            data = preprocess_func(data, hf_arch, hf_config, hf_tokenizer, hf_model, tokens, token_labels, labels)

        # not all architectures include a native pad_token (e.g., gpt2, ctrl, etc...), so we add one here
        if (hf_tokenizer.pad_token is None):
            hf_tokenizer.add_special_tokens({'pad_token': '<pad>'})
            hf_config.pad_token_id = hf_tokenizer.get_vocab()['<pad>']
            hf_model.resize_token_embeddings(len(hf_tokenizer))

        # build getters
        if (isinstance(data, pd.DataFrame)):
            get_x = ColReader(tokens_attr)
            get_y = partial(cls._get_y, tokens=tokens_attr, token_labels=token_labels_attr, tokenizer=hf_tokenizer)
        else:
            get_x = ItemGetter(tokens_attr)
            get_y = partial(cls._get_y, tokens=tokens_attr, token_labels=token_labels_attr, tokenizer=hf_tokenizer)

        before_batch_tfm = HF_TokenClassBeforeBatchTransform(hf_arch, hf_config, hf_tokenizer, hf_model,
                                                             is_split_into_words=True,
                                                             tok_kwargs={ 'return_special_tokens_mask': True })

        blocks = (
            HF_TextBlock(before_batch_tfm=before_batch_tfm, input_return_type=HF_TokenClassInput),
            HF_TokenCategoryBlock(vocab=labels)
        )

        dblock = DataBlock(blocks=blocks,
                           get_x=get_x,
                           get_y=get_y,
                           splitter=dblock_splitter)

        dls = dblock.dataloaders(data, **dl_kwargs.copy())

        # return BLearner instance
        return cls(dls, hf_model, **learner_kwargs.copy())

    @classmethod
    def from_dataframe(
         cls,
        # Your pandas DataFrame
        df:pd.DataFrame,
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The attribute in your dataset that contains a list of your tokens
        tokens_attr:List[str]='tokens',
        # The attribute in your dataset that contains the entity labels for each token in your raw text
        token_labels_attr:List[str]='token_labels',
        # The unique entity labels (or vocab) available in your dataset
        labels:List[str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=ColSplitter(),
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs={}
    ):
        # we need to tell transformer how many labels/classes to expect
        if (labels is None):
            labels = sorted(list(set([lbls for sublist in df[token_labels_attr].tolist() for lbls in sublist])))

        return cls._create_learner(df, pretrained_model_name_or_path, preprocess_func,
                                   tokens_attr, token_labels_attr, labels, dblock_splitter,
                                   dl_kwargs, learner_kwargs)


    @classmethod
    def from_csv(
        cls,
        # The path to your csv file
        csv_file:Union[Path, str],
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The attribute in your dataset that contains a list of your tokens
        tokens_attr:List[str]='tokens',
        # The attribute in your dataset that contains the entity labels for each token in your raw text
        token_labels_attr:List[str]='token_labels',
        # The unique entity labels (or vocab) available in your dataset
        labels:List[str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=ColSplitter(),
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs={}
    ):
        df = pd.read_csv(csv_file)

        return cls.from_dataframe(df,
                                  pretrained_model_name_or_path=pretrained_model_name_or_path,
                                  preprocess_func=preprocess_func,
                                  tokens_attr=tokens_attr, token_labels_attr=token_labels_attr, labels=labels,
                                  dblock_splitter=dblock_splitter,
                                  dl_kwargs=dl_kwargs, learner_kwargs=learner_kwargs)

    @classmethod
    def from_dictionaries(
        cls,
        # A list of dictionaries
        ds:List[Dict],
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The attribute in your dataset that contains a list of your tokens
        tokens_attr:List[str]='tokens',
        # The attribute in your dataset that contains the entity labels for each token in your raw text
        token_labels_attr:List[str]='token_labels',
        # The unique entity labels (or vocab) available in your dataset
        labels:List[str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs={}
    ):

        # we need to tell transformer how many labels/classes to expect
        if (labels is None):
            all_labels = []
            for item in raw_ds: all_labels += item[token_labels_attr]
            labels = sorted(list(set(all_labels)))

        return cls._create_learner(ds, pretrained_model_name_or_path, preprocess_func,
                                   tokens_attr, token_labels_attr, labels, dblock_splitter,
                                   dl_kwargs, learner_kwargs)