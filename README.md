# NLP-homework

大三上-自然语言处理导论作业

## Project-1

>Chinese word segmentation.

This task provides PKU data as training set and test set(e.g., you can use 80% data for model training and other 20% for testing), and you are free to use data learned or model trained from any resources.

Evaluation Metrics:
- Precision = (Number of words correctly segmented) / (Number of words segmented) * 100%
- Recall = (Number of words correctly segmented) / (Number of words in the reference) * 100%
- F-measure = 2 * P * R / (P + R)

## Project-2

>N-gram Language Models.

In this assignent you will explore a simple, typical N-gram language model.

This model can be trained and tested on sentence-segented data of a Chinese text corpus. "Word Perplexity" is the most widely-used evaluation metric for language models.

Additional points:
- Test how does the different "Word Perplexity" of the different "N" grams.
- Test how does the different "Word Perplexity" of the different smoothing methods.