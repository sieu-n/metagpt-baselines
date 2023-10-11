
[Meta-GPT](https://github.com/geekan/MetaGPT) propose multi-agent frameworks for writing code, and claim that it can develop 
programs no other agent framework is capable of. According to Table 2 which is illustrated below, existing frameworks are incapable of 
creating relatively simple games, which was surprising to me considering GPT-4's capabilities. I tested the official prompts, 

The tasks are scored based on a grading system from ‘0’ to ‘3’, where ‘0’ denotes ‘complete failure’, ‘1’ denotes ‘runnable code’, ‘2’ denotes ‘largely expected workflow’, and ‘3’ denotes ‘perfect match to expectations’ (shown in Section 4.2).

| Task                 | AutoGPT | LangChain w/ Python REPL tool | AgentVerse | MetaGPT |
|----------------------|---------|-------------------------------|------------|---------|
| Flappy Bird          | 0       | 0                             | 0          | 1       |
| Tank Battle Game     | 0       | 0                             | 0          | 2       |
| 2048 Game            | 0       | 0                             | 0          | 2       |
| Snake Game           | 0       | 0                             | 0          | 3       |
| Brick Breaker Game   | 0       | 0                             | 0          | 3       |
| Excel Data Process   | 0       | 0                             | 0          | 3       |
| CRUD Manage          | 0       | 0                             | 0          | 3       |


### Experiment procedure


1. enter the official prompt from Table 6.
2. If ChatGPT responds with general suggestions instead of code (e.g. [tank game](https://chat.openai.com/share/5221714a-7251-4a84-b304-5fd4f72d5fb9) ), slightly modify the prompt to make it more explicit(e.g. using pygame, change some verbs)
3. Since ChatGPT responses are typically short, if the model suggested that the current code is incomplete, simply respond `continue` until the code is complete (e.g. [2048-web](https://chat.openai.com/share/24bd875e-64dc-48f5-8eb9-713c398535df)).
4. I simply copy-pasted (and stitched in the case of 3) the generated code without modification. I did not write or modify any line not mentioned by gpt. I prompted `stitch together the final code without omissions` from the `brick` game and did 0 manual modifications

- I didn't rigorously tested this multiple times, but I didn't retry any failed attempts
- I tried my best not to do any sort of p-hacking or prompt engineering apart from the rules mentioned above unless mentioned. 
- I filled missing resource files (e.g. sprites and music) that the model clearly said to include seperately.

### Results

These are tasks claimed to fail, according to Table 2

|   Task    | Result | Conversation url | Description  |
| --------- | ---    | ---------------  | -----------  |
| 2048-web  | ✅     | [link](https://chat.openai.com/share/24bd875e-64dc-48f5-8eb9-713c398535df) |   Not so pretty, but works.   |
|  2048-py  | ✅     | [link](https://chat.openai.com/share/83818bfd-dec7-41a6-8edc-c65b1bd7a4c9) | pygame, the up and down keys are inverted, but works otherwise.  |
|   snake   | ✅     | [link](https://chat.openai.com/share/46c4287c-a7fe-40b8-a1fa-de14d8d46df3)     |  pygame  |
| tank-game | ✅ | [link](https://chat.openai.com/share/5221714a-7251-4a84-b304-5fd4f72d5fb9) | I stitched code from multiple blocks. I did not manually write any line. Nevertheless, this included, sprites, sound, shooting & collision, death checks which weren't pretty, but functions mostly well. I manually added the png and wav files, but did no modifications to the code. |
|   brick   | ✅     | [link](https://chat.openai.com/share/22bbc1d1-bc94-447f-afc8-4304ab942c12)     |  pygame  |
|  flappy   | ❌     | [link](https://chat.openai.com/share/ed67939a-14ee-4843-b2d5-08e3fcf2bcb3)     |  p5js, the game has *some* features but is incomplete |
|   excel   | ✅     | [link](https://chat.openai.com/share/597463c1-8b0d-4fa2-a644-849aa68ad2db)     |    |
|    crud   | ✅     | [link](https://chat.openai.com/share/3736879e-9044-4833-a3ab-6f68c1a2675b)     | Works surprisingly well! One mistake is that it doesn't check for existence on delete unlike on update. |
