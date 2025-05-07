# LLM Summarization Microservice Notes

## Data

I used this Kaggle dataset: https://www.kaggle.com/datasets/justinas/startup-investments?resource=download&select=acquisitions.csv for this project and specifically I used the `acquisitions`, `funding_rounds`, `investments`, and `objects`. I've also put in the `ipos` sheet even though I didn't end up using it. Inside of the messy_data_gen.ipynb, you will find how I combined all these different datasets for further analysis.

After I managed to do some general pre-processing of the data, I then used that data in order to generate some "messy" or "raw" data for the next part of the microservice. For this MVP, I primarily wanted to focus on two different types of scenarios of either startups that were acquired by another company, or startups that received funding from an investor.

This "messy" or raw data can then be provided into the LLM Summarization endpoint which will be talked about in the next section.

## Model

The LLM summarization microservice is hosted on a FastAPI server on endpoint /docs/summarize. It assumes the user provides a valid input of data that can be summarized (i.e. an excerpt/paragraph about a startup that is getting acquired or obtained funding). In addition, it also assumes the user does not provide too little or too much of an input.

For the purposes of an MVP, I used GPT 4o-mini, but this microservice should work on any OpenAI GPT model that's available given the scope of the project. I also used an LLM API for the purposes of this project since it was an MVP and I wanted a working prototype in the time constraints. I will talk more about how I would have approached this project outside of the MVP.

## Testing

I used the messy data (which was synthetically generated, but manually reviewed) as inputs into the LLM summarization microservice and then manually inspected the structured output. From there, I'd finetune the system prompt until the output matched what I had desired.

## Deployment

I utilized a Simple Docker + FastAPI interface for my deployment process and the instructions for how to run the project are inside the README.md. 

## Alternative + Future steps

### Data

I did all my data pre-processing locally inside a Jupyter Notebook in addition to storing all the data inside a local folder. However, if I were to scale out this project, I would use SageMaker Notebook and/or AWS Glue in order to do all ETL, and I would store all the data (raw and processed) inside of S3.

### Model

For the purposes of the MVP, I only used an LLM API for the summarization call, but I would scale out this project by finetuning a local transformer-based LLM model such as DeepSeek or even Meta's Llama. By finetuning on a local model such as that, it would allow for even more specialized answers, missing less fields, and being able to extrapolate more on the given inputs.

Another option that could be explored would be a whole feedback/eval system to help iteratively improve the responses since the feedback and eval metrics are being stored and analyzed continuously. This option of reinforcement learning would be employed if we don't have access to high-quality data.

### Testing

There are two avenues for testing based on the previous section: Finetuning or Reinforcement Learning.

~Finetuning - If we go down the path of finetuning, then we would probably finetune using LoRA with at least 100 input/output pairs. This would require to expand out the messy data generator and then manually checking them OR manually creating these pairs by human hand. Given the simplicity of the prompt, this might be the most efficient route.

~ Reinforcement Learning - If we were to go down this route, it means that we probably chose to expand the Summarization microservice to beyond startup data and as a result, it is impossible to generate input/output pairs to cover all possible cases. With each output the LLM generates, we would have some evaluation and metrics system in place to properly analyze and "score" the result. These would then be stored in some sort of database (S3 for example), and essentially would be re-fed into the model with slight improvements to the prompt or how the data is formatted.

### Deployment

The full deployment of expanding out this MVP would be something similar to this parallel process:

S3 (raw data) -> SageMaker Notebook -> S3 (processed data) -> LLM Model (Training + Finetuning)
User input -> API Gateway -> AWS Lambda Function running FastAPI application -> LLM Model -> Back to user in same pipeline

### Future Steps

Besides all the steps I've listed above as alternates/future steps, some other things I would potentially add to this project would be a more proper UI for a user and also expanding out the use cases to be a general summarization microservice rather than just for raw startup data.
