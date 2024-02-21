# gen-ai-examples

I'm starting this repo to collect some of my local experiments and testing with various gen ai tools in and around open source.

## My Setup

While I have access to different OSes and compute form factors, my daily driver is a:

- MacBook Air, 
- M2,
- 24 GB of RAM

For the most part, all of my examples and journalling will be with this setup. For some of the experiments, I will look to recreate on a Windows machine. I'll also spin up spot instances in the cloud when needed.  


## Use Cases

### RAG 

One of the first experiments I'll be journalling here is around RAG, or Retrieval Augmented Generated, AI. Here's an AWS doc I read through to get some better understanding on the approach:

[link](https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-customize-rag.html)

One of the things I'm having to replicate is decoupling work-related content and provide similarly structured Markdown files to use RAG as a mechanism to ingest, index, and then use as a data source for asking questions. To make sure I'm not using actual work-related content, I'll look at using fake data or public domain data that I can safely manipulate. 
