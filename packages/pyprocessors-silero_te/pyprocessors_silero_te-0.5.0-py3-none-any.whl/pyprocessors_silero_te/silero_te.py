import os
from enum import Enum
from functools import lru_cache
from typing import Type, List, cast

import torch
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')


class SileroModel(str, Enum):
    silero_te = 'silero_te'


class SileroTextEnhancementParameters(ProcessorParameters):
    model: SileroModel = Field(SileroModel.silero_te,
                               description="""The model is published in the repository [silero-models](https://github.com/snakers4/silero-models), can be one of:<br/>
                            <li>`silero_te`: The Text Enhancement model.""")
    lang: str = Field("english",
                      description="""Name of the [language](https://github.com/snakers4/silero-models)
    supported by Silero Text Enhancement model,
    can be one of:<br/>
    <li>`en` English
    <li>`de` German
    <li>`ru` Russian
    <li>`es` Spanish
    """)


class SileroTextEnhancementProcessor(ProcessorBase):
    """Silero_te processor .
    """

    def process(self, documents: List[Document], parameters: ProcessorParameters) \
            -> List[Document]:
        params: SileroTextEnhancementParameters = \
            cast(SileroTextEnhancementParameters, parameters)
        model, example_texts, languages, punct, apply_te = get_pipeline(params.model)
        for document in documents:
            document.text = apply_te(document.text, lan=params.lang)
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SileroTextEnhancementParameters


@lru_cache(maxsize=None)
def get_pipeline(model):
    return torch.hub.load(repo_or_dir='snakers4/silero-models', model=model)
