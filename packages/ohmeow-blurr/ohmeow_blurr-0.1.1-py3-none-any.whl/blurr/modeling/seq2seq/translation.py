# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/12_modeling-seq2seq-translation.ipynb (unless otherwise specified).

__all__ = ['BlearnerForTranslation']

# Cell
import ast, inspect, torch
from typing import Any, Callable, Dict, List, Optional, Union, Type

from datasets import load_metric as hf_load_metric, list_metrics as hf_list_metrics
from fastcore.all import *
from fastai.callback.all import *
from fastai.data.block import DataBlock, ColReader, ItemGetter, ColSplitter, RandomSplitter
from fastai.data.core import DataLoader, DataLoaders, TfmdDL
from fastai.imports import *
from fastai.learner import *
from fastai.losses import CrossEntropyLossFlat
from fastai.optimizer import Adam, ranger, OptimWrapper, params
from fastai.torch_core import *
from fastai.torch_imports import *
from fastprogress.fastprogress import progress_bar,master_bar
from transformers import (
    AutoModelForSeq2SeqLM, logging,
    PretrainedConfig, PreTrainedTokenizerBase, PreTrainedModel
)

from ...utils import BLURR
from ...data.seq2seq.core import HF_Seq2SeqBlock, HF_Seq2SeqBeforeBatchTransform, default_text_gen_kwargs
from ..core import HF_BaseModelWrapper, HF_BaseModelCallback, HF_PreCalculatedLoss, Blearner
from .core import HF_Seq2SeqMetricsCallback, seq2seq_splitter

logging.set_verbosity_error()

# Cell
@delegates(Blearner.__init__)
class BlearnerForTranslation(Blearner):

    def __init__(
        self,
        dls: DataLoaders,
        hf_model: PreTrainedModel,
        **kwargs
    ):
        super().__init__(dls, hf_model, **kwargs)

    @classmethod
    def get_model_cls(cls):
        return AutoModelForSeq2SeqLM

    @classmethod
    def _add_t5_prefix(cls, inp, src_lang_name, trg_lang_name):
        return f'translate {src_lang_name} to {trg_lang_name}: {inp}'

    @classmethod
    def get_metrics_cb(self):
        seq2seq_metrics = {
            'bleu': { 'returns': "bleu" },
            'meteor': { 'returns': "meteor" },
            'sacrebleu': { 'returns': "score" }
        }

        return HF_Seq2SeqMetricsCallback(custom_metrics=seq2seq_metrics)

    @classmethod
    def _create_learner(
        cls,
        # Your raw dataset
        data,
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The language of your source (inputs)
        src_lang_name:str='English',
        # The attribute/column of your source language texts
        src_lang_attr:str='src_lang',
        # The attribute/column of your target language texts
        trg_lang_name:str='English',
        # The attribute/column of your target language texts (this is what you want to predict)
        trg_lang_attr:str='trg_lang',
        # The max length of your raw text to consider for summarization
        max_length:Union[int,str]=None,
        # The max length of your targets (sumamrized) text
        max_target_length:Union[int,str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any additional keyword arguments applied during tokenization
        hf_tok_kwargs:dict={},
        # If you want to override your Blurr transform's `text_gen_kwargs`, do that here
        text_gen_kwargs:dict={},
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs:dict={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs:dict={}
    ):
        # we need to find the architecture to ensure "mbart" specific tokenizer kwargs are included
        model_cls = cls.get_model_cls()
        model = model_cls.from_pretrained(pretrained_model_name_or_path)
        hf_arch = BLURR.get_model_architecture(type(model).__name__)

        if (hf_arch == 'mbart'):
            hf_tok_kwargs = { **{'src_lang': 'en_XX', 'tgt_lang': 'en_XX'}, **hf_tok_kwargs }

        # get our hf objects
        hf_arch, hf_config, hf_tokenizer, hf_model = BLURR.get_hf_objects(pretrained_model_name_or_path,
                                                                          model_cls=model_cls,
                                                                          tokenizer_kwargs=hf_tok_kwargs)

        # if we need to preprocess the raw data before creating our DataLoaders
        if (preprocess_func):
            data = preprocess_func(data, hf_arch, hf_config, hf_tokenizer, hf_model, text_attr, summary_attr)

        # update text generation kwargs
        text_gen_kwargs = { **text_gen_kwargs, **default_text_gen_kwargs(hf_config, hf_model, task='translation') }

        # not all "summarization" parameters are for the model.generate method ... remove them here
        generate_func_args = list(inspect.signature(hf_model.generate).parameters.keys())
        for k in text_gen_kwargs.copy():
            if k not in generate_func_args: del text_gen_kwargs[k]

        # update our text generation kwargs for mbart
        if (hf_arch == 'mbart'):
            text_gen_kwargs = { **{'decoder_start_token_id': 'en_XX'}, **text_gen_kwargs }

        # build dblock, dls, and default metrics (optional)
        if (isinstance(data, pd.DataFrame)):
            get_x = Pipeline(funcs=[ColReader(src_lang_attr)])
            get_y = ColReader(trg_lang_attr)
        else:
            get_x = Pipeline(funcs=[ItemGetter(src_lang_attr)])
            get_y = ItemGetter(trg_lang_attr)

        if (hf_arch == 't5'):
            get_x.add(partial(cls._add_t5_prefix, src_lang_name=src_lang_name, trg_lang_name=trg_lang_name))

        before_batch_tfm = HF_Seq2SeqBeforeBatchTransform(hf_arch, hf_config, hf_tokenizer, hf_model,
                                                          max_length=max_length,
                                                          max_target_length=max_target_length,
                                                          text_gen_kwargs=text_gen_kwargs)

        blocks = (HF_Seq2SeqBlock(before_batch_tfm=before_batch_tfm), noop)
        dblock = DataBlock(blocks=blocks,
                           get_x=get_x,
                           get_y=get_y,
                           splitter=dblock_splitter)

        dls = dblock.dataloaders(data, **dl_kwargs.copy())

        # return BLearner instance
        learner_kwargs['splitter'] = learner_kwargs.pop('splitter', partial(seq2seq_splitter, arch=hf_arch))
        learner_kwargs['loss_func'] = learner_kwargs.pop('loss_func', CrossEntropyLossFlat())
        return cls(dls, hf_model, **learner_kwargs.copy())

    @classmethod
    def from_dataframe(
        cls,
        # Your pandas DataFrame
        df,
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The language of your source (inputs)
        src_lang_name:str='English',
        # The attribute/column of your source language texts
        src_lang_attr:str='src_lang',
        # The attribute/column of your target language texts
        trg_lang_name:str='English',
        # The attribute/column of your target language texts (this is what you want to predict)
        trg_lang_attr:str='trg_lang',
        # The max length of your raw text to consider for summarization
        max_length:Union[int,str]=None,
        # The max length of your targets (sumamrized) text
        max_target_length:Union[int,str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any additional keyword arguments applied during tokenization
        hf_tok_kwargs:dict={},
        # If you want to override your Blurr transform's `text_gen_kwargs`, do that here
        text_gen_kwargs:dict={},
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs:dict={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs:dict={}
    ):
        return cls._create_learner(df,
                                   pretrained_model_name_or_path=pretrained_model_name_or_path,
                                   preprocess_func=preprocess_func,
                                   src_lang_name=src_lang_name,
                                   src_lang_attr=src_lang_attr,
                                   trg_lang_name=trg_lang_name,
                                   trg_lang_attr=trg_lang_attr,
                                   max_length=max_length,
                                   max_target_length=max_target_length,
                                   dblock_splitter=dblock_splitter,
                                   hf_tok_kwargs=hf_tok_kwargs, text_gen_kwargs=text_gen_kwargs,
                                   dl_kwargs=dl_kwargs, learner_kwargs=learner_kwargs)


    @classmethod
    def from_csv(
        cls,
        # The path to your csv file
        csv_file:Union[Path, str],
        # The name or path of the pretrained model you want to fine-tune
        pretrained_model_name_or_path:Optional[Union[str, os.PathLike]],
        # A function to perform any preprocessing required for your Dataset
        preprocess_func:Callable=None,
        # The language of your source (inputs)
        src_lang_name:str='English',
        # The attribute/column of your source language texts
        src_lang_attr:str='src_lang',
        # The attribute/column of your target language texts
        trg_lang_name:str='English',
        # The attribute/column of your target language texts (this is what you want to predict)
        trg_lang_attr:str='trg_lang',
        # The max length of your raw text to consider for summarization
        max_length:Union[int,str]=None,
        # The max length of your targets (sumamrized) text
        max_target_length:Union[int,str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any additional keyword arguments applied during tokenization
        hf_tok_kwargs:dict={},
        # If you want to override your Blurr transform's `text_gen_kwargs`, do that here
        text_gen_kwargs:dict={},
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs:dict={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs:dict={}
    ):
        df = pd.read_csv(csv_file)

        return cls.from_dataframe(df,
                                  pretrained_model_name_or_path=pretrained_model_name_or_path,
                                  preprocess_func=preprocess_func,
                                  src_lang_name=src_lang_name,
                                  src_lang_attr=src_lang_attr,
                                  trg_lang_name=trg_lang_name,
                                  trg_lang_attr=trg_lang_attr,
                                  max_length=max_length,
                                  max_target_length=max_target_length,
                                  dblock_splitter=dblock_splitter,
                                  hf_tok_kwargs=hf_tok_kwargs, text_gen_kwargs=text_gen_kwargs,
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
        # The language of your source (inputs)
        src_lang_name:str='English',
        # The attribute/column of your source language texts
        src_lang_attr:str='src_lang',
        # The attribute/column of your target language texts
        trg_lang_name:str='English',
        # The attribute/column of your target language texts (this is what you want to predict)
        trg_lang_attr:str='trg_lang',
        # The max length of your raw text to consider for summarization
        max_length:Union[int,str]=None,
        # The max length of your targets (sumamrized) text
        max_target_length:Union[int,str]=None,
        # A function that will split your Dataset into a training and validation set
        # See [here](https://docs.fast.ai/data.transforms.html#Split) for a list of fast.ai splitters
        dblock_splitter:Callable=RandomSplitter(),
        # Any additional keyword arguments applied during tokenization
        hf_tok_kwargs:dict={},
        # If you want to override your Blurr transform's `text_gen_kwargs`, do that here
        text_gen_kwargs:dict={},
        # Any kwargs to pass to your `DataLoaders`
        dl_kwargs:dict={},
        # Any kwargs to pass to your task specific `Blearner`
        learner_kwargs:dict={}
    ):
        return cls._create_learner(ds,
                                   pretrained_model_name_or_path=pretrained_model_name_or_path,
                                   preprocess_func=preprocess_func,
                                   src_lang_name=src_lang_name,
                                   src_lang_attr=src_lang_attr,
                                   trg_lang_name=trg_lang_name,
                                   trg_lang_attr=trg_lang_attr,
                                   max_length=max_length,
                                   max_target_length=max_target_length,
                                   dblock_splitter=dblock_splitter,
                                   hf_tok_kwargs=hf_tok_kwargs, text_gen_kwargs=text_gen_kwargs,
                                   dl_kwargs=dl_kwargs, learner_kwargs=learner_kwargs)
