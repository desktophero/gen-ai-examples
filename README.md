# gen-ai-examples

I'm starting this repo to collect some of my local experiments and testing with various gen ai tools in and around open source.

## My Setup

### Workstation

While I have access to different OSes and compute form factors, my daily driver is a:

- MacBook Air,
- M2,
- 24 GB of RAM

For the most part, all of my examples and journalling will be with this setup. For some of the experiments, I will look to recreate on a Windows machine. I'll also spin up spot instances in the cloud when needed.

### Installs and Dependencies

| Install            | Link                                                         | Details                                                |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------ |
| `ollama`           | [link](https://github.com/ollama/ollama)                     | I'm on v0.1.27                                         |
| `mistral-openorca` | [link](https://huggingface.co/Open-Orca/Mistral-7B-OpenOrca) | I keep trying others\* but this one keeps working well |
| `python`           | [link](https://www.python.org/downloads/)                    | Using `3.11.7`                                         |
| `pipenv`           | [link](https://pipenv.pypa.io/en/latest/)                    | For package installs, scripts, etc.                    |
| `jq`               | [link](https://github.com/jqlang/jq)                         | Filter and parse JSON content                          |

> - LLama2 and Mistral are the other two LLMs I've used locally. I don't have enough local resources for other LLMs

I don't go into setup of all the above. I didn't do anything special except RTFM.

### Pipfile

Please take a look at the Pipfile packages to know all the items in this setup. Via `pipenv install` (called out below), several dependencies are installed.

### Prep

The way I get my workstation into the right space includes the following steps:

- Open a terminal into the directory where you cloned this repo
- Run `pipenv shell`: use a `pipenv` shell
- Run `pipenv run install`: install dependencies
- Run `pipenv run setup`: get PDF files as data
- Run `pipenv run mistral`: get the LLM into Ollama
- Run `pipenv run gen-docs`: this will create a series of local Markdown (`md`) files to show loading multiple `md` files

## Use Cases

### RAG

One of the first experiments I'll be journalling here is around RAG, or Retrieval Augmented Generated, AI. Here's an AWS doc I read through to get some better understanding on the approach:

[link](https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-customize-rag.html)

One of the things I'm having to replicate is decoupling work-related content and provide similarly structured Markdown files to use RAG as a mechanism to ingest, index, and then use as a data source for asking questions. To make sure I'm not using actual work-related content, I'll look at using fake data or public domain data that I can safely manipulate.

#### Documents

The initial testing I'm doing uses all public data. This includes PDFs and JSON files that are available on the Internet, like the Great Gatsby. You can run `./setup.sh` from the root of this directory to collect the files. These files are not stored in the repo.

### Loading Documents

> Be sure to run checkout the [setup prep](#prep) section above!

After running the prep steps above:

- Run `pipenv run load --type <pdf|md>`: depending on your choice of `pdf` (default) or `md`, the vector database is loaded with different information:
  - `pdf`: this loads the Gatsby document to Chroma. 
  - `md`: this loads the gibberish IT policy markdown files from `data/gibberish/output`
- Run `pipenv run search "<your search query>"`: this will search the vector database using the LLM

Here are some examples:

#### Loading the data

```shell
pipenv run load
[snip]
Loaded client=SentenceTransformer(
  (0): Transformer({'max_seq_length': 384, 'do_lower_case': False}) with Transformer model: MPNetModel
  (1): Pooling({'word_embedding_dimension': 768, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
  (2): Normalize()
) model_name='sentence-transformers/all-mpnet-base-v2' cache_folder=None model_kwargs={} encode_kwargs={} multi_process=False show_progress=True embeddings.
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 40/40 [00:10<00:00,  3.87it/s]
Saved 1252 chunks to chroma.
pipenv run load  41.12s user 17.67s system 316% cpu 18.600 total
```

> The load has taken roughly 15-22 seconds with each iteration

#### Search the data

```shell
> pipenv run search "who are the main 5 characters in the Great Gatsby?" | jq -r '.result'

The main five characters in The Great Gatsby are Jay Gatsby, Daisy Buchanan, Nick Carraway, Jordan Baker, and Tom Buchanan.<|im_end|>
```

> the search has taken 5-7 seconds with each iteration
