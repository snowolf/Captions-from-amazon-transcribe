# captions-from-amazon-transcribe

This repository contains code for VOD subtitle creation.

## Prerequisites

- Using Amazon Transcribe get an ASR.json which is response from Amazon Transcribe


```shell
python srt.py output_file_from_transcribe.json captions_name.srt
```


| name   | description                                                  |
| ------ | ------------------------------------------------------------ |
| srt.py | Takes the JSON response from AWS Transcribe and converts to a captions.srt file |
| vtt.py | Takes the JSON response from AWS Transcribe and converts to a captions.vtt file |
