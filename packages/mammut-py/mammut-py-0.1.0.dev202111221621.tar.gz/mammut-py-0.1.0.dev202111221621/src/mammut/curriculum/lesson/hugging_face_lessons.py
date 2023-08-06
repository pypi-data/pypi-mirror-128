from mammut.curriculum.lesson.lesson_base import Lesson
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.models.model_base import ModelBase
from mammut.curriculum.models.hugging_face.roberta import (
    HuggingFaceRobertaTokenClassificationModel,
    HuggingFaceRobertaSequenceClassificationModel,
    HuggingFaceRobertaQuestionAnsweringModel,
)
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class HuggingFaceLessonFactory(type):
    """
    Implements a factory class from the lesson_base.Lesson class
    to create any HuggingFaceLesson concrete class
    that works with the different HuggingFace models curriculum wrapper.
    .
    """
    def __new__(cls, lesson_name, *args, **kwargs):
        def _get_model_instance(self) -> ModelBase:
            """Factory method for concrete instantiation of model at
            initialization time. The model returned depends on the self.name value.
            """
            model_name = self.name.replace("Lesson", "Model")
            if model_name == "HuggingFaceRobertaTokenClassificationModel":
                return HuggingFaceRobertaTokenClassificationModel(
                    self.parameters_dict,
                    self.course,
                    self.lesson_id,
                    self._mammut_session_context,
                    self.corpus_id,
                    self._corpus_map_reference,
                )
            elif model_name == "HuggingFaceRobertaSequenceClassificationModel":
                return HuggingFaceRobertaSequenceClassificationModel(
                    self.parameters_dict,
                    self.course,
                    self.lesson_id,
                    self._mammut_session_context,
                    self.corpus_id,
                    self._corpus_map_reference,
                )
            elif model_name == "HuggingFaceRobertaQuestionAnsweringModel":
                return HuggingFaceRobertaQuestionAnsweringModel(
                    self.parameters_dict,
                    self.course,
                    self.lesson_id,
                    self._mammut_session_context,
                    self.corpus_id,
                    self._corpus_map_reference,
                )
            else:
                raise ValueError(f"this {model_name} isn't implemented yet")

        def get_corpus(
            self, corpus_id: int, corpus_map: CorpusMap,
        ):
            """Returns a training corpus from the corpus map.

            Args:
                corpus_id(int): corpus id in corpus map sheet in package.
                corpus_map: CorpusMap object from within the Package used.

            Returns:
            The corpus instance.
            """

            corpus = corpus_map.get_corpus_by_id(corpus_id)
            dataset = corpus.get_hf_dataset()
            return dataset

        def lecture(self):
            """Loads and prepare the model, tokenizer and data for this lesson.

            Currently, this data is prepared:
               - Download the pretrained model in memory.
            """
            self.preprocessed_data = self.model.tokenize_corpus(
                self.get_corpus(self.corpus_id, self._corpus_map_reference)
            )
            self.model.load_pretrained_models()

        def practice(self, mammut_session_context: MammutSessionContext):
            """Practice the lessons by training the model with prepared data.

            Args:
                mammut_session_context: The session context from the classroom.
            """
            self.model.train(
                mammut_session_context, **{"corpus": self.preprocessed_data}
            )
            self.model.save(mammut_session_context)

        new_class_type = type(
            lesson_name,
            (Lesson,),
            {
                "name": lesson_name,
                "_get_model_instance": _get_model_instance,
                "get_corpus": get_corpus,
                "lecture": lecture,
                "practice": practice,
            },
        )
        return new_class_type


HuggingFaceRobertaTokenClassificationLesson = HuggingFaceLessonFactory(
    "HuggingFaceRobertaTokenClassificationLesson", (), {}
)
HuggingFaceRobertaSequenceClassificationLesson = HuggingFaceLessonFactory(
    "HuggingFaceRobertaSequenceClassificationLesson", (), {}
)
HuggingFaceRobertaQuestionAnsweringLesson = HuggingFaceLessonFactory(
    "HuggingFaceRobertaQuestionAnsweringLesson", (), {}
)
