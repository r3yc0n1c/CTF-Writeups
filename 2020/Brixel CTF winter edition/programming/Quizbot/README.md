# Quizbot (30)
> Legend has it there's a flag at the end when you have a perfect score <br>
> [http://timesink.be/quizbot](http://timesink.be/quizbot)

## The Recon
So they set up a Quizbot with a hint **`Can you beat the 1000 questions?`** which tells us that maybe we can get a reward if we manage to answer all the 1000
questions the Bot is going to ask us!

Without wasting any time I jumped into the Source code. This was fairly simple so I checked the cookies and got the **`PHPSESSID`** is set!

## The Synergy
### First
I thought I'll use **python** + **Selenium** to automate the whole thing but I faced the following issues,
* There were too many answers on Google
* Lots of things to parse
* It's slow

### Second
Hmmmmmm..... to think from a technical point of view, all Quizbots must have a Database of Q&As and if we can find that we're almost done.
After searching for a while I found this site - [Questions quiz test answers general knowledge](https://www.riassuntini.com/questions-quiz-test-answers/questions-quiz-test-answers-general-knowledge.html)
which has all the question answers (tested manually for a couple of questions). Then I saved all the Q&As in a file named **all_10000qs.txt**.
Now, we just need the parser!

## Crafting the Parser
The best idea that came to my mind was **python** for it's amazing module called **requests**. Here's a sneak peek!
```py
import requests
import re

[snip]

def find_answer(question):
	qna = open('all_10000qs.txt').read().strip().split('\n')
	for qa in qna:
		if question in qa:
			ans = qa.split(' : ')[2]
			return ans
      
### gimme flag ###

url = 'http://timesink.be/quizbot/index.php'
session = requests.Session()

[snip]

while score!=1001:
	# GET question
	res = session.get(url)
  
  [snip]
  
  query = get_question(res.text)
	# print(query[1])
	sanitized = sanitize(query[1])
	# print(sanitized)
	ans = find_answer(sanitized)
  
	# POST answer
	d = {'insert_answer': ans}
	a = session.post(url, data=d)
  
  [snip]
```
Now I have the parser but I ran into some weird problems!

## The Final Call
Basically my script worked fine for ~600 questions and then it stopped! After debugging a lot I figured out that there were two issues,
* My Internet was shitty.
* The Bot Server was down.
* The Query text had some weird double spaces and Unicode chars.
* The Answer comparison was Case sensitive (this was the major bug).

So I modified the Script,
* Sanitized the Query text.
* Added the Manual Feed data mode.
* Added Auto-correct mode.
* Added Score count.

And then tried it again. When they fixed the Server, it worked finally and I **got the flag!!!**

#### Full Script - [quizbot_hack.py](quizbot_hack.py)
```py
import requests
import re

"""
https://www.riassuntini.com/questions-quiz-test-answers/questions-quiz-test-answers-general-knowledge.html
"""

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def get_question(text):
	stripped = remove_tags(text).split('\n')
	# print(stripped)
	score = stripped[0][stripped[0].index('?')+1 : stripped[0].index('&nbsp;')]
	for i, sen in enumerate(stripped):
		if 'Question' in sen:
			return [sen, stripped[i+1], score]

def find_answer(question):
	qna = open('all_10000qs.txt').read().strip().split('\n')
	for qa in qna:
		if question in qa:
			ans = qa.split(' : ')[2]
			return ans

def sanitize(text):
	s1 = text.replace('  ', ' ')
	return s1

def autocorrect(text, q):
	correct_ans = text.split('\n')[0].split(': ')[1]	
	# print("[+] CA:", correct_ans, q)
	
	qna = open('all_10000qs.txt').read().strip().split('\n')
	for i in range(len(qna)):
		if q in qna[i]:
			idx = qna[i].index(' Answer : ')
			qna[i] = qna[i][:idx] + ' Answer : ' + correct_ans		# replace the answer with the correct one

	new = open('all_10000qs.txt', 'w')
	for line in qna:
		new.write(line + '\n')


### gimme flag ###

# qna = open('all_10000qs.txt').read().split('\n')
url = 'http://timesink.be/quizbot/index.php'
session = requests.Session()

score = 0
i = 0
# for i in range(1000+1):
while score!=1001:
	# GET question
	res = session.get(url)

	if i == 0:
		print(f"(0-0) Cookie: {res.cookies}\n")

	query = get_question(res.text)
	# print(query[1])
	sanitized = sanitize(query[1])
	# print(sanitized)
	ans = find_answer(sanitized)
	score = int(query[2].split(': ')[1])

	# failed to find the ques in the db / feed manual data
	if ans==None:
		print("(x-x)", query[1])
		ans = input("> ")
		open('all_10000qs.txt', 'a').write(f"\nQuestion : {query[1]} Answer : {ans}")

	# ques_no = int(query[0].split(' ')[2])
	# print(ques_no)
	# if ques_no != score 

	print(f"(^-^) Solved {query[0]} [Score: {score}]")

	# POST answer
	d = {'insert_answer': ans}
	a = session.post(url, data=d)

	# check if the answer was correct / get the correct answer and store in db
	data = remove_tags(a.text)
	if 'Correct!' not in data:		
		autocorrect(data, sanitized)
		print('-'*20)
		print("[+] Q:", sanitized)
		print("[+] Corrected!!!")
		print('-'*20)
		# break
	if score==1000:
		print(a.text)
	i += 1

# print(session.get(url).text)
```
This is the raw script I used. Please ignore the silly stuffs...

## Flag
> **brixelCTF{kn0wl3dg3}**
